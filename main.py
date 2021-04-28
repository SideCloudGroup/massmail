import smtplib
import email
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

smtp_server = smtplib.SMTP("SMTP server here", 25)  # SMTP服务器地址与端口
# smtp_server.set_debuglevel(1) #调试
smtp_server.login("Username", "Password")  # SMTP用户名与密码
from_addr = ""  # 发件人邮箱
from_name = ""  # 发件人名


def _format_addr(s):  # 编码
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def SendMail(toaddr):
    message = MIMEMultipart()
    title = "邮件标题"
    mailtextfile = open("邮件模板.html", "r", encoding='UTF-8')
    mailbody = mailtextfile.read()
    mailtextfile.close()
    message.attach(MIMEText(mailbody, 'html', 'utf-8'))
    message['From'] = _format_addr(f"{from_name} <%s>" % from_addr)
    message['To'] = _format_addr(f"{toaddr} <%s>" % f"{toaddr}")
    message['Subject'] = Header(f'{title}', 'utf-8').encode()
    smtp_server.sendmail(from_addr, toaddr, message.as_string())


def ReadCSV(filepath):
    with open(filepath) as OriginCSV:
        OriginCSV.readline()
        for line in OriginCSV:
            print(line)
            toaddr = line.split(",")[0]
            SendMail(toaddr)


smtp_server.quit()
