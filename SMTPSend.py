
import smtplib
import configparser

from email.mime.text import MIMEText


config = configparser.ConfigParser()
config.read('dbConnections.ini')

# sending
port = 25
host = '192.168.1.211'
sender_email = 'eam_converter@smd-chem.ru'
# receiver_email = 'EAM_Converter_Info@smd-chem.ru'
receiver_email = config['Email']['Receiver']
print(receiver_email)

message = MIMEText('Внимание!!!\nПрограмма EamConverter завершила работу с ошибкой.\n', 'plain', 'utf-8')

#     send email
with smtplib.SMTP(host, port) as server:
    server.sendmail(sender_email, receiver_email, message.as_string())

server.close()