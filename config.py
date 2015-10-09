# -*- coding: utf-8 -*-

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SECRET_KEY = 'foobar'
DIRECTORY = "tests/openvpn/easy-rsa/keys/"
COMMAND_BUILD = "tests/openvpn/clients/openvpn-build-key"
COMMAND_MAIL = "tests/openvpn/clients/openvpn-mail-key"
