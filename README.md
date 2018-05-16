# ca.berlin.freifunk.net

[![Coverage Status](https://coveralls.io/repos/freifunk-berlin/ca.berlin.freifunk.net/badge.svg?branch=master&service=github)](https://coveralls.io/github/freifunk-berlin/ca.berlin.freifunk.net?branch=master)

This project helps us (Freifunk Berlin) to automate the certificate request
process. In the past a user requested a certificate for our vpn service
[VPN03](https://wiki.freifunk.net/Vpn03) via the mailinglist which caused a lot
of noise on the mailing list and work on the admin side of the process.
Today we use a webinterface for user input that lives at
[https://ca.berlin.freifunk.net](https://ca.berlin.freifunk.net). This code is
also used for our new Community tunnel [Tunnel Berlin](https://wiki.freifunk.net/Berlin:Community-Tunnel).
The user provides us with an id and e-mail and generates a certificate request in the
database. After the generation of the request an admin has to execute
`python3 manage.py requests process` on the server to create the certificate and send it to the
user. To send an already existing certificate again use `python3 manage.py certificates send`.

See also:
`python3 manage.py requests --help`
`python3 manage.py certificates --help`

## Development

### Required packages (Ubuntu 14.04)
`sudo apt-get install python-virtualenv python-pip python3-dev libffi-dev libssl-dev`

Use virtualenv with:

```
virtualenv env -p python3
. env/bin/activate
```

Install dependencies with pip:

```
pip3 install -r requirements.txt
```


Setup the initial database

```
./manage.py db init
./manage.py db migrate
./manage.py db upgrade
```

Note that the default path for the database is in `/tmp` so you will lose your data when rebooting.

Run the application
```
python3 manage.py runserver
```

To change the **host** you can add the `-h 0.0.0.0` parameter.

To change the **port** you can add the `-p 1337` parameter.

All development should be done in Python 3.


## Deployment

For each deployed system there is a branch "instance/<hostname>" where the actual deployed setup will be hosted. On a new host just branch from master and put your host-specific changes into this branch.

Since this code only requires Python and no additional system-access is required, there is no need to run this instance with root-access for signing. the following lines show some commands that suggest some level of privilege-separation for the daily operation.

### basic system setup
```
# setup of basic system-accounts
addgroup freifunk
addgroup tunnelberlin-signer
addgroup tunnelberlin-admin
adduser --ingroup tunnelberlin-admin --disabled-password --disabled-login tunnelberlin-keymaster
mkdir /home/tunnelberlin-keymaster/ssl-data
# this ca.files needs to be set in the config.py
cp <ca.crt> /home/tunnelberlin-keymaster/ssl-data
cp <ca.key> /home/tunnelberlin-keymaster/ssl-data
chown -R tunnelberlin-keymaster:tunnelberlin-signer /home/tunnelberlin-keymaster/ssl-data
chmod 710 /home/tunnelberlin-keymaster/ssl-data
chmod 640 /home/tunnelberlin-keymaster/ssl-data/ca.*
adduser --ingroup tunnelberlin-signer --disabled-password --disabled-login tunnelberlin-sign
# this directory needs to be set in the config.py and will contain the created certs & keys
mkdir /home/tunnelberlin-sign/certs
chown tunnelberlin-sign:tunnelberlin-signer /home/tunnelberlin-sign/certs
chmod 2770 /home/tunnelberlin-sign/certs

# change the umask that all users of group "tunnelberlin-signer" can write to the files made by other users
sed -i -e "s/UMASK.*/UMASK 002/" /etc/login.defs

# setup of web-frontend, users of group "tunnelberlin-admin" will be able to change the code  (e.g. git pull, git checkout)
mkdir /var/www/tunnel.berln.freifunk.net
chmod 775 /var/www/tunnel.berln.freifunk.net
chgrp tunnelberlin-admin /var/www/tunnel.berln.freifunk.net
cd /var/www/tunnel.berln.freifunk.net
sg tunnelberlin-admin
git clone https://github.com/freifunk-berlin/ca.berlin.freifunk.net.git .
su postgreq -c "createdb -O ca tunnelberlin-ca"
```

### adding a new user
```
adduser --ingroup freifunk <username>
addgroup <username> tunnelberlin-signer
```

### procesing requests
```
cd <instance> # e.g. /var/www/tunnel.berlin.freifunk.net
sg tunnelberlin-signer
. env/bin/activate
./manage ....
```
