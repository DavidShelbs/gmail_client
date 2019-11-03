from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
# import quickstart
import email_client

app = Flask(__name__)

message = """\
Subject: Hi there

This message is sent from Python."""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/spam', methods=['GET', 'POST'])
def spam():
    # quickstart.main()
    email = request.form.get('from')
    to = request.form.get('to')
    password = request.form.get('password')
    email_client.send_message(email, to, message, password)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=4000)
