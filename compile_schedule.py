import pandas as pd
import subprocess
import os
from datetime import datetime
import re

# Determine the term and year
def get_term_and_year(start_date):
    date = datetime.strptime(start_date, "%Y-%m-%d")
    year = date.year
    if date.month in [1, 2, 3]:
        term = "Winter"
    elif date.month in [4, 5, 6]:
        term = "Spring"
    elif date.month in [7, 8, 9]:
        term = "Summer"
    else:
        term = "Fall"
    return term, year

# Emoji mapping
emoji_mapping = {
    "🍷": "wine-glass",
    "🧀": "cheese-wedge",
    "🚶": "walking",
    "🌲": "evergreen-tree",
    "🌳": "deciduous-tree",
    "🍵": "tea",
    "🍪": "cookie",
    "🥯": "bagel",
    "☕️": "coffee",
    "🎉": "tada",
    "🎃": "jack-o-lantern",
    "🎲": "game-die"
}

def replace_emojis(text):
    def replace(match):
        emoji = match.group(0)
        return f"\\emoji{{{emoji_mapping.get(emoji, '')}}}"
    
    # Use regex to find emojis
    emoji_pattern = re.compile('|'.join(re.escape(key) for key in emoji_mapping.keys()))
    return emoji_pattern.sub(replace, text)

# Load events
events_df = pd.read_csv('events.tsv', delimiter='\t')
start_date = events_df.iloc[0]['Start Date']
term, year = get_term_and_year(start_date)

# Generate events calendar in Markdown format
events_markdown = f"# PBS Social Committee Calendar of Events\n{term}, {year}\n\nHere’s our schedule of events this term.\n\n"
for _, row in events_df.iterrows():
    content_file = row["Content File"]
    if pd.isna(content_file) or not os.path.exists(f'templates/{content_file}'):
        print(f"Warning: Content file for '{row['Event Name']}' is missing or incorrect.")
        continue
    
    with open(f'templates/{content_file}', 'r') as file:
        event_content = file.read()

    # Replace placeholders with actual values
    event_content = event_content.replace('{DATE}', row['Date']).replace('{TIME}', row['Time']).replace('{LOCATION}', row['Location'])
    
    # Remove the first and last lines
    event_content_lines = event_content.split('\n')
    event_content = '\n'.join(event_content_lines[1:-1]).strip()
    
    # Adjust formatting for Date, Time, Location
    event_content = event_content.replace('Date:', '\nDate:')
    event_content = event_content.replace('Time:', '\nTime:')
    event_content = event_content.replace('Location:', '\nLocation:')
    
    # Replace emojis
    event_content = replace_emojis(event_content)
    
    events_markdown += f"## {row['Event Name']}\n\n"
    events_markdown += event_content + "\n\n"
    events_markdown += "---\n\n"

# Save the events markdown to a file
with open('events_schedule.md', 'w') as file:
    file.write(events_markdown.strip())

# Set TEXINPUTS environment variable to include the latex directory
env = os.environ.copy()
env['TEXINPUTS'] = './/latex//:'

# Convert the Markdown file to PDF using Pandoc with LuaLaTeX and Poppins font
subprocess.run([
    'pandoc', 'events_schedule.md', '-o', 'events_schedule.pdf', 
    '--pdf-engine=lualatex', 
    '--include-in-header=latex_header.tex', 
    '--variable', 'geometry:margin=1in',
    '--variable', 'fontsize=12pt'
], env=env)
