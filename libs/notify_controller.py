import requests
from email.mime.text import MIMEText
import smtplib
from distutils.util import strtobool
from discord_webhook import DiscordWebhook, DiscordEmbed
import slackweb
from libs.logger import writelog  # log出力

def send_line_notify(message, config):
    writelog('info','send_line_notify','start')
    line_notify_token = config['LINE']['TOKEN']
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    result = requests.post(line_notify_api, data=payload, headers=headers)
    writelog('info','send_line_notify','end' + str(result))
    return

def send_discord_webhook(message, config):
    writelog('info','send_discord_webhook','start')
    discord_url = config['discord']['url']
    webhook = DiscordWebhook(url=discord_url, content=message)
    result = webhook.execute()
    writelog('info','send_discord_webhook','end' + str(result))
    return

def send_slack_webhook(message, config):
    writelog('info','send_slack_webhook','start')
    slack_url = config['slack']['url']
    slack = slackweb.Slack(url=slack_url)
    result = slack.notify(text=message)
    writelog('info','send_slack_webhook','end' + str(result))
    return

def send_gmail_notify(message, config, subject):
    writelog('info','send_gmail_notify','start')    
    # SMTP認証情報
    from_email = config['gmail']['from_email']
    from_password = config['gmail']['from_password']    
    to_email = config['gmail']['to_email']
    # 件名
    if len(subject) == 0:
        subject = config['gmail']['subject']
        
    # MIMEの作成
    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email
    
    # メール送信処理
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, from_password)
    result = server.send_message(msg)
    server.quit()
    writelog('info','send_gmail_notify','end' + str(result))
    return

def send_notify(message, config, subject=""):
    if strtobool(config['LINE']['flag']):
        send_line_notify(message, config)
    if strtobool(config['discord']['flag']):
        send_discord_webhook(message, config)
    if strtobool(config['slack']['flag']):
        send_slack_webhook(message, config)
    if strtobool(config['gmail']['flag']):
        send_gmail_notify(message, config, subject)
    return