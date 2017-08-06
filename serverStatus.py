#!/usr/bin/python

import subprocess
from datetime import datetime, timedelta, time
import smtplib
import email.utils
from email.mime.text import MIMEText


def main():
    start = ServerStatus()


if __name__ == "__main__":
    main()


class ServerStatus:
    receiverMail = 'receiver@email.com'  # Receiver mail
    senderMail = 'sender@from.email'  # Sender mail
    mailServer = 'smtp.server.url'  # SMTP server
    mailPort = 587  # Port (25 or 587 if using TLS)
    username = 'username'  # Username if TLS
    password = 'password'  # Password if TLS

    # Internal variable.  DO NOT EDIT
    relaunch_status = False

    def __init__(self):
        # Call for general status
        main_process = subprocess.Popen("systemctl status | grep State: | head -1 | awk '{print $2}'", shell=True,
                                        stdout=subprocess.PIPE)
        status = main_process.stdout.read().decode('UTF-8').strip()
        main_process.stdout.close()

        if status != "running":
            failing_process = subprocess.Popen("systemctl --failed | grep failed | wc -l", shell=True,
                                               stdout=subprocess.PIPE)
            failing_units = int(failing_process.stdout.read().decode('UTF-8').strip())
            failing_process.stdout.close()
            if failing_units == 0:
                error_msg = 'System is unstable but I don\'t detect any failed service.\n\nCurrent status is «' + status + '»'
            else:
                failed_process = subprocess.Popen("systemctl --failed | grep failed | awk '{print $2}'", shell=True,
                                                  stdout=subprocess.PIPE)
                failed_units = failed_process.stdout.read().decode('UTF-8').strip()
                failed_process.stdout.close()
                failed_units = failed_units.split('\n')
                error_msg = str(failing_units) + " failed services have been found.\n\n"
                error_msg += 'Following units are in «failed» state:\n'
                for unit in failed_units:
                    # Attempting unit restart
                    result = self.relaunch_unit(unit)
                    if self.relaunch_status:
                        error_msg += '- ' + unit + ': RELAUNCHED on ' + datetime.now().strftime(
                            "%Y-%m-%d %H:%I:%S") + "\n"
                        if result:
                            error_msg += "This message was returned while reloading service:\n"
                            error_msg += result + "\n\n"
                    else:
                        error_msg += '- ' + unit + ': FAILED on ' + datetime.now().strftime("%Y-%m-%d %H:%I:%S") + "\n"
                        error_msg += "Message returned while reloading unit:\n"
                        error_msg += result + "\n"
                        error_msg += "This is the last error log we have about this failure:\n"
                        error_msg += self.get_log_for_unit(unit) + "\n\n"

            # Sending email
            self.send_mail(error_msg)

    @staticmethod
    def get_log_for_unit(unit):
        previous_hour = datetime.now() - timedelta(hours=1)
        unit_log_process = subprocess.Popen(
            "journalctl -u " + unit + " --since '" + previous_hour.strftime("%Y-%m-%d %H:%I:%S") + "'", shell=True,
            stdout=subprocess.PIPE)
        logs = unit_log_process.stdout.read().decode('UTF-8').strip()
        unit_log_process.stdout.close()
        return logs

    def relaunch_unit(self, unit):
        self.relaunch_status = False
        unit_reload_process = subprocess.Popen("systemctl start " + unit, shell=True, stdout=subprocess.PIPE)
        unit_restart_result = unit_reload_process.stdout.read().decode('UTF-8').strip()
        relaunch_message = ''
        if unit_restart_result:
            relaunch_message = unit_restart_result
        unit_reload_process.stdout.close()
        time.sleep(15)  # Waiting 15 sec for process to restart
        unit_status_process = subprocess.Popen("systemctl status " + unit + " | grep Active: | awk '{print $2}'",
                                               shell=True, stdout=subprocess.PIPE)
        if unit_status_process.stdout.read().decode('UTF-8').strip() != "active":
            self.relaunch_status = True
        unit_status_process.stdout.close()
        return relaunch_message

    def send_mail(self, message):
        msg = MIMEText(message)
        msg['To'] = email.utils.formataddr(('Recipient', self.receiverMail))
        msg['From'] = email.utils.formataddr(('Author', self.senderMail))
        msg['Subject'] = 'Mirror out of sync'

        smtpRelay = smtplib.SMTP(self.mailServer, self.mailPort)
        smtpRelay.ehlo()
        if self.mailPort > 25:
            smtpRelay.starttls()
            smtpRelay.ehlo()
            smtpRelay.login(self.username, self.password)

        smtpRelay.sendmail(self.senderMail, self.receiverMail, msg.as_string())
        smtpRelay.quit()