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

    def __init__(self, id, email, generation_date=None):
        self.id = id
        self.email = email
        self.generation_date = generation_date

    def __repr__(self):
        return "<Request {} - {} - {}>".format(
                self.id,
                self.email,
                self.generation_date
                )


class RequestForm(Form):
    id = TextField(
            'Id',
            [
                validators.Length(min=4, max=32),
                validators.Required(),
                validators.Regexp(
                    "[a-z]+[\-a-z]*",
                    message="Must be lowercase and can contain '-'."
                    )
            ]
            )
    email = TextField(
            'E-Mail',
            [
                validators.Email(), validators.Required(),
                validators.EqualTo('email_confirm')
            ]
            )
    email_confirm = TextField('E-Mail')
    captcha = TextField(
            'Rätzel',
            validators=[
                validators.AnyOf(['Berlin', 'berlin'], message="Incorrect. If you keep having trouble contact the mailing list."),
                validators.Required()
            ]
    )


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
