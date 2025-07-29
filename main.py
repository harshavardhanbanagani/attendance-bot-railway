import os

username = os.getenv("MITS_USERNAME")
password = os.getenv("MITS_PASSWORD")
email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = os.getenv("EMAIL_RECEIVER")

# Dummy logic for now - replace with actual attendance logic
print(f"Logging in as {username}...")
print("Fetching attendance...")
print("Sending email to", email_receiver)
