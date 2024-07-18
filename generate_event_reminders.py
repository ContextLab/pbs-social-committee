import os
import pandas as pd
import yaml
from datetime import datetime, timedelta

# Create the scripts directory if it doesn't exist
if not os.path.exists('scripts'):
    os.makedirs('scripts')

# Load TSV files
events_df = pd.read_csv('events.tsv', delimiter='\t')
emails_df = pd.read_csv('email_addresses.csv')

# Function to create valid cron expressions
def get_cron_expression(event_date):
    dt = datetime.strptime(event_date, '%Y-%m-%d')
    # Set the cron job to run at 9 AM UTC the day before the event
    cron_expression = f"0 9 {dt.day - 1} {dt.month} *"
    return cron_expression

# Function to create event reminder scripts
def create_event_script(event_name, date_str, content, frequency, day_of_week, date, time, location):
    event_date = datetime.strptime(date_str, '%Y-%m-%d')
    trigger_time = get_cron_expression(date_str)

    # Create the event-specific script
    script_content = f"""
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
events_df = pd.read_csv('events.tsv', delimiter='\\t')
event = events_df[events_df['Event Name'] == '{event_name}'].iloc[0]
event_name = event['Event Name']
date = event['Date']
time = event['Time']
location = event['Location']
content_file = event['Content File']

# Email content
with open(f'templates/{{content_file}}', 'r') as file:
    email_content = file.read()
email_content = email_content.replace('{{DATE}}', date).replace('{{TIME}}', time).replace('{{LOCATION}}', location)
email_content_html = markdown.markdown(email_content)

# Create email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ', '.join(admin_emails)
msg['Cc'] = ', '.join(organizer_emails)
msg['Subject'] = f'{event_name} Reminder'

body = f\"""{{email_content_html}}\"""
msg.attach(MIMEText(body, 'html'))

# Send email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, "${{ secrets.GMAIL_PASSWORD }}")
text = msg.as_string()
server.sendmail(sender_email, admin_emails + organizer_emails, text)
server.quit()
"""

    with open(f'scripts/send_email_{event_name.replace(" ", "_")}.py', 'w') as file:
        file.write(script_content)

    # Create GitHub Action YAML
    action_script = {
        'name': f'Reminder for {event_name}',
        'on': {
            'workflow_dispatch': {},
            'schedule': [
                {'cron': trigger_time}
            ]
        },
        'jobs': {
            'send_email': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'name': 'Checkout repository', 'uses': 'actions/checkout@v2'},
                    {'name': 'Set up Python', 'uses': 'actions/setup-python@v2', 'with': {'python-version': '3.x'}},
                    {'name': 'Install dependencies', 'run': 'pip install pandas markdown'},
                    {'name': 'Run email script', 'run': f'python scripts/send_email_{event_name.replace(" ", "_")}.py'}
                ]
            }
        }
    }

    with open(f'.github/workflows/reminder_{event_name.replace(" ", "_")}.yml', 'w') as file:
        yaml.dump(action_script, file, sort_keys=False)

# Process each event
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
