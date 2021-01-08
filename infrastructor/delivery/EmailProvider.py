import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror
from infrastructor.dependency.scopes import IScoped
from models.configs.EmailConfig import EmailConfig


class EmailProvider(IScoped):
    def __init__(self, email_config: EmailConfig):

        self.email_config: EmailConfig = email_config

    def send(self, to, subject, body):
        try:
            # Send your message with credentials specified above
            # with smtplib.SMTP(smtp_server, port) as server:
            # server.ehlo()
            # server.starttls()
            # server.login(MY_ADDRESS, PASSWORD)

            # Create the root message and fill in the from, to, and subject headers
            msgRoot = MIMEMultipart('related')
            msgRoot[
                'Subject'] = subject
            msgRoot['From'] = f'PDI'
            msgRoot['To'] = to
            msgRoot.preamble = 'This is a multi-part message in MIME format.'

            # Encapsulate the plain and HTML versions of the message body in an
            # 'alternative' part, so message agents can decide which they want to display.
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)

            # We reference the image in the IMG SRC attribute by the ID we give it below
            # msg['To']='ahmetcagriakca@gmail.com'

            html = body

            # msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
            # msgAlternative.attach(msgText)
            msgText = MIMEText(html, "html")
            msgAlternative.attach(msgText)

            # # This example assumes the image is in the current directory
            # file_path_1 = os.path.join(root_directory, 'image1.jpg')
            # fp_1 = open(file_path_1, 'rb')
            # msgImage_1 = MIMEImage(fp_1.read())
            # fp_1.close()
            # msgImage_1.add_header('Content-ID', '<image1>')
            # msgRoot.attach(msgImage_1)

            smtp = smtplib.SMTP()
            smtp.connect(self.email_config.host, self.email_config.port)
            smtp.sendmail(self.email_config.from_addr, to, msgRoot.as_string())
            smtp.quit()
        except (gaierror, ConnectionRefusedError):
            # tell the script to report if your message was sent or which errors need to be fixed
            print('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPServerDisconnected:
            print('Failed to connect to the server. Wrong user/password?')
        except smtplib.SMTPException as e:
            print('SMTP error occurred: ' + str(e))
        else:
            print('Sent')
