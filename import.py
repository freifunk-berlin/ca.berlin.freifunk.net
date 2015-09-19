#!/bin/env python

from app import Request, db
from glob import glob
from ntpath import basename
from sqlalchemy.exc import IntegrityError

DIRECTORY = "tests/openvpn/easy-rsa/keys/"


for file in glob("{}/freifunk_*.crt".format(DIRECTORY)):
    id = basename(file).replace('freifunk_', '').replace('.crt', '')
    # acctually we should receive the id, email and date by parsing the crt
    request = Request(id, "foo@bar.de")
    try:
        db.session.add(request)
        db.session.commit()
        print("Improted {}.".format(id))
    except IntegrityError:
        print("{} already exists.".format(id))
        db.session.rollback()
