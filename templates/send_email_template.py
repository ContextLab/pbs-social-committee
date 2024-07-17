import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "{sender_email}"
receiver_email = "{admin_emails_str}"
cc_email = "{organizer_emails_str}"
subject = "{event_name} Reminder"

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Cc'] = cc_email
msg['Subject'] = subject

body = """{announcement_content}"""
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, "{password}")
text = msg.as_string()
server.sendmail(sender_email, receiver_email.split(", ") + cc_email.split(", "), text)
server.quit()
