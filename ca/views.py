from flask import Flask, request, render_template, flash, url_for, abort
from itsdangerous import URLSafeSerializer

from ca import app, db
from ca.forms import RequestForm
from ca.models import Request

s = URLSafeSerializer(app.config['SECRET_KEY'])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RequestForm(request.form)
    if request.method == 'POST' and form.validate():
        req = Request(form.id.data, form.email.data)
        db.session.add(req)
        db.session.commit()
        token = s.dumps(req.id, salt='freifunk-ca-service')
        confirm_url = url_for('get_certificate',
                              token=token,
                              _external=True)

        return render_template('thanks.html')
    return render_template('index.html', form=form)


@app.route('/certificates/<token>', methods=['GET'])
def get_certificate(token):
    try:
        cert_id = s.loads(token, salt='freifunk-ca-service')
    except:
        abort(404)

    ca_req = Request.query.get_or_404(cert_id)
    print(ca_req)

    return "return key + cert here + {}".format(ca_req)
