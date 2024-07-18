import pandas as pd
import subprocess

# Load events
events_df = pd.read_csv('events.tsv', delimiter='\t')

# Generate events calendar in Markdown format
events_markdown = "# PBS Social Committee Calendar of Events\nWinter, 2024*\n\nAfter a brief hiatus, we’ve put together another exciting term for you! Here’s our schedule of events this term.\n\n"
for _, row in events_df.iterrows():
    with open(f'templates/{row["Content File"]}', 'r') as file:
        event_content = file.read()
    
    # Replace placeholders with actual values
    event_content = event_content.replace('{DATE}', row['Date']).replace('{TIME}', row['Time']).replace('{LOCATION}', row['Location'])
    
    events_markdown += f"## {row['Event Name']}\n\n"
    events_markdown += event_content + "\n\n"
    events_markdown += "---\n\n"

# Save the events markdown to a file
with open('events_schedule.md', 'w') as file:
    file.write(events_markdown.strip())

# Convert the Markdown file to PDF using Pandoc
subprocess.run(['pandoc', 'events_schedule.md', '-o', 'events_schedule.pdf'])
