from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import gmail_api
import oauth2
import build_service
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/spam', methods=['GET', 'POST'])
def spam():
    try:
        session['RECIPIENT'] = request.form.get('to')
        session['SUBJECT'] = request.form.get('subject')
        session['MESSAGE'] = request.form.get('message')
        return redirect(oauth2.get_authorization_url("dnshelby712@gmail.com", None))
    except:
        return render_template('index.html')

@app.route('/done', methods=['GET', 'POST'])
def done():
    try:
        code = request.args.get('code')
        creds = oauth2.get_credentials(code, None)
        user_info = oauth2.get_user_info(creds)
        email_address = user_info.get('email')
        gmail = build_service.build_service(creds)
        message = gmail_api.create_message("me", session['RECIPIENT'], session['SUBJECT'], session['MESSAGE'])
        gmail_api.send_message(gmail, "me", message)
        return render_template('index.html')
    except:
        return render_template('index.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host='192.168.0.22', port=5001,ssl_context='adhoc')
    # app.run(debug=True,host='192.168.0.17', port=5001,ssl_context='adhoc')
