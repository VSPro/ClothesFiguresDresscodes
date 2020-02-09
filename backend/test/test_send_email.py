import datetime
from portalbackend import app
from portalbackend.ses_email_adapter import SESEmailAdapter


# Note this won't work unless you have SEND_EMAIL_IN_TESTS=True in your env
def test_send_email():
    with app.app_context():
        email = SESEmailAdapter(app)
        msg = "The test is good"
        sender = "noreply@incountry.com"
        rec = "scottp@incountry.com"
        subject = "Email test at {}".format(str(datetime.datetime.now()))
        email.send_email_message(
            rec, subject, msg, msg, sender, "InCountry System"
        )


def test_support(client, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    message = '''Hi team. I get 400 error while trying to make API calls
                 to POPAPI. Is there anything wrong with my API keys?'''
    rv = client.post(
        '/v2/support',
        json={
            "email": 'email@dsdfgk.com',
            "subject": 'Critical issue with POPAPI',
            "message": message,
            "recaptcha": "12332445",
        },
    )
    assert rv.status_code == 200
