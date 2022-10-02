import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


def recaptcha_token_validate(value):
    VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'response': value,
        'secret': settings.RECAPTCHA_SECRET_KEY
    }
    resp = requests.post(VERIFY_URL, data=data)
    result_json = resp.json()
    if not (result_json.get('success') is True and result_json.get('score') >= 0.5):
        msg = _('You are like a bot.')
        raise serializers.ValidationError(msg, code="authorization")
    return True
