# coding=utf-8
"""实现发送邮件的公共方法
"""

from email.mime.text import MIMEText

import os
import smtplib
import json


def send_mail(tasks: int):
    """
    Send alert to users.

    :param tasks: Specify the email content and its receivers,
                 i.e., content as keys, receivers as values.
                 Example `tasks`:
                 [
                    {
                        'users': [some users],
                        'data': {
                            'key1': 'value1',
                            'key2': 'value2',
                        }
                    },
                 ]
    """

    mail_host = os.environ.get('SMTP_SERVER') or 'smtp.163.com'
    alert_email_sender = os.environ.get('ALERT_EMAIL_SENDER') or 'alert@163.com'
    alert_email_password = os.environ.get('ALERT_EMAIL_PASSWORD') or 'apasswordhardtoguess'
    ssl_enable = os.environ.get('SSL_BASED_ALERT_EMAIL', False)
    default_port = os.environ.get('ALERT_EMAIL_PORT')

    try:
        if ssl_enable:
            port = default_port or 465
            smtp_obj = smtplib.SMTP_SSL_PORT(mail_host, port)
        else:
            port = defaut_port or 25
            smtp_obj = smtplib.SMTP(mail_host, port)
        # smtp_obj.set_debuglevel(1)
        smtp_obj.login(alert_email_sender, alert_email_password)
    except smtplib.SMTPAuthenticationError as e:
        return 'Failed to connect to alert email server. Please check.'
    try:
        for task in tasks:
            receivers = task.get('users')
            email_content = json.dumps(task.get('data'))
            smtp_obj.sendmail(alert_email_sender, receivers, email_content)
    except Exception as e:
        print(e)
