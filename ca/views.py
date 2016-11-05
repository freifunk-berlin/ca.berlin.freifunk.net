from flask import request, render_template
from flask_mail import Message

from ca import app, db, mail
from ca.forms import RequestForm
from ca.models import Request

@app.route('/status')
def status():
    """ Returns a page showing the number of unprocessed certficate-requests. """
    result = db.session.query(Request).filter(Request.generation_date == None).count()
    return render_template('status.html', requests=result)

@app.route('/', methods=['GET'])
def index():
    form = RequestForm()
    return render_template('index.html', form=form)


@app.route('/', methods=['POST'])
def post_request():
    form = RequestForm(request.form)
    if form.validate():
        req = Request(form.id.data, form.email.data)
        db.session.add(req)
        db.session.commit()
        mail_info_after_request(form.email.data)
        return render_template('thanks.html')
    else:
        return render_template('index.html', form=form)

def mail_info_after_request(email):
    msg = Message(
            "Deine Anfrage für das Freifunk VPN ist eingegangen!",
            sender=app.config['MAIL_FROM'],
            recipients=[email]
            )
    msg.body = render_template('mail_info_after_request.txt')
    mail.send(msg)
