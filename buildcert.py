#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import datetime
from subprocess import call

from ca import app, db
from ca.models import Request

from OpenSSL import crypto, SSL
from os.path import exists, join

CERT_FILE = "myapp.crt"
KEY_FILE = "myapp.key"

# taken from https://gist.github.com/ril3y/1165038
def create_self_signed_cert(cert_dir):
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    if not exists(join(cert_dir, CERT_FILE)) \
            or not exists(join(cert_dir, KEY_FILE)):

        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        cert.get_subject().L = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        cert.get_subject().O = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"
        cert.get_subject().OU = "my organization"
        cert.get_subject().CN = "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')

        open(join(cert_dir, CERT_FILE), "wt").write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(join(cert_dir, KEY_FILE), "wt").write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

create_self_signed_cert('/tmp')

quit(0)

for request in Request.query.filter(Request.generation_date == None).all():  # noqa
    prompt = "Do you want to generate a certificate for {}, {} ?"
    print(prompt.format(request.id, request.email))
    print("Type y to continue")
    confirm = input('>')
    if confirm in ['Y', 'y']:
        print('generating certificate')
        call([app.config['COMMAND_BUILD'], request.id, request.email])
        call([app.config['COMMAND_MAIL'], request.id, request.email])
        request.generation_date = datetime.date.today()
        db.session.commit()
        print()
    else:
        print('skipping generation \n')
