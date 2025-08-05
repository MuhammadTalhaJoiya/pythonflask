# D:\backendflask\project-root\run.py
from main import create_app

if __name__ == '__main__':
    app = create_app()  # Explicitly create the app instance
    app.run(debug=True)