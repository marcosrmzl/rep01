from app import app
from flask import render_template, request, make_response, jsonify, redirect, url_for
from flask_cors import cross_origin
from twilio.rest import Client
import keys


@app.route("/")
def index():
    return render_template("public/index.html")


@app.route('/', methods=['POST'])
def my_form_post():
    if request.method == "POST":
        phone_num = request.form["phnum"]
        text_sms = request.form["smstext"]
        full_sms = str(f"Phone:{phone_num} ,  Sms Text: {text_sms}")
        print(phone_num, text_sms)
        print(full_sms)
        client = Client(keys.account_sid, keys.auth_token)

        message = client.messages.create(
            body=text_sms,
            from_=keys.twilio_number,
            to=phone_num
        )

        print(message.body)
        return redirect(url_for('sms_success', smsok=text_sms, phoneok=phone_num))
    else:
        return render_template("index.html")


@app.route('/<smsok>.<phoneok>')
def sms_success(smsok, phoneok):
    return f"<h1>message:{smsok} / {phoneok}</h1> "



@app.route("/data", methods=['GET', 'POST'])
@cross_origin()
def data():
    if request.is_json:
        render_template("ft/data.html")

        req = request.get_json()

        response = {
            "message": "JSON received!",
            "jsonHtml": req.get('jsonHtml')
        }

        res = make_response(jsonify(response), 200)

        print(request)
        return res

    else:

        res = make_response(jsonify({"message": "No JSON received"}))

        return "No JSON received", 400
