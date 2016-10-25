#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_mail import Message

from ca import app, db, mail
from ca.models import Request

import datetime
from subprocess import call


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

requests_subcommands = Manager(usage="Handle certificate requests")
manager.add_command('requests', requests_subcommands)

certificates_subcommands = Manager(usage="Handle existing certificates")
manager.add_command('certificates', certificates_subcommands)


def mail_certificate(id, email):
        msg = Message(
                app.config['MAIL_SUBJECT'],
                sender=app.config['MAIL_FROM'],
                recipients=[email]
                )
        msg.body = render_template('mail.txt')
        certificate_path = "{}/freifunk_{}.tgz".format(
                app.config['DIRECTORY_CLIENTS'],
                id
                )
        with app.open_resource(certificate_path) as fp:
            msg.attach(
                    "freifunk_{}.tgz".format(id),
                    "application/gzip",
                    fp.read()
                    )
        mail.send(msg)


@requests_subcommands.command
def process():
    "Process new certificate requests"
    for request in Request.query.filter(Request.generation_date == None).all():  # noqa
        if app.config['SHOW_SIGNED_REQUESTS']:
            numsigned = Request.query.filter(Request.email == request.email, Request.generation_date != None).count()
            prompt = "Do you want to generate a certificate for {}, {}?\n\talready signed to this address: {}"
            print(prompt.format(request.id, request.email, numsigned))
        else:
            prompt = "Do you want to generate a certificate for {}, {} ?"
            print(prompt.format(request.id, request.email))
        print("Type y to continue")
        confirm = input('>')
        if confirm in ['Y', 'y']:
            print('generating certificate')
            call([app.config['COMMAND_BUILD'], request.id, request.email])
            request.generation_date = datetime.date.today()
            db.session.commit()
            mail_certificate(request.id, request.email)
            print()
        else:
            print('skipping generation \n')


@requests_subcommands.command
def show():
    "Show new certificate requests"
    for request in Request.query.filter(Request.generation_date == None).all():  # noqa
        prompt = "ID: {} - Email: {}"
        print(prompt.format(request.id, request.email))


@certificates_subcommands.command
def send():
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
def show():
    "Show already existing certificates"
    for request in Request.query.filter(Request.generation_date != None).all():  # noqa
        prompt = "ID: {} - Email: {}"
        print(prompt.format(request.id, request.email))

if __name__ == '__main__':
    manager.run()
