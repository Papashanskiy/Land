from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
import os
from models import *


base_url = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kfu.anatomy.2018@gmail.com'
app.config['MAIL_PASSWORD'] = 'z31aedc170f8'
app.config['MAIL_USE_TLS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_url, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail(app)
db = SQLAlchemy(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_message(form, email):
    msg = Message('Новый подписчик!', recipients=['kfu.anatomy.2018@gmail.com'], sender='kfu.anatomy.2018@gmail.com')
    msg.html = render_template('email.html', result=form)
    msg.body = 'New subscriber ' + email
    t = Thread(target=send_async_email, args=[app, msg])
    t.start()
    return t


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':

        if Email.query.filter_by(email=request.form['email']).first() == None:
            print('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOKKKKKKKKKKKKKKKKKKKKKKKKKKKKK')
            e = Email(email=request.form['email'])
            db.session.add(e)
            db.session.commit()

        send_message(request.form, request.form['email'])
        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/email')
def email_page():
    q = Email.query.all()
    result = ''
    for i in q:
        result += i.email + '\n'
    return result


if __name__ == '__main__':
    app.run()
