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

The rest of Python packages should be installed by default.

### Configuration
Configurations variables are following.

- hostname : hostname which will be looked for in ArchLinux mirror's list.  Typically, it's your domain name

- receiverMail : email address which will receive a warning email when sync rate for your mirror is too low

- senderMail : email address which will send the email.  Generally «something@hostname.com»

- mailServer : server used to send mail.  Generally «localhost» if you have a postfix installed locally

- logPrefix : prefix used for logs in Systemd.  Change it if you want.
