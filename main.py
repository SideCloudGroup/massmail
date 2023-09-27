import json

from requests import post

server = ""  # Postal面板地址，无需路径和斜杠
key = ""  # Postal API Key
from_name = ""  # 发件人名称
from_email = ""  # 发件人邮箱


def send_mails(to, subject, content):
    global server, key, from_name, from_email
    data = {
        "from": f"{from_name} <{from_email}>",
        "sender": from_email,
        "to": to,
        "subject": subject,
        "html_body": content
    }
    # 转换成json格式
    data = json.dumps(data)
    result = post(server + "/api/v1/send/message", data=data,
                  headers={"X-Server-API-Key": key, "content-type": "application/json"})
    if result.status_code == 200:
        result_json = json.loads(result.text)
        if result_json["status"] != "success":
            print(f"发件失败，错误信息：{result_json['data']['message']}")
            return False
        else:
            print("发件成功")
            return True
    else:
        print(f"发件失败，错误信息：{result.text}")
        return False


# 读取邮件列表到数组
emails = []
emails_file_name = input("请输入邮箱列表txt文件名，无需后缀\n")
try:
    emails_file = open(emails_file_name + ".txt", "r")
except FileNotFoundError:
    print("读取邮箱列表失败")
    exit()
else:
    for line in emails_file.readlines():
        if line.strip() != "":
            emails.append(line.strip())
    emails_file.close()
    if len(emails) == 0:
        print("邮箱列表为空")
        exit()

print(f"共读取到{len(emails)}个邮箱")
html_file_name = input("请输入邮件内容html文件名，无需后缀\n")
try:
    html_file = open(html_file_name + ".html", "r", encoding="utf-8")
except FileNotFoundError:
    print("读取邮件内容失败")
    exit()
else:
    html = html_file.read()
    html_file.close()

title = input("请输入邮件标题\n")
if input("确认发送？(y/n)") != "y":
    exit()
for address in emails:
    send_mails([address], title, html)
