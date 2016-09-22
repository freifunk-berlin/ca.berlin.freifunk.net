#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from subprocess import call

from ca import app, db
from ca.models import Request

from flask import Flask, render_template
from flask_mail import Mail, Message


def mail_certificate(id, email):
    msg = Message('Freifunk Vpn03 Key', sender = 'no-reply@ca.berlin.freifunk.net', recipients = [email])
    msg.body = render_template('mail.txt')
    with app.open_resource("/etc/openvpn/client/freifunk_{}.tgz".format(id)) as fp:
        msg.attach("freifunk_{}.tgz".format(id), "application/gzip", fp.read())
    mail.send(msg)

for request in Request.query.filter(Request.generation_date == None).all():  # noqa
    prompt = "Do you want to generate a certificate for {}, {} ?"
    print(prompt.format(request.id, request.email))
    print("Type y to continue")
    confirm = input('>')
    if confirm in ['Y', 'y']:
        print('generating certificate')
        call([app.config['COMMAND_BUILD'], request.id, request.email])
        #call([app.config['COMMAND_MAIL'], request.id, request.email])
        mail_certificate(request.id, request.email)
        request.generation_date = datetime.date.today()
        db.session.commit()
        print()
    else:
        print('skipping generation \n')
