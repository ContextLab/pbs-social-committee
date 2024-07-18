import pandas as pd
import yaml
from datetime import datetime, timedelta
import os
import markdown

# Create the scripts directory if it doesn't exist
os.makedirs('scripts', exist_ok=True)

# Load events.tsv and email_addresses.csv
events_df = pd.read_csv('events.tsv', delimiter='\t')
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

# Function to create event reminder scripts
def create_event_script(event_name, date_str, content_file, frequency, day_of_week, date, time, location):
    event_date = datetime.strptime(date_str, '%Y-%m-%d')
    trigger_time = (event_date - timedelta(days=1)).strftime('%Y-%m-%dT14:00:00Z') # 9 AM ET is 14:00 UTC

    # Email content
    with open(f'templates/{content_file}', 'r') as file:
        email_content = file.read()

    email_content = email_content.replace('{{DATE}}', date + '\n\n').replace('{{TIME}}', time + '\n\n').replace('{{LOCATION}}', location)

    # Insert event content into admin template
    full_content = admin_template.replace('===BEGIN===', '===BEGIN===\n\n' + email_content)

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
password = os.getenv('GMAIL_PASSWORD')
if password is None:
    raise ValueError("GMAIL_PASSWORD environment variable not set")
server.login(sender_email, password)
text = msg.as_string()
server.sendmail(sender_email, admin_emails + organizer_emails, text)
server.quit()
"""

    script_path = f'scripts/send_email_{event_name.replace(" ", "_")}.py'
    print(f"Creating script at {script_path}")
    with open(script_path, 'w') as file:
        file.write(script_content)

    # Generate appropriate cron time
    cron_time = f'{event_date.minute} {event_date.hour} {event_date.day} {event_date.month} *'

    # Create the workflow for the event
    workflow_content = {
        'name': f'Reminder for {event_name}',
        'on': {
            'workflow_dispatch': {},
            'schedule': [
                {'cron': cron_time}  # Set the cron time
            ]
        },
        'jobs': {
            'send_email': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'name': 'Checkout repository', 'uses': 'actions/checkout@v2'},
                    {'name': 'Set up Python', 'uses': 'actions/setup-python@v2', 'with': {'python-version': '3.x'}},
                    {'name': 'Install dependencies', 'run': 'pip install pandas markdown'},
                    {'name': 'Run email script', 'run': f'python scripts/send_email_{event_name.replace(" ", "_")}.py', 'env': {'GMAIL_PASSWORD': '${{ secrets.GMAIL_PASSWORD }}'}}
                ]
            }
        }
    }

    workflow_path = f'.github/workflows/reminder_{event_name.replace(" ", "_")}.yml'
    print(f"Creating workflow at {workflow_path}")
    with open(workflow_path, 'w') as file:
        yaml.dump(workflow_content, file)

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
