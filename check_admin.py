from main import create_app

app = create_app()
User = app.config['User']
with app.app_context():
    admin_count = User.query.filter_by(role='admin').count()
    print(f'Number of admin users: {admin_count}')