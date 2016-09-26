#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from ca import app, db, mail

import datetime
from subprocess import call

from ca.models import Request

from flask import Flask, render_template
from flask_mail import Message


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

requests_subcommands = Manager(usage="Handle certificate requests")
manager.add_command('requests', requests_subcommands)

certificates_subcommands = Manager(usage="Handle existing certificates")
manager.add_command('certificates', certificates_subcommands)


def mail_certificate(id, email):
    with app.app_context():
        msg = Message(app.config['MAIL_SUBJECT'], sender=app.config['MAIL_FROM'], recipients=[email])
        msg.body = render_template('mail.txt')
        with app.open_resource("{}/freifunk_{}.tgz".format(app.config['DIRECTORY_CLIENTS'], id)) as fp:
            msg.attach("freifunk_{}.tgz".format(id), "application/gzip", fp.read())
        mail.send(msg)


@requests_subcommands.command
def process():
    "Process new certificate requests"
    for request in Request.query.filter(Request.generation_date == None).all():  # noqa
        prompt = "Do you want to generate a certificate for {}, {} ?"
        print(prompt.format(request.id, request.email))
        print("Type y to continue")
        confirm = input('>')
        if confirm in ['Y', 'y']:
            print('generating certificate')
            call([app.config['COMMAND_BUILD'], request.id, request.email])
            mail_certificate(request.id, request.email)
            request.generation_date = datetime.date.today()
            db.session.commit()
            print()
        else:
            print('skipping generation \n')


@requests_subcommands.command
def list():
    "List new certificate requests"
    for request in Request.query.filter(Request.generation_date == None).all():
        prompt = "ID: {} - Email: {}"
        print(prompt.format(request.id, request.email))


@requests_subcommands.command
def send_again():
    "Send existing certificate again"
    print("Which existing certificate do you want to send again? Type the ID")
    send_again_id = input('>')
    print("Where should it be sent? Please type the Email")
    send_again_mail = input('>')
    try:
        mail_certificate(send_again_id, send_again_mail)
        print("OK")
    except:
        print("That didn't work.")


@certificates_subcommands.command
def list():
    "List already existing certificates"
    for request in Request.query.filter(Request.generation_date != None).all():
        prompt = "ID: {} - Email: {}"
        print(prompt.format(request.id, request.email))

if __name__ == '__main__':
    manager.run()
