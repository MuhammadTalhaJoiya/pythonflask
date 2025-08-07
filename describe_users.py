from main import create_app, db
import sqlalchemy as sa

app = create_app()
with app.app_context():
    with db.engine.connect() as connection:
        result = connection.execute(sa.text("SHOW COLUMNS FROM users"))
        columns = [row[0] for row in result]
        print('Columns in users table:', columns)