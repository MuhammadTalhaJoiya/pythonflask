from flask import Blueprint

test_bp = Blueprint('test', __name__)

@test_bp.route('/')
def test_route():
    return {'message': 'Test blueprint is working!'}