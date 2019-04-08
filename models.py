from app import db


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return f'<Email: {self.email}>'
