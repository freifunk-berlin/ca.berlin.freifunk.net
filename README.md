# ca.berlin.freifunk.net

[![Coverage Status](https://coveralls.io/repos/freifunk-berlin/ca.berlin.freifunk.net/badge.svg?branch=master&service=github)](https://coveralls.io/github/freifunk-berlin/ca.berlin.freifunk.net?branch=master)

This project helps us (Freifunk Berlin) to automate the certificate request
process. In the past a user requested a certificate for our vpn service
[VPN03](https://wiki.freifunk.net/Vpn03) via the mailinglist which caused a lot
of noise on the mailing list and work on the admin side of the process.
Today we use a webinterface for user input that lives at
[https://ca.berlin.freifunk.net](https://ca.berlin.freifunk.net). The user
provides us with an id and e-mail and generates a certificate request in the
database. After the generation of the request an admin has to execute the
`buildcert` command on the server to create the certificate and send it to the
user.

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
