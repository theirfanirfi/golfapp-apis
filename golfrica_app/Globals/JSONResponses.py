from golfrica_app.Models.models import User, LoginDevice
from flask import escape
from base64 import b64decode
import json

notLoggedIn = dict({
    "isLoggedIn": False,
    'message': 'Your are not logged in'
})

found = dict({
    "isLoggedIn": True,
})

dataUpdateResponse = dict({
    "isLoggedIn": True,
    'isUpdated': True,
})

dataNotUpdateResponse = dict({
    "isLoggedIn": True,
    'isUpdated': False,
})

dataSavedResponse = dict({
    "isLoggedIn": True,
    'isSaved': True,
})

dataNotSavedResponse = dict({
    "isLoggedIn": True,
    'isSaved': False,
})

def AuthorizeRequest(headers):
    if not 'Authorization' in headers:
        return False

    token = headers['Authorization']
    token = escape(token)
    token_str = str(token).encode('ascii')
    missing_padding = len(token_str) % 4
    if missing_padding:
        return False

    token = b64decode(token_str)
    device = LoginDevice.query.filter_by(token=token)
    if not device.count() > 0:
        return False

    device = device.first()
    user = User.query.filter_by(user_id=device.user_id)

    if not user.count() > 0:
        return False

    return user.first()


def get_decoded(data):
    data = str(data).encode('ascii')
    missing_padding = len(data) % 4
    if missing_padding:
        return False
    try:
        data = b64decode(data)
        data = json.loads(data)
        return data
    except:
        return False


