#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ca import app, db
from ca.models import Request
from glob import glob
from sqlalchemy.exc import IntegrityError
from OpenSSL import crypto
from datetime import datetime

def import_easyrsa_certsn():
    print ("begin import serials of old EasyRSA certificates")
    easyrsa_index = open(os.path.join(app.config['DIRECTORY'], "index.txt"), 'r')
    for request in Request.query.filter(Request.generation_date != None).filter(Request.cert_sn == None).all():
        req_subject = "/CN=freifunk_" + request.id + "/emailAddress=" + request.email
        print("looking up : " + req_subject)
        for line in easyrsa_index:
            (flag, signdate, revokedate, sn, unknown, subject) = line.split("\t")
            if (revokedate != None) and (req_subject in subject):
                print (" match")
                request.cert_sn = sn
                print (" imported")
        easyrsa_index.seek(0)
    db.session.commit()


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

# try to import existing certificate serials also
import_easyrsa_certsn()
