from ca import db


class Request(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120))
    generation_date = db.Column(db.Date())
    cert_sn = db.Column(db.Integer, unique=True)

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

    def getCertSn(self):
        return "{}".format(self.cert_sn)
