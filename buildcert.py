#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from subprocess import call

from ca import app, db
from ca.models import Request

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
