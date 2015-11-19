# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators, ValidationError

from ca.models import Request
from ca import db

def id_does_not_exist(form, field):
    if db.session.query(Request.id).filter(Request.id == field.data).count():
        raise ValidationError('Id already exists.')

class RequestForm(Form):
    id = StringField(
            'ID',
            [
                validators.Length(min=4, max=32),
                validators.Required(),
                validators.Regexp(
                    "^[a-z]+[a-z\d\-]*$",
                    message="Must be lowercase and can contain '-'."
                    ),
                id_does_not_exist
            ]
            )
    email = StringField(
            'E-Mail',
            [
                validators.Email(), validators.Required(),
                validators.EqualTo('email_confirm')
            ]
            )
    email_confirm = StringField('E-Mail')
    captcha = StringField(
            u'Rätsel',
            validators=[
                validators.AnyOf(
                    ['Berlin', 'berlin'],
                    message="Incorrect. If you keep having trouble contact the mailing list."  # noqa
                    ),
                validators.Required()
            ]
    )
