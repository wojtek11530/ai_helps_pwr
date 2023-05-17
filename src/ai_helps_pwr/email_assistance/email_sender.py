import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


class EmailSender:

    def __init__(self, sender_email: str, password: str):
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        self.sender_email = sender_email
        message["From"] = sender_email
        self.password = password
        self.message = message

    def add_pic_to_email(self, cid, img_path):
        fp = open(img_path, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', f'<{cid}>')
        self.message.attach(msgImage)

    def create_email(self, html_body_path: str, text):
        with open(html_body_path, "r", encoding='utf-8') as f:
            html = f.read()

        html = html.replace('Odpowiedz', text)
        self.add_pic_to_email("image1", 'data/email/images/image-1.png')
        self.add_pic_to_email("image2", 'data/email/images/image-2.png')
        self.add_pic_to_email("image4", 'data/email/images/image-4.jpeg')
        self.add_pic_to_email("image5", 'data/email/images/image-5.png')
        self.add_pic_to_email("image6", 'data/email/images/students.png')

        m_text = MIMEText(html, "html")
        self.message.attach(m_text)

    def _send_mail(self, receiver_email):
        self.message["To"] = receiver_email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=context
        ) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, receiver_email, self.message.as_string()
            )

    def send_mail(
        self,
        receiver_email: str,
        text: str,
        html_body_path: str = "data/email/index.txt"
    ):
        self.create_email(html_body_path, text)
        self._send_mail(receiver_email)
