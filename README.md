# server-tools
Some tools usefull for server administration

# mirrorUpdater
Create and maintain up-to-date an ArchLinux mirror.

### Setup
Change (or not) *source* and *lastupdate_url* and launch the script every hour by cron.
That's all, you've got a working mirror.

All you have to do is just a bit on configuration on your Apache/Nginx server


# mirrorCheck
Check if a specified ArchLinux mirror is syncing well.
If not, send an email to specified address.

### Setup
To run _mirrorCheck_ you need:

- python > 3.0.0

- certify ( _python-certifi_ package)

- urllib3 ( _python-urllib3_ package)

- systemd (for logging)

- smtplib (by default)

The rest of Python packages should be installed by default.

### Configuration
Configurations variables are following.

- hostname : hostname which will be looked for in ArchLinux mirror's list.  Typically, it's your domain name

- receiverMail : email address which will receive a warning email when sync rate for your mirror is too low

- senderMail : email address which will send the email.  Generally «something@hostname.com»

- mailServer : server used to send mail.  Generally «localhost» if you have a postfix installed locally

- mailPort : port used to connect to SMTP server. Generally 25.  If not 25, STARTTLS will be automatically enabled

- username : username used to log into SMTP server

- password : password user to log into SMTP server

- logPrefix : prefix used for logs in Systemd.  Change it if you want.


# serverStatus
Check overall status of running services
If one service fails, it will try to restart it and will warn you,
sending last logs if script is unable to restart service.

Requirements are the same as for _mirrorCheck_, just edit the few config variables
and script is OK.
