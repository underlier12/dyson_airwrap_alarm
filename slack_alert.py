import requests
import configparser

class SlackAlert:
    def __init__(self) -> None:
        self.TOKEN = self._read_token()

    def _read_token(self):
        config = configparser.ConfigParser()
        config.read('slack_bot.ini')
        token = config['bot']['token']
        return token

    def send_message(self, channel, message):
        headers = {
            "Authorization": "Bearer "+self.TOKEN
        }
        
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            data={
                "channel": channel,
                "text": message
            }
        )
