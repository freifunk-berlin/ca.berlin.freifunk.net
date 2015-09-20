#!/bin/env python

from app import Request, db
from glob import glob
from ntpath import basename
from sqlalchemy.exc import IntegrityError
from OpenSSL import crypto
from datetime import datetime

DIRECTORY = "tests/openvpn/easy-rsa/keys/"


for path in glob("{}/freifunk_*.crt".format(DIRECTORY)):
    with open(path) as file:
        print("Importing {} ...".format(path))
        certificate = crypto.load_certificate(
                crypto.FILETYPE_PEM,
                file.read()
                )
        # extract email and id from subject components
        components = dict(certificate.get_subject().get_components())
        email_address = components[b'emailAddress']
        # remove 'freifunk_' prefix from id
        id = components[b'CN'].decode('utf-8').replace('freifunk_', '')
        # extract creation date from certificate
        creation_date = datetime.strptime(
                certificate.get_notBefore().decode('utf-8'),
                '%Y%m%d%H%M%SZ'
                )
        request = Request(id, email_address, creation_date)
        try:
            db.session.add(request)
            db.session.commit()
            print("Improted {}.".format(id))
        except IntegrityError:
            print("{} already exists.".format(id))
            db.session.rollback()
