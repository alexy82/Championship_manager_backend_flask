import json
import socket
from logging import Handler, INFO

import requests
from logging.handlers import HTTPHandler


class PythonHTTPHandler(HTTPHandler):
    def __init__(self, logPath, host, url, method):
        HTTPHandler.__init__(self, host, url, method)
        self.logPath = logPath
        self.s = requests.Session()

    def mapLogRecord(self, record):
        record_modified = HTTPHandler.mapLogRecord(self, record)
        record_modified['logPath'] = self.logPath
        try:
            record_modified['msg'] = self.format(record)
        except Exception as e:
            pass
        return record_modified

    def emit(self, record):
        try:
            host = self.host
            url = self.url
            url = 'http://' + host + '/' + url
            data = self.mapLogRecord(record)
            self.s.post(url, data=data, timeout=10)

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            self.handleError(record)


class LogSlackHandler(Handler):
    """
    Log handler
    """
    __color_dict = {
        'INFO': 'info',
        'WARNING': 'warning',
        'WARN': 'warning',
        'ERROR': 'danger',
    }

    def __init__(self, level=INFO, webhook='', username='LogSlackHandler bot',
                 icon_emoji=':loud_sound:', sender=None, channel='#watch-dog'):
        """
        Constructor
        :param level: log level
        :param webhook: Slack webhook
        :param username: display Username of bot
        :param icon_emoji: icon for bot
        :param sender: send from whom
        :param channel: channel to send
        """
        Handler.__init__(self, level)
        self.webhook = webhook
        self.username = username
        self.icon_emoji = icon_emoji
        if sender is None:
            sender = socket.gethostname()
        self.sender = sender
        self.channel = channel
        self.session = requests.Session()

    def mapLogRecord(self, record):
        """
        Map log record in to required format
        :param record:
        :return:
        """
        pretext = '*<!channel> {level}*'.format(level=record.levelname)
        title = '[{level}] - {sender}'.format(level=record.levelname,
                                              sender=self.sender)
        message = self.format(record)

        payload = {
            'username': self.username,
            'icon_emoji': self.icon_emoji,
            'channel': self.channel,
            'attachments': [
                {
                    'pretext': pretext,
                    'color': self.__color_dict.get(record.levelname, 'INFO'),
                    'mrkdwn_in': [
                        'pretext'
                    ],
                    'fields': [
                        {
                            'title': title,
                            'value': message,
                            'short': False
                        }
                    ]
                }
            ]
        }
        payload = json.dumps(payload)
        return payload

    def emit(self, record):
        """
        Emit log
        :param record:
        :return:
        """
        try:
            data = self.mapLogRecord(record)
            self.session.post(self.webhook, data=data, timeout=10)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            self.handleError(record)
