# ca.berlin.freifunk.net

This project helps us (Freifunk Berlin) to automate the certificate request
process. In the past a user requested a certificate for our vpn service via the
mailinglist which caused a lot of noise on the mailing list and work on the
admin side of the process. Today we use a webinterface for user input that lives
at [https://ca.berlin.freifunk.net](https://ca.berlin.freifunk.net). The user
provides us with an id and e-mail and generates a certificate request in the
database. After the generation of the request a admin has to execute the
`buildcert` command on the server to create the certificate and send it to the
user.

## Development

Install and use virtualenv with:

```
virtualenv env
. env/bin/activate
```

Install dependencies with pip:

```
pip install -r requirements.txt
```


Setup the database

Open a python terminal and run
```
from app import db
db.create_all()
```

Note that the default path for the database is in `/tmp` so you will lose your data when rebooting.

Run the application
```
python3 manage.py runserver
```

All development should be done in Python 3.
