#!/usr/bin/python

import json.decoder

import sys
import urllib3
import certifi
import smtplib
import email.utils
from email.mime.text import MIMEText
from systemd import journal

# User variables
hostname = 'your.mirror.domain'
receiverMail = 'receiver@email.com'
senderMail = 'sender@from.email'
mailServer = 'smtp.server.url'
mailPort = 587
username = 'username'
password = 'password'
logPrefix = '[mirrorCheck] '

# Retrieving mirror status
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
mirrorStatus = http.request('GET', 'https://www.archlinux.org/mirrors/status/json/')
if mirrorStatus.status != 200:
    journal.send(logPrefix + 'Unable to download mirror status')
    exit(1)

jsonStatus = json.loads(mirrorStatus.data)
if 'urls' not in jsonStatus:
    journal.send(logPrefix + 'Mirror status is not in a correct format')
    exit(1)

for url in jsonStatus['urls']:
    if 'url' not in url or 'completion_pct' not in url:
        journal.send(logPrefix + 'URLs status are not in a correct format')
        exit(1)
    if hostname in url['url'] and url['completion_pct'] < 0.95:
        msg = MIMEText("ALARM!  Mirror is out-of-sync!!!\n\nAffected URL: " + url['url'] + "\n\nCurrent sync is " + str(
            url['completion_pct'] * 100) + "%.\n\nLast sync occurred : " + url[
                           'last_sync'] + "\n\nFix is required ASAP!")
        msg['To'] = email.utils.formataddr(('Recipient', receiverMail))
        msg['From'] = email.utils.formataddr(('Author', senderMail))
        msg['Subject'] = 'Mirror out of sync'

        smtpRelay = smtplib.SMTP(mailServer, mailPort)
        smtpRelay.ehlo()
        smtpRelay.starttls()
        smtpRelay.ehlo()
        smtpRelay.login(username, password)

        smtpRelay.sendmail(senderMail, receiverMail, msg.as_string())
        smtpRelay.quit()

        # One mail have been sent, exiting to avoid spam
        sys.exit(0)
