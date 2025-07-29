import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load credentials from environment
USERNAME = os.getenv("MITS_USERNAME")
PASSWORD = os.getenv("MITS_PASSWORD")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def fetch_attendance():
    login_url = "http://mitsims.in/loginverify.jsp"
    attendance_url = "http://mitsims.in/studattendance.jsp"

    with requests.Session() as session:
        payload = {
            "userid": USERNAME,
            "password": PASSWORD
        }

        # Step 1: Login
        login_response = session.post(login_url, data=payload)
        if "Invalid" in login_response.text or "login" in login_response.url:
            raise Exception("Login failed. Check credentials.")

        # Step 2: Access attendance page
        attendance_page = session.get(attendance_url)
        soup = BeautifulSoup(attendance_page.content, "html.parser")
        tables = soup.find_all("table")

        # Step 3: Parse total attendance
        if len(tables) < 2:
            raise Exception("Attendance table not found.")
        
        summary_table = tables[-1]
        total_row = summary_table.find_all("tr")[-1]
        cells = total_row.find_all("td")
        subject_total = cells[2].text.strip()  # Assuming Total Attendance %

        return subject_total

def send_email(attendance):
    subject = "🎓 MITS Attendance Alert"
    body = f"Hi,\n\nYour total attendance is: {attendance}%\n\n– Automated Reminder"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    print("✅ Email sent!")

if __name__ == "__main__":
    try:
        attendance = fetch_attendance()
        send_email(attendance)
    except Exception as e:
        print(f"❌ Error: {e}")
