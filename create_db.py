from app.web.app import create_app, db

app = create_app()
app.app_context().push()

db.create_all()

print("Database created successfully.")