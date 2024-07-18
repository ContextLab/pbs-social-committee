
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import pandas as pd

# Load email addresses
emails_df = pd.read_csv('email_addresses.csv')
sender_email = emails_df[emails_df['Role'] == 'Sender']['Email address'].iloc[0]
admin_emails = emails_df[emails_df['Role'] == 'Admin']['Email address'].tolist()
organizer_emails = emails_df[emails_df['Role'] == 'Organizer']['Email address'].tolist()
admin_emails_str = ', '.join(admin_emails)
organizer_emails_str = ', '.join(organizer_emails)

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = admin_emails_str
msg['Cc'] = organizer_emails_str
msg['Subject'] = "Winter Holiday Party Reminder"

body = """<p>Hi Michelle,</p>
<p>Could you please send out the announcement below to the department?</p>
<p>Thanks very much!</p>
<p>Best,<br />
The PBS Social Committee</p>
<p>===BEGIN===</p>
<p>PBS Social Committee Calendar of Events</p>
<p>Winter Holiday Party 🎉❄️⛄🤹</p>
<p>Join us for our Winter Holiday Party! Celebrate the season with colleagues, friends, and family.</p>
<p><strong>Date:</strong> Mid-December<br />
<strong>Time:</strong> TBD<br />
<strong>Location:</strong> TBD</p>
<p>Let's spread some holiday cheer!</p>
<p>Best,<br />
The PBS Social Committee</p>
<p>===END===</p>"""
msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
password = os.getenv('GMAIL_PASSWORD')
if password is None:
    raise ValueError("GMAIL_PASSWORD environment variable not set")
server.login(sender_email, password)
text = msg.as_string()
server.sendmail(sender_email, admin_emails + organizer_emails, text)
server.quit()
