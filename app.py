from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import gmail_api
import oauth2
import build_service
import os
import sqlite3
import google.oauth2.credentials
import google_auth_oauthlib.flow

app = Flask(__name__)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/spam', methods=['GET', 'POST'])
def spam():
    # try:
        session['FROM'] = request.form.get('from')
        session['RECIPIENT'] = request.form.get('to')
        session['SUBJECT'] = request.form.get('subject')
        session['MESSAGE'] = request.form.get('message')
        session['QUANTITY'] = request.form.get('quantity')
        return redirect(oauth2.get_authorization_url(session['FROM'], None))
    # except:
        return render_template('index.html')

@app.route('/done', methods=['GET', 'POST'])
def done():
    try:
        state=None
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://mail.google.com/'],
        state=state)
        flow.redirect_uri = 'https://localhost/done'

        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)

        # Store the credentials in the session.
        # ACTION ITEM for developers:
        #     Store user's access and refresh tokens in your data store if
        #     incorporating this code into your real app.
        creds = flow.credentials
        session['credentials'] = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes}


        # code = request.args.get('code')
        # creds = oauth2.get_credentials(code, None)
        # user_info = oauth2.get_user_info(creds)
        # email_address = user_info.get('email')
        gmail = build_service.build_service(creds)
        # print(email_address)
        message = gmail_api.create_message("me", session['RECIPIENT'], session['SUBJECT'], session['MESSAGE'])
        gmail_api.send_message(gmail, "me", message)
        return render_template('index.html')
    except:
        return render_template('index.html')

if __name__ == "__main__":
    database = r"email_client.db"
    app.secret_key = os.urandom(24)
    # app.run(debug=True, host='192.168.0.22', port=443, ssl_context='adhoc')
    # app.run(debug=True,host='192.168.0.17', port=443,ssl_context='adhoc')
    app.run(debug=True,host='0.0.0.0', port=443,ssl_context='adhoc')
