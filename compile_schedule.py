import pandas as pd
import subprocess
import os
from datetime import datetime
import re
import csv

# Function to convert unicode code points to actual emoji characters
def unicode_to_emoji(unicode_str):
    codes = unicode_str.split()
    return ''.join(chr(int(code.lstrip('U+'), 16)) for code in codes)

# Function to load emoji mapping from CSV
def load_emoji_mapping(csv_file):
    emoji_mapping = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            emoji = unicode_to_emoji(row['Emoji'])
            emoji_mapping[emoji] = row['Name']
    return emoji_mapping

# Load emoji mapping
emoji_mapping = load_emoji_mapping('emoji_mapping.csv')

# Determine the term and year
def get_term_and_year(start_date):
    date = datetime.strptime(start_date, "%Y-%m-%d")
    year = date.year
    if (date.month == 8 and date.day >= 24) or date.month in [9, 10, 11] or (date.month == 12 and date.day <= 31):
        term = "Fall"
    elif date.month in [1, 2] or (date.month == 3 and date.day <= 15):
        term = "Winter"
    elif (date.month == 3 and date.day >= 24) or date.month in [4, 5] or (date.month == 6 and date.day <= 7):
        term = "Spring"
    else:
        term = "Summer"
    return term, year

def replace_emojis(text):
    def replace(match):
        emoji = match.group(0)
        latex_name = emoji_mapping.get(emoji, '')
        return f"\\emoji{{{latex_name}}}" if latex_name else emoji
    
    # Use regex to find emojis
    emoji_pattern = re.compile('|'.join(re.escape(key) for key in emoji_mapping.keys()))
    return emoji_pattern.sub(replace, text)

def remove_last_lines(lines, n):
    count = 0
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() != '':
            count += 1
            if count == n:
                return lines[:i]
    return lines

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
        event_content = file.readlines()

    # Extract event title from the second non-whitespace line
    non_whitespace_lines = [line.strip() for line in event_content if line.strip()]
    event_title = non_whitespace_lines[1] if len(non_whitespace_lines) > 1 else row["Event Name"]

    # Remove the first line (title) and the last two non-whitespace lines
    event_content = remove_last_lines(event_content, 2)[1:]

    # Replace placeholders with actual values
    event_content = ''.join(event_content).replace('{DATE}', row['Date']).replace('{TIME}', row['Time']).replace('{LOCATION}', row['Location'])
    
    # Adjust formatting for Date, Time, Location
    event_content = event_content.replace('**Date:**', '\n**Date:**')
    event_content = event_content.replace('**Time:**', '\n**Time:**')
    event_content = event_content.replace('**Location:**', '\n**Location:**')
    
    # Replace emojis
    event_title = replace_emojis(event_title)
    event_content = replace_emojis(event_content)
    
    events_markdown += f"## {event_title}\n\n"
    events_markdown += event_content + "\n\n"
    events_markdown += "---\n\n"

# Save the events markdown to a file
with open('events_schedule.md', 'w') as file:
    file.write(events_markdown.strip())

# Set TEXINPUTS environment variable to include the latex directory
env = os.environ.copy()
env['TEXINPUTS'] = './/latex//:'

# Convert the Markdown file to PDF using Pandoc with LuaLaTeX and Merriweather font
subprocess.run([
    'pandoc', 'events_schedule.md', '-o', 'events_schedule.pdf', 
    '--pdf-engine=lualatex', 
    '--include-in-header=latex_header.tex', 
    '--variable', 'geometry:margin=1in',
    '--variable', 'fontsize=12pt'
], env=env)
