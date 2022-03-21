import smtplib, ssl

class EmailNotifier:
    
    # port for starttls
    port = 587
    # server address
    smtp_server = "smtp.gmail.com"
    # sender email address (to specify)
    sender_email = ""
    # sender password (to specify)
    password = ""
    # list of recipients(s)
    recipients = []
    # message content
    message = """\
    Subject: Bad Posture Detected

    Content of detection."""

    # constructor
    def __init__(self, recipients):
        self.recipients = recipients

    # setter for message
    def setMessage(self, message):
        self.message = message

    # function for sending email to all specified recipients
    def sendEmail(self):
        
        # retrieve each recipient's email and send email notification
        for recipient_email in self.recipients:
            
            # create a ssl context
            context = ssl.create_default_context()

            # try loging in using sender credentials and send email notification
            try:
                server = smtplib.SMTP(self.smtp_server, self.port)
                server.ehlo()
                # secure the connection
                server.starttls(context=context)
                server.ehlo()
                # login
                server.login(self.sender_email, self.password)
                # send email
                server.sendmail(self.sender_email, recipient_email, self.message)
            except Exception as e:
                print(e)
            finally:
                server.quit()

# Sample Usage
# message = """\
# Subject: Hi there

# This message is sent from Python."""

# emailNotifier = EmailNotifier(["leongjinghao@gmail.com"])
# emailNotifier.setMessage(message)
# emailNotifier.sendEmail()
