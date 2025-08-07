from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from datetime import datetime, date, timedelta
import os
import csv
import io
import json
from sqlalchemy import func, and_, or_

compliance_bp = Blueprint('compliance', __name__)

# Helper function to calculate compliance rate
def calculate_compliance_rate(scheduled_doses, taken_doses):
    if scheduled_doses == 0:
        return 0
    return (taken_doses / scheduled_doses) * 100

# Helper function to get scheduled doses for a member
def get_scheduled_doses(member_id, start_date, end_date, is_family_member=False):
    Reminder = current_app.config.get('Reminder')
    
    # Get all active reminders for the member
    query = Reminder.query.filter(Reminder.active == True)
    
    if is_family_member:
        query = query.filter(Reminder.family_member_id == member_id)
    else:
        query = query.filter(Reminder.user_id == member_id, Reminder.family_member_id == None)
    
    reminders = query.all()
    
    # Calculate scheduled doses based on reminder days and date range
    scheduled_count = 0
    current_date = start_date
    
    while current_date <= end_date:
        day_name = current_date.strftime('%A')
        for reminder in reminders:
            # Check if this day is scheduled in the reminder
            if day_name in reminder.days.split(','):
                scheduled_count += 1
        current_date += timedelta(days=1)
    
    return scheduled_count

# Helper function to get taken doses for a member
def get_taken_doses(member_id, start_date, end_date, is_family_member=False):
    SupplementIntake = current_app.config.get('SupplementIntake')
    
    # Convert dates to datetime for comparison
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    # Query intakes within the date range
    query = SupplementIntake.query.filter(
        SupplementIntake.taken_at >= start_datetime,
        SupplementIntake.taken_at <= end_datetime
    )
    
    if is_family_member:
        query = query.filter(SupplementIntake.family_member_id == member_id)
    else:
        query = query.filter(SupplementIntake.user_id == member_id, SupplementIntake.family_member_id == None)
    
    return query.count()

# Get daily compliance for a member
@compliance_bp.route('/daily/<int:member_id>', methods=['GET'])
@jwt_required()
def daily_compliance(member_id):
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    FamilyMember = current_app.config.get('FamilyMember')
    
    # Check if the member_id is for a family member or the user
    is_family_member = False
    member = None
    
    # First check if it's a family member
    family_member = FamilyMember.query.filter_by(id=member_id, user_id=current_user).first()
    if family_member:
        is_family_member = True
        member = family_member
    else:
        # If not a family member, check if it's the current user
        if member_id == current_user:
            member = User.query.get(current_user)
        else:
            return jsonify({'error': 'Unauthorized access to member data'}), 403
    
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    # Get date parameter or use today
    date_str = request.args.get('date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    else:
        target_date = date.today()
    
    # Calculate compliance for the day
    scheduled_doses = get_scheduled_doses(member_id, target_date, target_date, is_family_member)
    taken_doses = get_taken_doses(member_id, target_date, target_date, is_family_member)
    compliance_rate = calculate_compliance_rate(scheduled_doses, taken_doses)
    
    return jsonify({
        'date': target_date.strftime('%Y-%m-%d'),
        'member_id': member_id,
        'member_name': family_member.name if is_family_member else member.username,
        'scheduled_doses': scheduled_doses,
        'taken_doses': taken_doses,
        'compliance_rate': round(compliance_rate, 2)
    }), 200

# Get weekly compliance for a member
@compliance_bp.route('/weekly/<int:member_id>', methods=['GET'])
@jwt_required()
def weekly_compliance(member_id):
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    FamilyMember = current_app.config.get('FamilyMember')
    
    # Check if the member_id is for a family member or the user
    is_family_member = False
    member = None
    
    # First check if it's a family member
    family_member = FamilyMember.query.filter_by(id=member_id, user_id=current_user).first()
    if family_member:
        is_family_member = True
        member = family_member
    else:
        # If not a family member, check if it's the current user
        if member_id == current_user:
            member = User.query.get(current_user)
        else:
            return jsonify({'error': 'Unauthorized access to member data'}), 403
    
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    # Get week parameter or use current week
    date_str = request.args.get('date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    else:
        target_date = date.today()
    
    # Calculate start and end of week (Monday to Sunday)
    start_of_week = target_date - timedelta(days=target_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Calculate compliance for the week
    scheduled_doses = get_scheduled_doses(member_id, start_of_week, end_of_week, is_family_member)
    taken_doses = get_taken_doses(member_id, start_of_week, end_of_week, is_family_member)
    compliance_rate = calculate_compliance_rate(scheduled_doses, taken_doses)
    
    # Get daily breakdown
    daily_data = []
    current_date = start_of_week
    while current_date <= end_of_week:
        day_scheduled = get_scheduled_doses(member_id, current_date, current_date, is_family_member)
        day_taken = get_taken_doses(member_id, current_date, current_date, is_family_member)
        day_rate = calculate_compliance_rate(day_scheduled, day_taken)
        
        daily_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': current_date.strftime('%A'),
            'scheduled_doses': day_scheduled,
            'taken_doses': day_taken,
            'compliance_rate': round(day_rate, 2)
        })
        
        current_date += timedelta(days=1)
    
    return jsonify({
        'week_start': start_of_week.strftime('%Y-%m-%d'),
        'week_end': end_of_week.strftime('%Y-%m-%d'),
        'member_id': member_id,
        'member_name': family_member.name if is_family_member else member.username,
        'scheduled_doses': scheduled_doses,
        'taken_doses': taken_doses,
        'compliance_rate': round(compliance_rate, 2),
        'daily_breakdown': daily_data
    }), 200

# Get monthly compliance for a member
@compliance_bp.route('/monthly/<int:member_id>', methods=['GET'])
@jwt_required()
def monthly_compliance(member_id):
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    FamilyMember = current_app.config.get('FamilyMember')
    
    # Check if the member_id is for a family member or the user
    is_family_member = False
    member = None
    
    # First check if it's a family member
    family_member = FamilyMember.query.filter_by(id=member_id, user_id=current_user).first()
    if family_member:
        is_family_member = True
        member = family_member
    else:
        # If not a family member, check if it's the current user
        if member_id == current_user:
            member = User.query.get(current_user)
        else:
            return jsonify({'error': 'Unauthorized access to member data'}), 403
    
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    # Get month parameter or use current month
    month_str = request.args.get('month')
    year_str = request.args.get('year')
    
    if month_str and year_str:
        try:
            month = int(month_str)
            year = int(year_str)
            if month < 1 or month > 12:
                return jsonify({'error': 'Month must be between 1 and 12'}), 400
            # Create a date for the first day of the month
            start_of_month = date(year, month, 1)
        except ValueError:
            return jsonify({'error': 'Invalid month or year format'}), 400
    else:
        today = date.today()
        start_of_month = date(today.year, today.month, 1)
    
    # Calculate the last day of the month
    if start_of_month.month == 12:
        end_of_month = date(start_of_month.year + 1, 1, 1) - timedelta(days=1)
    else:
        end_of_month = date(start_of_month.year, start_of_month.month + 1, 1) - timedelta(days=1)
    
    # Calculate compliance for the month
    scheduled_doses = get_scheduled_doses(member_id, start_of_month, end_of_month, is_family_member)
    taken_doses = get_taken_doses(member_id, start_of_month, end_of_month, is_family_member)
    compliance_rate = calculate_compliance_rate(scheduled_doses, taken_doses)
    
    # Get weekly breakdown
    weekly_data = []
    current_date = start_of_month
    
    while current_date <= end_of_month:
        # Calculate start and end of week, but cap at month boundaries
        week_start = current_date - timedelta(days=current_date.weekday())
        if week_start < start_of_month:
            week_start = start_of_month
            
        week_end = week_start + timedelta(days=6)
        if week_end > end_of_month:
            week_end = end_of_month
        
        week_scheduled = get_scheduled_doses(member_id, week_start, week_end, is_family_member)
        week_taken = get_taken_doses(member_id, week_start, week_end, is_family_member)
        week_rate = calculate_compliance_rate(week_scheduled, week_taken)
        
        weekly_data.append({
            'week_start': week_start.strftime('%Y-%m-%d'),
            'week_end': week_end.strftime('%Y-%m-%d'),
            'scheduled_doses': week_scheduled,
            'taken_doses': week_taken,
            'compliance_rate': round(week_rate, 2)
        })
        
        # Move to the next week
        current_date = week_end + timedelta(days=1)
        if current_date > end_of_month:
            break
    
    return jsonify({
        'month': start_of_month.strftime('%B %Y'),
        'month_start': start_of_month.strftime('%Y-%m-%d'),
        'month_end': end_of_month.strftime('%Y-%m-%d'),
        'member_id': member_id,
        'member_name': family_member.name if is_family_member else member.username,
        'scheduled_doses': scheduled_doses,
        'taken_doses': taken_doses,
        'compliance_rate': round(compliance_rate, 2),
        'weekly_breakdown': weekly_data
    }), 200

# Get compliance leaderboard for a family
@compliance_bp.route('/leaderboard/<int:family_id>', methods=['GET'])
@jwt_required()
def compliance_leaderboard(family_id):
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    FamilyMember = current_app.config.get('FamilyMember')
    
    # Verify the user has access to this family
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if family_id is 0, which means the user's own family
    if family_id == 0:
        # Get all family members for the current user
        family_members = FamilyMember.query.filter_by(user_id=current_user).all()
    else:
        # For future expansion - could support multiple families
        return jsonify({'error': 'Invalid family ID'}), 400
    
    # Get time period parameter (default to weekly)
    period = request.args.get('period', 'weekly')
    
    if period not in ['daily', 'weekly', 'monthly']:
        return jsonify({'error': 'Invalid period. Use daily, weekly, or monthly'}), 400
    
    # Calculate date ranges based on period
    today = date.today()
    
    if period == 'daily':
        start_date = today
        end_date = today
    elif period == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    else:  # monthly
        start_date = date(today.year, today.month, 1)
        if today.month == 12:
            end_date = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(today.year, today.month + 1, 1) - timedelta(days=1)
    
    # Calculate compliance for each family member and the user
    leaderboard = []
    
    # Add user to leaderboard
    user_scheduled = get_scheduled_doses(current_user, start_date, end_date, False)
    user_taken = get_taken_doses(current_user, start_date, end_date, False)
    user_rate = calculate_compliance_rate(user_scheduled, user_taken)
    
    leaderboard.append({
        'member_id': current_user,
        'member_name': user.name,
        'is_user': True,
        'scheduled_doses': user_scheduled,
        'taken_doses': user_taken,
        'compliance_rate': round(user_rate, 2)
    })
    
    # Add family members to leaderboard
    for member in family_members:
        member_scheduled = get_scheduled_doses(member.id, start_date, end_date, True)
        member_taken = get_taken_doses(member.id, start_date, end_date, True)
        member_rate = calculate_compliance_rate(member_scheduled, member_taken)
        
        leaderboard.append({
            'member_id': member.id,
            'member_name': member.name,
            'is_user': False,
            'scheduled_doses': member_scheduled,
            'taken_doses': member_taken,
            'compliance_rate': round(member_rate, 2)
        })
    
    # Sort leaderboard by compliance rate (descending)
    leaderboard.sort(key=lambda x: x['compliance_rate'], reverse=True)
    
    # Add rank to each entry
    for i, entry in enumerate(leaderboard):
        entry['rank'] = i + 1
    
    return jsonify({
        'period': period,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'leaderboard': leaderboard
    }), 200

# Export compliance report
@compliance_bp.route('/export-report', methods=['POST'])
@jwt_required()
def export_report():
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    FamilyMember = current_app.config.get('FamilyMember')
    
    # Get request parameters
    data = request.get_json()
    member_id = data.get('member_id')
    period = data.get('period', 'monthly')
    format_type = data.get('format', 'csv')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    
    # Validate parameters
    if not member_id:
        return jsonify({'error': 'Member ID is required'}), 400
    
    if period not in ['daily', 'weekly', 'monthly', 'custom']:
        return jsonify({'error': 'Invalid period. Use daily, weekly, monthly, or custom'}), 400
    
    if format_type not in ['csv', 'json']:
        return jsonify({'error': 'Invalid format. Use csv or json'}), 400
    
    # Check if the member_id is for a family member or the user
    is_family_member = False
    member = None
    
    # First check if it's a family member
    family_member = FamilyMember.query.filter_by(id=member_id, user_id=current_user).first()
    if family_member:
        is_family_member = True
        member = family_member
    else:
        # If not a family member, check if it's the current user
        if int(member_id) == current_user:
            member = User.query.get(current_user)
        else:
            return jsonify({'error': 'Unauthorized access to member data'}), 403
    
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    # Calculate date range based on period
    today = date.today()
    
    if period == 'custom':
        if not start_date_str or not end_date_str:
            return jsonify({'error': 'Start date and end date are required for custom period'}), 400
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            if start_date > end_date:
                return jsonify({'error': 'Start date must be before end date'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    elif period == 'daily':
        start_date = today
        end_date = today
    elif period == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    else:  # monthly
        start_date = date(today.year, today.month, 1)
        if today.month == 12:
            end_date = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(today.year, today.month + 1, 1) - timedelta(days=1)
    
    # Generate report data
    report_data = []
    current_date = start_date
    
    while current_date <= end_date:
        day_scheduled = get_scheduled_doses(member_id, current_date, current_date, is_family_member)
        day_taken = get_taken_doses(member_id, current_date, current_date, is_family_member)
        day_rate = calculate_compliance_rate(day_scheduled, day_taken)
        
        report_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day_of_week': current_date.strftime('%A'),
            'scheduled_doses': day_scheduled,
            'taken_doses': day_taken,
            'compliance_rate': round(day_rate, 2)
        })
        
        current_date += timedelta(days=1)
    
    # Calculate overall compliance
    total_scheduled = sum(day['scheduled_doses'] for day in report_data)
    total_taken = sum(day['taken_doses'] for day in report_data)
    overall_rate = calculate_compliance_rate(total_scheduled, total_taken)
    
    # Generate report in requested format
    if format_type == 'csv':
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Compliance Report'])
        writer.writerow(['Member:', family_member.name if is_family_member else member.name])
        writer.writerow(['Period:', period])
        writer.writerow(['Date Range:', f'{start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}'])
        writer.writerow(['Overall Compliance Rate:', f'{round(overall_rate, 2)}%'])
        writer.writerow(['Total Scheduled Doses:', total_scheduled])
        writer.writerow(['Total Taken Doses:', total_taken])
        writer.writerow([])
        
        # Write data header
        writer.writerow(['Date', 'Day of Week', 'Scheduled Doses', 'Taken Doses', 'Compliance Rate (%)'])
        
        # Write data rows
        for day in report_data:
            writer.writerow([
                day['date'],
                day['day_of_week'],
                day['scheduled_doses'],
                day['taken_doses'],
                day['compliance_rate']
            ])
        
        # Prepare response
        output.seek(0)
        member_name = family_member.name if is_family_member else member.username
        filename = f"compliance_report_{member_name.replace(' ', '_')}_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
        
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    else:  # json
        # Prepare JSON response
        report = {
            'member': {
                'id': member_id,
                'name': family_member.name if is_family_member else member.username,
                'is_user': not is_family_member
            },
            'period': period,
            'date_range': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            },
            'overall': {
                'scheduled_doses': total_scheduled,
                'taken_doses': total_taken,
                'compliance_rate': round(overall_rate, 2)
            },
            'daily_data': report_data
        }
        
        return jsonify(report), 200

# Get missed doses for a member
@compliance_bp.route('/missed-doses/<int:member_id>', methods=['GET'])
@jwt_required()
def missed_doses(member_id):
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    FamilyMember = current_app.config.get('FamilyMember')
    Supplement = current_app.config.get('Supplement')
    Reminder = current_app.config.get('Reminder')
    SupplementIntake = current_app.config.get('SupplementIntake')
    
    # Check if the member_id is for a family member or the user
    is_family_member = False
    member = None
    
    # First check if it's a family member
    family_member = FamilyMember.query.filter_by(id=member_id, user_id=current_user).first()
    if family_member:
        is_family_member = True
        member = family_member
    else:
        # If not a family member, check if it's the current user
        if member_id == current_user:
            member = User.query.get(current_user)
        else:
            return jsonify({'error': 'Unauthorized access to member data'}), 403
    
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    # Get date range parameters (default to last 7 days)
    days = request.args.get('days', 7, type=int)
    if days < 1 or days > 90:
        return jsonify({'error': 'Days parameter must be between 1 and 90'}), 400
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)  # inclusive of today
    
    # Get all active reminders for the member
    reminder_query = Reminder.query.filter(Reminder.active == True)
    
    if is_family_member:
        reminder_query = reminder_query.filter(Reminder.family_member_id == member_id)
    else:
        reminder_query = reminder_query.filter(Reminder.user_id == member_id, Reminder.family_member_id == None)
    
    reminders = reminder_query.all()
    
    # Get all intakes for the member in the date range
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    intake_query = SupplementIntake.query.filter(
        SupplementIntake.taken_at >= start_datetime,
        SupplementIntake.taken_at <= end_datetime
    )
    
    if is_family_member:
        intake_query = intake_query.filter(SupplementIntake.family_member_id == member_id)
    else:
        intake_query = intake_query.filter(SupplementIntake.user_id == member_id, SupplementIntake.family_member_id == None)
    
    intakes = intake_query.all()
    
    # Create a lookup of supplement_id -> taken_dates
    taken_supplements = {}
    for intake in intakes:
        taken_date = intake.taken_at.date()
        if intake.supplement_id not in taken_supplements:
            taken_supplements[intake.supplement_id] = []
        taken_supplements[intake.supplement_id].append(taken_date)
    
    # Calculate missed doses
    missed_doses = []
    current_date = start_date
    
    while current_date <= end_date:
        day_name = current_date.strftime('%A')
        
        for reminder in reminders:
            # Check if this day is scheduled in the reminder
            if day_name in reminder.days.split(','):
                supplement = Supplement.query.get(reminder.supplement_id)
                
                # Check if the supplement was taken on this date
                was_taken = False
                if reminder.supplement_id in taken_supplements:
                    if current_date in taken_supplements[reminder.supplement_id]:
                        was_taken = True
                
                if not was_taken:
                    missed_doses.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'day_of_week': day_name,
                        'supplement_id': reminder.supplement_id,
                        'supplement_name': supplement.name if supplement else 'Unknown',
                        'scheduled_time': reminder.time.strftime('%H:%M') if reminder.time else 'Unknown'
                    })
        
        current_date += timedelta(days=1)
    
    # Sort missed doses by date (most recent first)
    missed_doses.sort(key=lambda x: x['date'], reverse=True)
    
    return jsonify({
        'member_id': member_id,
        'member_name': family_member.name if is_family_member else member.username,
        'date_range': {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'days': days
        },
        'missed_doses_count': len(missed_doses),
        'missed_doses': missed_doses
    }), 200