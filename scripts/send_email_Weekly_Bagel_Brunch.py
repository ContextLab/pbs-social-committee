
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown

# Load email addresses
emails_df = pd.read_csv('email_addresses.csv')
sender_email = emails_df[emails_df['Role'] == 'Sender']['Email address'].iloc[0]
admin_emails = emails_df[emails_df['Role'] == 'Admin']['Email address'].tolist()
organizer_emails = emails_df[emails_df['Role'] == 'Organizer']['Email address'].tolist()
admin_emails_str = ', '.join(admin_emails)
organizer_emails_str = ', '.join(organizer_emails)

# Load event details
events_df = pd.read_csv('events.tsv', delimiter='\t')
event = events_df[events_df['Event Name'] == 'Weekly Bagel Brunch'].iloc[0]
event_name = event['Event Name']
date = event['Date']
time = event['Time']
location = event['Location']
content_file = event['Content File']

# Email content
with open(f'templates/{content_file}', 'r') as file:
    email_content = file.read()
email_content = email_content.replace('{DATE}', date).replace('{TIME}', time).replace('{LOCATION}', location)
email_content_html = markdown.markdown(email_content)

# Create email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ', '.join(admin_emails)
msg['Cc'] = ', '.join(organizer_emails)
msg['Subject'] = f'Weekly Bagel Brunch Reminder'

body = f"""{email_content_html}"""
msg.attach(MIMEText(body, 'html'))

# Send email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, "${ secrets.GMAIL_PASSWORD }")
text = msg.as_string()
server.sendmail(sender_email, admin_emails + organizer_emails, text)
server.quit()
