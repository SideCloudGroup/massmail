# Postal邮件群发工具

## 使用方法：
1. 在`config.toml`中配置好邮件服务器的信息，以及发件相关设置
2. 将收件人的邮箱地址填写到`emails.txt`中，每行一个
3. 将邮件内容以HTML的格式写入`email.html`中
4. 执行`pip3 install -r requirements.txt`安装依赖
5. 执行`python3 main.py`开始发送邮件
