import json
import time
import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
import toml
from urllib3 import Retry


def init_session(proxy):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.proxies = {} if proxy == "" else {"http": proxy, "https": proxy}
    return s


def send_mails(session, server, key, from_name, from_email, to, subject, content):
    data = {
        "from": f"{from_name} <{from_email}>",
        "sender": from_email,
        "to": to,
        "subject": subject,
        "html_body": content
    }
    data = json.dumps(data)
    result = session.post(server + "/api/v1/send/message", data=data,
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


if __name__ == "__main__":
    try:
        config = toml.load("config.toml")
    except FileNotFoundError:
        print("配置文件config.toml不存在")
        exit()
    server = config["postal"]["server"]
    key = config["postal"]["key"]
    from_name = config["postal"]["from_name"]
    from_email = config["postal"]["from_email"]
    if server == "" or key == "" or from_name == "" or from_email == "":
        print("请先修改配置文件config.toml")
        exit()
    emails = []
    try:
        emails_file = open(config['setting']['email_list'], "r")
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
    try:
        html_file = open(config["setting"]["email_content"], "r", encoding="utf-8")
    except FileNotFoundError:
        print("读取邮件内容失败")
        exit()
    else:
        html = html_file.read()
        html_file.close()
    session = init_session(config["setting"]["proxy"])
    if input("确认发送？(y/n)") != "y":
        exit()
    delay = (60 / config["setting"]["limit"]) if config["setting"]["limit"] != 0 else 0
    total_emails = len(emails)
    print(f"延迟{delay}秒发送，共{total_emails}封邮件")
    for i, address in enumerate(tqdm(emails, desc="发送邮件进度"), start=1):
        try:
            send_mails(session, server, key, from_name, from_email, [address], config["setting"]["subject"], html)
        except Exception as e:
            print(f"发件失败，错误信息：{e}")
            session = init_session(config["setting"]["proxy"])
        if i != total_emails:
            time.sleep(delay)
