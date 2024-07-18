# 🤖 One-stop Automation for the PBS Social Committee!
Credit: [ChatGPT](https://chatgpt.com/)!

Isn't being "social" annoying? With this repository, *you can automate away the annoyances*!

Welcome to the ultimate automation hub for the PBS Social Committee! Say goodbye to tedious manual tasks and hello to streamlined, automated processes. This repository has everything you need to manage event reminders and announcements effortlessly.

## 📑 Table of Contents

1. [Features](#-features)
2. [How It Works](#-how-it-works)
3. [Setup](#-setup)
4. [Usage](#-usage)
   - [Launch Event Reminders](#launch-event-reminders)
   - [Pause Event Reminders](#pause-event-reminders)
   - [Compile Schedule](#compile-schedule)
5. [Starting a New Term](#-starting-a-new-term)
6. [Finishing Out a Term](#-finishing-out-a-term)
7. [Updating Committee Membership](#-updating-committee-membership)
8. [Adding or Modifying Events](#-adding-or-modifying-events)
9. [Repository Organization](#repository-organization)
10. [Example](#-example)
11. [Contributing](#-contributing)
12. [License](#-license)
13. [Acknowledgments](#-acknowledgments)

## 🚀 Features

- **Automated Event Reminders**: Automatically send reminder emails for one-time, weekly, and monthly events.
- **Dynamic Email Templates**: Use customizable Markdown templates for consistent and professional announcements.
- **GitHub Actions Integration**: Trigger workflows to launch or cancel event reminders with ease.
- **Secure Email Handling**: Store sensitive email credentials securely using GitHub Secrets.

## 📋 How It Works

1. **Events Configuration**:
   - List all your events in the `events.tsv` file.
   - Specify the start date, frequency (one-time, weekly, monthly), and the content file for each event.

2. **Email Addresses**:
   - Add the email addresses of your admins, organizers, and sender in the `email_addresses.csv` file.
   - Ensure the "Sender" role is designated to the email address that will send the reminders.

3. **Templates**:
   - Customize your email content using Markdown files stored in the `templates` folder.
   - The `admin.md` template includes placeholders for dynamic content insertion.

## 🛠️ Setup

1. **Fork the Repository**:
   - Press the "Fork" button in the upper right and follow the instructions (just do this once).
   - Navigate to your fork (`https://github.com/username/pbs-social-committee`).
   - Press the "Sync fork" button to make sure you're up to date with the source repository!

2. **Add GitHub Secrets**:
   - Navigate to your forked repository on GitHub.
   - Go to **Settings** > **Secrets** > **Actions**.
   - Add a new secret with the name `GMAIL_PASSWORD` and the value of your Gmail password.

3. **Configure CSV and TSV Files**:
   - Update `events.tsv` with your event details:
     - **Event Name**: The name of the event.
     - **Start Date**: The start date in YYYY-MM-DD format.
     - **Frequency**: 'O' for one-time, 'W-X' for weekly on day X, 'M' for monthly.
     - **Content File**: The filename of the content file in the templates folder.
     - **Date**: A plain text description of the event date.
     - **Time**: The time of the event.
     - **Location**: The location of the event.
   - Update `email_addresses.csv` with your team members' email addresses and roles:
     - **Name**: The name of the person.
     - **Role**: Admin, Organizer, or Sender.
     - **Email address**: The email address of the person.

## 🚀 Usage

### Launch Event Reminders

Trigger the `launch_events.yml` workflow to start sending event reminders.

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Launch Events** workflow.
3. Click **Run workflow**.

### Pause Event Reminders

Trigger the `pause_events.yml` workflow to stop sending event reminders.

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Pause Events** workflow.
3. Click **Run workflow**.

### Compile Schedule

Trigger the `compile_schedule.yml` workflow to generate the event schedule PDF.

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Compile Schedule** workflow.
3. Click **Run workflow**.
4. When it's done, view the updated schedule [here](https://github.com/ContextLab/pbs-social-committee/blob/main/events_schedule.pdf)!

## 🔄 Starting a New Term

1. **Update Events and Email Addresses**:
   - Modify `events.tsv` with new or updated event details.
   - Update `email_addresses.csv` if committee membership or admin staffing has changed.
   - Update `templates/admin.md` with new admin names if needed.

2. **Run Launch Events Script**:
   - Trigger the `launch_events.yml` workflow to start sending event reminders.

3. **Compile Schedule**:
   - Run the `compile_schedule.yml` workflow to generate and view the updated schedule PDF.

## 🏁 Finishing Out a Term

Trigger the `pause_events.yml` workflow to stop sending event reminders.

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Pause Events** workflow.
3. Click **Run workflow**.

## 🔄 Updating Committee Membership

1. **Add or Remove Members**:
   - Update `email_addresses.csv` with new or removed members.
   - Ensure the "Sender" role is assigned correctly.

2. **Update Admin Template**:
   - Modify `templates/admin.md` with new admin names.

## ➕ Adding or Modifying Events

1. **Add New Events**:
   - Add new event details to `events.tsv`.
   - Create a new Markdown template file in the `templates` folder for the new event.
   - Run the `launch_events.yml` workflow to start sending reminders for the new event.

2. **Modify Existing Events**:
   - Update `events.tsv` with new details or change the content file.
   - Edit the corresponding Markdown template in the `templates` folder.
   - Run the `launch_events.yml` workflow to apply the changes.

## 🗂️ Repository Organization

```plaintext
📦pbs-social-committee
 ┣ 📂.github
 ┃ ┗ 📂workflows
 ┃ ┃ ┣ 📜launch_events.yml
 ┃ ┃ ┣ 📜pause_events.yml
 ┃ ┃ ┗ 📜compile_schedule.yml
 ┣ 📂scripts
 ┃ ┣ 📜generate_event_reminders.py
 ┃ ┣ 📜send_email_Game_Night.py
 ┃ ┣ 📜send_email_Hike_to_Gile_Mountain.py
 ┃ ┗ 📜... other send_email scripts ...
 ┣ 📂templates
 ┃ ┣ 📜admin.md
 ┃ ┣ 📜game_night.md
 ┃ ┣ 📜hike_gile_mountain.md
 ┃ ┗ 📜... other event templates ...
 ┣ 📜events.tsv
 ┗ 📜email_addresses.csv
💡 Example
Here's a quick example to get you started:

events.tsv
```
Event Name Start Date Frequency Content File Date Time Location
Research Extravaganza 2024-09-20 O research_extravaganza.md Friday, September 20 TBD TBD
Hike to Gile Mountain 2024-09-21 O hike_gile_mountain.md First two weeks of term TBD Meet at Moore Hall then carpool to Gile Mountain
Mid-term Wine and Cheese Gathering 2024-10-21 O wine_cheese_gathering.md Monday, October 21 4:00 – 5:30 PM Bucci Lounge, Moore Hall, 2nd floor
Winter Holiday Party 2024-12-15 O winter_holiday_party.md Mid-December TBD TBD
Weekly Wednesday Woccoms 2024-09-25 W-W wednesday_woccoms.md Wednesdays throughout the term 2





hold on...you're forgetting to use "```" instead of "
"...the rendering is getting messed up :(
ChatGPT
markdown
Copy code
# 🤖 One-stop Automation for the PBS Social Committee!
Credit: [ChatGPT](https://chatgpt.com/)!

Isn't being "social" annoying? With this repository, *you can automate away the annoyances*!

Welcome to the ultimate automation hub for the PBS Social Committee! Say goodbye to tedious manual tasks and hello to streamlined, automated processes. This repository has everything you need to manage event reminders and announcements effortlessly.

## 📑 Table of Contents

1. [Features](#-features)
2. [How It Works](#-how-it-works)
3. [Setup](#-setup)
4. [Usage](#-usage)
   - [Launch Event Reminders](#launch-event-reminders)
   - [Pause Event Reminders](#pause-event-reminders)
   - [Compile Schedule](#compile-schedule)
5. [Starting a New Term](#-starting-a-new-term)
6. [Finishing Out a Term](#-finishing-out-a-term)
7. [Updating Committee Membership](#-updating-committee-membership)
8. [Adding or Modifying Events](#-adding-or-modifying-events)
9. [Repository Organization](#-repository-organization)
10. [Example](#-example)
11. [Contributing](#-contributing)
12. [License](#-license)
13. [Acknowledgments](#-acknowledgments)

## 🚀 Features

- **Automated Event Reminders**: Automatically send reminder emails for one-time, weekly, and monthly events.
- **Dynamic Email Templates**: Use customizable Markdown templates for consistent and professional announcements.
- **GitHub Actions Integration**: Trigger workflows to launch or cancel event reminders with ease.
- **Secure Email Handling**: Store sensitive email credentials securely using GitHub Secrets.

## 📋 How It Works

1. **Events Configuration**:
   - List all your events in the `events.tsv` file.
   - Specify the start date, frequency (one-time, weekly, monthly), and the content file for each event.

2. **Email Addresses**:
   - Add the email addresses of your admins, organizers, and sender in the `email_addresses.csv` file.
   - Ensure the "Sender" role is designated to the email address that will send the reminders.

3. **Templates**:
   - Customize your email content using Markdown files stored in the `templates` folder.
   - The `admin.md` template includes placeholders for dynamic content insertion.

## 🛠️ Setup

1. **Fork the Repository**:
   - Press the "Fork" button in the upper right and follow the instructions (just do this once).
   - Navigate to your fork (`https://github.com/username/pbs-social-committee`).
   - Press the "Sync fork" button to make sure you're up to date with the source repository!

2. **Add GitHub Secrets**:
   - Navigate to your forked repository on GitHub.
   - Go to **Settings** > **Secrets** > **Actions**.
   - Add a new secret with the name `GMAIL_PASSWORD` and the value of your Gmail password.

3. **Configure CSV and TSV Files**:
   - Update `events.tsv` with your event details:
     - **Event Name**: The name of the event.
     - **Start Date**: The start date in YYYY-MM-DD format.
     - **Frequency**: 'O' for one-time, 'W-X' for weekly on day X, 'M' for monthly.
     - **Content File**: The filename of the content file in the templates folder.
     - **Date**: A plain text description of the event date.
     - **Time**: The time of the event.
     - **Location**: The location of the event.
   - Update `email_addresses.csv` with your team members' email addresses and roles:
     - **Name**: The name of the person.
     - **Role**: Admin, Organizer, or Sender.
     - **Email address**: The email address of the person.

## 🚀 Usage

### Launch Event Reminders

Trigger the `launch_events.yml` workflow to start sending event reminders.

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Launch Events** workflow.
3. Click **Run workflow**.

### Pause Event Reminders

Trigger the `pause_events.yml` workflow to stop sending event reminders.

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Pause Events** workflow.
3. Click **Run workflow**.

### Compile Schedule

Trigger the `compile_schedule.yml` workflow to generate the event schedule PDF.

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Compile Schedule** workflow.
3. Click **Run workflow**.
4. When it's done, view the updated schedule [here](https://github.com/ContextLab/pbs-social-committee/blob/main/events_schedule.pdf)!

## 🔄 Starting a New Term

1. **Update Events and Email Addresses**:
   - Modify `events.tsv` with new or updated event details.
   - Update `email_addresses.csv` if committee membership or admin staffing has changed.
   - Update `templates/admin.md` with new admin names if needed.

2. **Run Launch Events Script**:
   - Trigger the `launch_events.yml` workflow to start sending event reminders.

3. **Compile Schedule**:
   - Run the `compile_schedule.yml` workflow to generate and view the updated schedule PDF.

## 🏁 Finishing Out a Term

Trigger the `pause_events.yml` workflow to stop sending event reminders.

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Pause Events** workflow.
3. Click **Run workflow**.

## 🔄 Updating Committee Membership

1. **Add or Remove Members**:
   - Update `email_addresses.csv` with new or removed members.
   - Ensure the "Sender" role is assigned correctly.

2. **Update Admin Template**:
   - Modify `templates/admin.md` with new admin names.

## ➕ Adding or Modifying Events

1. **Add New Events**:
   - Add new event details to `events.tsv`.
   - Create a new Markdown template file in the `templates` folder for the new event.
   - Run the `launch_events.yml` workflow to start sending reminders for the new event.

2. **Modify Existing Events**:
   - Update `events.tsv` with new details or change the content file.
   - Edit the corresponding Markdown template in the `templates` folder.
   - Run the `launch_events.yml` workflow to apply the changes.

## 🗂️ Repository Organization

```
📦pbs-social-committee
 ┣ 📂.github
 ┃ ┗ 📂workflows
 ┃ ┃ ┣ 📜launch_events.yml
 ┃ ┃ ┣ 📜pause_events.yml
 ┃ ┃ ┗ 📜compile_schedule.yml
 ┣ 📂scripts
 ┃ ┣ 📜generate_event_reminders.py
 ┃ ┣ 📜send_email_Game_Night.py
 ┃ ┣ 📜send_email_Hike_to_Gile_Mountain.py
 ┃ ┗ 📜... other send_email scripts ...
 ┣ 📂templates
 ┃ ┣ 📜admin.md
 ┃ ┣ 📜game_night.md
 ┃ ┣ 📜hike_gile_mountain.md
 ┃ ┗ 📜... other event templates ...
 ┣ 📜events.tsv
 ┗ 📜email_addresses.csv
```

## 💡 Example

Here's a quick example to get you started:

### events.tsv

### email_addresses.csv

```
Name,Role,Email address
John Doe,Admin,johndoe@example.com
Jane Smith,Organizer,janesmith@example.com
Bob Brown,Sender,bobbrown@gmail.com
```

### templates/admin.md

```
# Upcoming Event Notification

Hello Admin,

Please send out the following announcement to the department:

===BEGIN===
[Your event content will be inserted here]
===END===

Thank you,
PBS Social Committee
```

### templates/weekly_sync.md

```
Event Calendar

Weekly Sync Meeting 🧑‍💼🤝🧑‍💼

Hey team,

Don't forget our weekly sync meeting happening every Tuesday at 10 AM.

Cheers,
PBS Social Committee
```

### templates/monthly_meeting.md

```
Event Calendar

Monthly Meeting 📆

Hey team,

Join us for our monthly meeting to discuss progress and plans. Looking forward to seeing you there!

**Date:** {DATE}
**Time:** {TIME}
**Location:** {LOCATION}

Cheers,
PBS Social Committee
```

## 👩‍💻 Contributing

We welcome contributions! If you have ideas to improve this repository, feel free to submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

Special thanks to all of the PBS Social Committee members for their feedback and contributions!
