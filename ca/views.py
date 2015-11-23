from flask import request, render_template

from ca import app, db
from ca.forms import RequestForm
from ca.models import Request


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def post_request():
    form = RequestForm(request.form)
    if form.validate():
        req = Request(form.id.data, form.email.data)
        db.session.add(req)
        db.session.commit()
        return render_template('thanks.html')
    else:
        return render_template('index.html', form=form)
