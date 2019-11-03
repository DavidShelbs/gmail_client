from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import quickstart
import oauth2
import build_service

RECIPIENT = ""

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/spam', methods=['GET', 'POST'])
def spam():
    global RECIPIENT
    RECIPIENT = request.form.get('to')
    return redirect(oauth2.get_authorization_url("dnshelby712@gmail.com", None))
    # scope = "https://mail.google.com/"
    # if GOOGLE_REFRESH_TOKEN is None:
    #     return redirect(gmail.generate_permission_url(GOOGLE_CLIENT_ID, scope))
        # session['refresh_token'], session['access_token'], session['expires_in'] = gmail.get_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
        # session['GOOGLE_REFRESH_TOKEN'] = session['refresh_token']

    # send_mail('dnshelby712@gmail.com', 'dnshelby712@gmail.com',
    #           'A mail from you from Python',
    #           '<b>A mail from you from Python</b><br><br>' +
    #           'So happy to hear from you!')
    # email_client.send_message(email, to, message, password)
    return render_template('index.html')

@app.route('/done', methods=['GET', 'POST'])
def done():
    global RECIPIENT
    code = request.args.get('code')
    creds = oauth2.get_credentials(code, None)
    user_info = oauth2.get_user_info(creds)
    email_address = user_info.get('email')
    gmail = build_service.build_service(creds)
    message = quickstart.create_message("me", RECIPIENT, "Test subject", "Test body")
    quickstart.send_message(gmail, "me", message)
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True,host='192.168.0.17', port=5001,ssl_context='adhoc')
