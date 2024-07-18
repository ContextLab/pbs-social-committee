
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
msg['Subject'] = "Weekly Wednesday Woccoms Reminder"

body = """<p>Hi Michelle,</p>
<p>Could you please send out the announcement below to the department?</p>
<p>Thanks very much!</p>
<p>Best,
The PBS Social Committee</p>
<p>===BEGIN===
PBS Social Committee Calendar of Events</p>
<p>Weekly Wednesday Woccoms 🚶🌲🌳</p>
<p>That computer screen can wait!  Step away from your desk and join us for a walk around Occom Pond. Extend your lab meeting, problem-solve, or simply enjoy the fresh air with colleagues.</p>
<p><strong>Date:</strong> {DATE}
<strong>Time:</strong> {TIME}
<strong>Location:</strong> {LOCATION}</p>
<p>Looking forward to walking with you!</p>
<p>Best,
The PBS Social Committee</p>
<p>===END===</p>"""
msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, os.getenv('GMAIL_PASSWORD'))
text = msg.as_string()
server.sendmail(sender_email, admin_emails + organizer_emails, text)
server.quit()
