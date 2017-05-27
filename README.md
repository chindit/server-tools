# server-tools
Some tools usefull for server administration

# mirrorCheck
Check if a specified ArchLinux mirror is syncing well.
If not, send an email to specified address.

## Configuration
Configurations variables are following.

- hostname : hostname which will be looked for in ArchLinux mirror's list.  Typically, it's your domain name

- receiverMail : email address which will receive a warning email when sync rate for your mirror is too low

- senderMail : email address which will send the email.  Generally «something@hostname.com»

- mailServer : server used to send mail.  Generally «localhost» if you have a postfix installed locally

- logPrefix : prefix used for logs in Systemd.  Change it if you want.
