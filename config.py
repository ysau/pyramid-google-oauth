from authomatic.providers import oauth2
import json

def load_google_credential():
    try:
        with open('client_secret.json') as file:
            data = json.load(file)
            client_id = data['web']['client_id']
            client_secret = data['web']['client_secret']
        print('Google O-auth credential loaded from disk')
        return client_id, client_secret
    except IOError:
        print('File not found.  Please save Google O-auth credential as client_secret.json')


GOOGLE_LOGIN_CLIENT_ID, GOOGLE_LOGIN_CLIENT_SECRET = load_google_credential()

CONFIG = {
    'google': {
        'class_': oauth2.Google,
        'consumer_key': GOOGLE_LOGIN_CLIENT_ID,
        'consumer_secret': GOOGLE_LOGIN_CLIENT_SECRET,
        'scope': ['email', 'profile'],
    }
}

