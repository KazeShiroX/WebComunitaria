from app import create_app
from models import db, Usuario

app = create_app()

with app.app_context():
    try:
        users = Usuario.query.all()
        print(f"Found {len(users)} users:")
        for u in users:
            print(f"- {u.email} ({u.rol})")
    except Exception as e:
        print(f"Error querying users: {e}")
