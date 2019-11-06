from django.conf import settings
import requests

def get_client_auth_header():
    return 'Basic ' + settings.AUTH_SERVICE['CLIENT_ID'] + ':' + settings.AUTH_SERVICE['CLIENT_SECRET']

def get_user_auth_header():
    response = requests.post(settings.AUTH_SERVICE['BASE_URL'] + '/token', {
        'email': settings.TESTING['user_email'],
        'password': settings.TESTING['user_password'],
        'team': settings.TESTING['team_id'],
    })
    response = response.json()
    return 'Bearer ' + response['token']
