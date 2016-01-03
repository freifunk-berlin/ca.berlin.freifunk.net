#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ca import app, db
from ca.models import Request
from glob import glob
from sqlalchemy.exc import IntegrityError
from OpenSSL import crypto
from datetime import datetime

for path in glob("{}/freifunk_*.crt".format(app.config['DIRECTORY'])):
    with open(path) as certfile:
        print("Importing {} ...".format(path))
        certificate = crypto.load_certificate(
                crypto.FILETYPE_PEM,
                certfile.read()
                )
        # extract email and id from subject components
        components = dict(certificate.get_subject().get_components())
        email_address = components[b'emailAddress']
        # remove 'freifunk_' prefix from id
        cert_id = components[b'CN'].decode('utf-8').replace('freifunk_', '')
        # extract creation date from certificate
        generation_date = datetime.strptime(
                certificate.get_notBefore().decode('utf-8'),
                '%Y%m%d%H%M%SZ'
                )
        request = Request(cert_id, email_address, generation_date)
        try:
            db.session.add(request)
            db.session.commit()
            print("Improted {}.".format(cert_id))
        except IntegrityError:
            print("{} already exists.".format(cert_id))
            db.session.rollback()
