import pandas as pd
import yaml
from datetime import datetime, timedelta
import os
import markdown

# Load events and email addresses
events_df = pd.read_csv('events.tsv', delimiter='\t')
emails_df = pd.read_csv('email_addresses.csv')

# Filter email addresses
sender_email = emails_df[emails_df['Role'] == 'Sender']['Email address'].iloc[0]
admin_emails = emails_df[emails_df['Role'] == 'Admin']['Email address'].tolist()
organizer_emails = emails_df[emails_df['Role'] == 'Organizer']['Email address'].tolist()
admin_emails_str = ', '.join(admin_emails)
organizer_emails_str = ', '.join(organizer_emails)

# Function to create event reminder scripts
def create_event_script(event_name, date_str, content, frequency, day_of_week, date, time, location):
    event_date = datetime.strptime(date_str, '%Y-%m-%d')
    trigger_time = (event_date - timedelta(days=1)).strftime('%Y-%m-%dT14:00:00Z') # 9 AM ET is 14:00 UTC

    # Email content
    with open(f'templates/{content}', 'r') as file:
        email_content = file.read()

    # Replace placeholders with actual values
    email_content = email_content.replace('{DATE}', date).replace('{TIME}', time).replace('{LOCATION}', location)

    # Read admin.md template
    with open('templates/admin.md', 'r') as file:
        admin_template = file.read()

    # Insert event content into admin template
    announcement_content = admin_template.replace('===BEGIN===', '===BEGIN===\n' + email_content).replace('===END===', '\n===END===')

    # Convert markdown to HTML
    html_content = markdown.markdown(email_content)

    # Email script with HTML content
    email_script = f"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "{sender_email}"
receiver_email = "{admin_emails_str}"
cc_email = "{organizer_emails_str}"
subject = "{event_name} Reminder"

msg = MIMEMultipart("alternative")
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Cc'] = cc_email
msg['Subject'] = subject

text = \"\"\"{announcement_content}\"\"\"
html = \"\"\"<html><body>{html_content}</body></html>\"\"\"

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

msg.attach(part1)
msg.attach(part2)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, "${{ secrets.GMAIL_PASSWORD }}")
text = msg.as_string()
server.sendmail(sender_email, receiver_email.split(", ") + cc_email.split(", "), text)
server.quit()
"""

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
                    {'name': 'Send email', 'run': f'python - <<EOF\n{email_script}\nEOF'}
                ]
            }
        }
    }

    # Write action script to file
    with open(f'.github/workflows/reminder_{event_name}.yml', 'w') as file:
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
