# -*- coding: utf-8 -*-

# override these in instance/config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SECRET_KEY = 'foobar'
DENY_EXEC_AS_ROOT = True
DIRECTORY = "tests/openvpn/easy-rsa/keys/"
CACERT_FILE = '/tmp/ffca.crt'
CAKEY_FILE = '/tmp/ffca.key'

# tunnel.berlin.freifunk.net settings
SHOW_SIGNED_REQUESTS = True
MAIL_FROM = "no-reply@tunnel.berlin.freifunk.net"
MAIL_SUBJECT = "Freifunk Tunnel-Berlin Zugangsdaten"
NEWKEY_ALG = 'rsa'
NEWKEY_SIZE = 2048
NEWCERT_COUNTRY = "DE"
NEWCERT_STATE = "Eastern Germany"
NEWCERT_LOCATION = "Berlin"
NEWCERT_ORGANIZATION = "Freifunk Community Berlin"
NEWCERT_DURATION = 10*365*24*60*60 # 10 years
NEWCERT_COMMENT = b'initial test-certs'
NEWCERT_SIGNDIGEST = "sha256"
