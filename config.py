# -*- coding: utf-8 -*-

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SECRET_KEY = 'foobar'
DIRECTORY = "tests/openvpn/easy-rsa/keys/"
COMMAND_BUILD = "tests/openvpn/clients/openvpn-build-key"
MAIL_FROM = "no-reply@ca.berlin.freifunk.net"
MAIL_SUBJECT = "Freifunk VPN03 Zugangsdaten"
DIRECTORY_CLIENTS = "/etc/openvpn/clients/"
