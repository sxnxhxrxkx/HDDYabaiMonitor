import requests
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

def send_notify(message, config):
    if strtobool(config['LINE']['flag']):
        send_line_notify(message, config)
    if strtobool(config['discord']['flag']):
        send_discord_webhook(message, config)
    if strtobool(config['slack']['flag']):
        send_slack_webhook(message, config)
    return
