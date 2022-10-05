import os
import smtplib as smtp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#
login = os.environ.get('FROM_MAIL')
password = os.environ.get('PASSWORD')
code = '<p> Ваша учетная запись на сайте {{domain}} успешно создана.</p>' # Присваиваем code пустую строку
user_email = 'karlvonkrause@protonmail.com'

try:
    msg = MIMEMultipart()
    msg['subject'] = 'Verification code'
    msg['from'] = login
    msg['to'] = user_email
    msg.attach(MIMEText(code, 'plain', 'utf-8'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(login, password)
        smtp.send_message(msg)
        smtp.quit()
except Exception as e:
    print(e)
# to = 'karlvonkrause@hotmail.com'
# try:
#     server = smtp.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(login, password)
#
#     subject = '!!!!!!!!!!!!!!'
#     text = 'Lorum ipsum dolo.....'
#
#     server.sendmail(login, to, f'Subject:{subject}\n{text}')
# except TimeoutError as e:
#     print(e)


