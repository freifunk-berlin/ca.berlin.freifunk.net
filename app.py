#!/bin/env python

from flask import Flask, request, render_template, flash, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import Form, TextField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'foobar'
db = SQLAlchemy(app)


class Request(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120))
    generation_date = db.Column(db.Date())

    def __init__(self, id, email):
        self.id = id
        self.email = email

    def __repr__(self):
        return "<Request {} - {}>".format(self.id, self.email)


class RequestForm(Form):
    id = TextField(
            'Id',
            [validators.Length(min=4, max=32), validators.Required()]
            )
    email = TextField(
            'Email',
            [
                validators.Email(), validators.Required(),
                validators.EqualTo('email_confirm')
            ]
            )
    email_confirm = TextField('Confirm Email')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RequestForm(request.form)
    if request.method == 'POST' and form.validate():
        req = Request(form.id.data, form.email.data)
        db.session.add(req)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()
