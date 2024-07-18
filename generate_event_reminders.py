import pandas as pd
import yaml
from datetime import datetime, timedelta
import os
import markdown

# Load events.csv and email_addresses.csv
events_df = pd.read_csv('events.csv')
emails_df = pd.read_csv('email_addresses.csv')

# Extract email addresses
sender_email = emails_df[emails_df['Role'] == 'Sender']['Email address'].iloc[0]
admin_emails = emails_df[emails_df['Role'] == 'Admin']['Email address'].tolist()
organizer_emails = emails_df[emails_df['Role'] == 'Organizer']['Email address'].tolist()

admin_emails_str = ', '.join(admin_emails)
organizer_emails_str = ', '.join(organizer_emails)

# Load the email script template
with open('templates/admin.md', 'r') as file:
    admin_template = file.read()

# Load the email content templates
event_templates = {}
for event_name in events_df['Event Name']:
    with open(f'templates/{event_name.replace(" ", "_")}.md', 'r') as file:
        event_templates[event_name] = file.read()

# Function to create event reminder scripts
def create_event_script(event_name, date_str, content_file, frequency, day_of_week, date, time, location):
    event_date = datetime.strptime(date_str, '%Y-%m-%d')
    trigger_time = (event_date - timedelta(days=1)).strftime('%Y-%m-%dT14:00:00Z') # 9 AM ET is 14:00 UTC

    # Email content
    email_content = event_templates[event_name].replace('{{DATE}}', date + '\n').replace('{{TIME}}', time + '\n').replace('{{LOCATION}}', location)

    # Insert event content into admin template
    full_content = admin_template.replace('===BEGIN===', '===BEGIN===\n' + email_content).replace('===END===', '\n===END===')

    # Convert the full email content to HTML
    full_content_html = markdown.markdown(full_content)

    # Write the script
    script_content = f"""
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
msg['Subject'] = "{event_name} Reminder"

body = \"\"\"{full_content_html}\"\"\"
msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, os.getenv('GMAIL_PASSWORD'))
text = msg.as_string()
server.sendmail(sender_email, admin_emails + organizer_emails, text)
server.quit()
"""

    with open(f'scripts/send_email_{event_name.replace(" ", "_")}.py', 'w') as file:
        file.write(script_content)

# Generate scripts for each event
for _, row in events_df.iterrows():
    event_name = row['Event Name']
    start_date = row['Start Date']
    frequency = row['Frequency']
    content_file = row['Content File']
    date = row['Date']
    time = row['Time']
    location = row['Location']

    if frequency == 'O' or pd.isna(frequency):
        create_event_script(event_name, start_date, content_file, 'one-time', None, date, time, location)
    elif frequency.startswith('W-'):
        day_of_week = frequency.split('-')[1]
        create_event_script(event_name, start_date, content_file, 'weekly', day_of_week, date, time, location)
    elif frequency == 'M':
        create_event_script(event_name, start_date, content_file, 'monthly', None, date, time, location)
