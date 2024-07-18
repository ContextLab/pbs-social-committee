# 🤖 One-stop Automation for the PBS Social Committee!
Credit: [ChatGPT](https://chatgpt.com/)!

Isn't being "social" annoying? With this repository, *you can automate away the annoyances*!

Welcome to the ultimate automation hub for the PBS Social Committee! Say goodbye to tedious manual tasks and hello to streamlined, automated processes. This repository has everything you need to manage event reminders and announcements effortlessly.

## 📚 Table of Contents
- [🚀 Features](#-features)
- [📋 How It Works](#-how-it-works)
- [🛠️ Setup](#️-setup)
- [🚀 Usage](#-usage)
  - [Launch Event Reminders](#launch-event-reminders)
  - [Cancel Event Reminders](#cancel-event-reminders)
  - [Compile Schedule](#compile-schedule)
- [📅 Starting a New Term](#starting-a-new-term)
- [🛑 Finishing Out a Term](#finishing-out-a-term)
- [🔄 Updating Committee Membership](#updating-committee-membership)
- [➕ Adding or Modifying Events](#adding-or-modifying-events)
- [📂 Repository Organization](#-repository-organization)
- [💡 Example](#-example)
- [👩‍💻 Contributing](#-contributing)
- [📄 License](#-license)
- [🎉 Acknowledgments](#-acknowledgments)

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

3. **Configure CSV Files**:
   - Update `events.tsv` with your event details. Make sure the file is tab-separated and follows the format:
     ```
     Event Name    Start Date    Frequency    Content File    Date    Time    Location
     ```
   - Update `email_addresses.csv` with your team members' email addresses and roles:
     ```
     Name,Role,Email address
     ```

## 🚀 Usage

### Launch Event Reminders

Trigger the `launch_events.yml` workflow to start sending event reminders.

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Launch Events** workflow.
3. Click **Run workflow**.

### Cancel Event Reminders

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

## 📅 Starting a New Term

1. Update `events.tsv` with new events for the term.
2. Update `email_addresses.csv` if committee membership or admin staffing has changed.
3. Run the **Launch Events** workflow to schedule new reminders.
4. Run the **Compile Schedule** workflow to generate and update the schedule PDF.

## 🛑 Finishing Out a Term

1. Run the **Pause Events** workflow to stop sending event reminders.

## 🔄 Updating Committee Membership

1. Update the `email_addresses.csv` file with the new committee members and their roles.
2. Run the **Launch Events** workflow to apply the changes.

## ➕ Adding or Modifying Events

1. To add a new event:
   - Add a new line to `events.tsv` with the event details.
   - Add a corresponding template file in the `templates` folder.
   - Run the **Launch Events** workflow to schedule the new event.
2. To modify an event:
   - Update the event details in `events.tsv`.
   - Modify the corresponding template file in the `templates` folder if needed.
   - Run the **Launch Events** workflow to apply the changes.

## 📂 Repository Organization

@tree
- .github
  - workflows
    - compile_schedule.yml
    - launch_events.yml
    - pause_events.yml
    - reminder_*.yml
- scripts
  - send_email_*.py
- templates
  - admin.md
  - *.md
- email_addresses.csv
- events.tsv
- README.md
@@

## 💡 Example

Here's a quick example to get you started:

### events.tsv

```
Event Name    Start Date    Frequency    Content File
Monthly Meeting    2024-07-20    M    monthly_meeting.md
Weekly Sync    2024-07-21    W-T    weekly_sync.md
One-time Workshop    2024-07-25    O    workshop.md
```

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
