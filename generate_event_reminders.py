import pandas as pd
import yaml
from datetime import datetime, timedelta

# Load TSV files
events_df = pd.read_csv('events.tsv', delimiter='\t')
emails_df = pd.read_csv('email_addresses.csv')

# Filter email addresses
sender_email = emails_df[emails_df['Role'] == 'Sender']['Email address'].iloc[0]
admin_emails = emails_df[emails_df['Role'] == 'Admin']['Email address'].tolist()
organizer_emails = emails_df[emails_df['Role'] == 'Organizer']['Email address'].tolist()
admin_emails_str = ', '.join(admin_emails)
organizer_emails_str = ', '.join(organizer_emails)

# Load email script template
with open('templates/send_email_template.py', 'r') as file:
    email_script_template = file.read()

# Function to create event reminder scripts
def create_event_script(event_name, date_str, content, frequency, day_of_week, date, time, location):
    event_date = datetime.strptime(date_str, '%Y-%m-%d')
    trigger_time = event_date - timedelta(days=1)  # 1 day before the event

    # Convert trigger time to cron syntax
    cron_schedule = f"{trigger_time.minute} {trigger_time.hour} {trigger_time.day} {trigger_time.month} *"

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

    # Replace placeholders in the email script template
    email_script = email_script_template.replace('{sender_email}', sender_email).replace('{admin_emails_str}', admin_emails_str).replace('{organizer_emails_str}', organizer_emails_str).replace('{event_name}', event_name).replace('{announcement_content}', announcement_content).replace('{password}', "${{ secrets.GMAIL_PASSWORD }}")

    # Create GitHub Action YAML
    action_script = {
        'name': f'Reminder for {event_name}',
        'on': {
            'schedule': [
                {'cron': cron_schedule}
            ]
        },
        'jobs': {
            'send_email': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'name': 'Checkout repository', 'uses': 'actions/checkout@v2'},
                    {'name': 'Set up Python', 'uses': 'actions/setup-python@v2', 'with': {'python-version': '3.x'}},
                    {'name': 'Install dependencies', 'run': 'pip install smtplib email'},
                    {'name': 'Send email', 'run': f'python - <<EOF\n{email_script}\nEOF'}
                ]
            }
        }
    }

    # Write action script to file
    with open(f'.github/workflows/reminder_{event_name.replace(" ", "_")}.yml', 'w') as file:
        yaml.dump(action_script, file)

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
