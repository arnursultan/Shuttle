import random
import redis
from twilio.rest import Client
from django.conf import settings

r = redis.Redis(host='localhost', port=6379, db=0)


def send_verification_code(phone, code):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your verification code: {code}",
        from_=twilio_phone_number,
        to=phone
    )
    return message.sid


def generate_and_send_code(phone):
    code = str(random.randint(1000, 9999))
    redis_key = f'verification_{phone}'

    r.set(redis_key, code, ex=600)

    send_verification_code(phone, code)
