#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import datetime
from subprocess import call

from ca import app, db
from ca.models import Request

from OpenSSL import crypto, SSL
from os.path import exists, join

# taken from https://gist.github.com/ril3y/1165038
def create_cert(cert_name, cert_email, cert_key):
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    # get required CA-data
    ca_cert_file = open('/tmp/ffca.crt', 'r')
    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ca_cert_file.read())
    ca_key_file = open('/tmp/ffca.key', 'r')
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key_file.read())

    if True:

        # create a self-signed cert
        cert = crypto.X509()
        cert.set_version = 3
        cert.get_subject().C = "DE"
        cert.get_subject().ST = "Eastern Germany"
        cert.get_subject().L = "Berlin"
        cert.get_subject().O = "Foerderverein Freie Netzwerke e.V."
        cert.get_subject().CN = "freifunk_%s" % cert_name
        cert.get_subject().emailAddress = cert_email
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(ca_cert.get_subject())
        cert.set_pubkey(cert_key)

        # create cert extensions
        cert_ext = [
            crypto.X509Extension('basicConstraints', False, 'CA:FALSE'),
            crypto.X509Extension('nsComment', False, 'made for you with PyOpenSSL'),
            crypto.X509Extension('subjectKeyIdentifier', False, 'hash', subject=cert),
            crypto.X509Extension('authorityKeyIdentifier', False, 'keyid:always,issuer:always', issuer=ca_cert),
            crypto.X509Extension('extendedKeyUsage', False, 'TLS Web Client Authentication'),
            crypto.X509Extension('keyUsage', False, 'Digital Signature'),
        ]
        cert.add_extensions(cert_ext)

        cert.sign(ca_key, 'sha1')

        print crypto.dump_certificate(crypto.FILETYPE_TEXT, cert)
        return cert

def create_key():
        """Create a 1024 RSA key-pair"""
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)
        # crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        return k


for request in Request.query.filter(Request.generation_date == None).all():  # noqa
    prompt = "Do you want to generate a certificate for {}, {} ?"
    print(prompt.format(request.id, request.email))
    print("Type y to continue")
    confirm = input('>')
    if confirm in ['Y', 'y']:
        print('generating certificate')
        new_key = create_key()
        new_cert = create_cert(request.id, request.email, new_key)
        # construct the TAR-archive here
        # and maybe rework the email-code
        #call([app.config['COMMAND_BUILD'], request.id, request.email])
        #call([app.config['COMMAND_MAIL'], request.id, request.email])
        #request.generation_date = datetime.date.today()
        db.session.commit()
        print()
    else:
        print('skipping generation \n')
