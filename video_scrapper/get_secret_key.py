import secrets

secret_key = secrets.token_hex(16)
print(f"Generated new secret key: {secret_key}")
print("Please add it to your .env file as FLASK_SECRET_KEY for consistency.")
