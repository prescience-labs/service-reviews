import logging

from django.conf import settings
from django.http import HttpRequest
import requests
from rest_framework import authentication
from rest_framework import exceptions

logger = logging.getLogger(__name__)

class AuthorizationHeaderAuthentication(authentication.BaseAuthentication):
    """Checks the current user/client from the Authoriation header and adds them to the request.

    If the user tried to log in via Authorization: Bearer <token> they will be a user.
    If the user tried to log in via Authorization: Basic <id>:<secret> they will be a client.

    request.user contains the payload of the user/client.
    request.auth contains the type (user or client) of the authentication.

    Raises:
    - exceptions.AuthenticationFailed: raises auth failed on any exception
    """
    def authenticate(self, request):
        try:
            header      = request.headers.get('Authorization').split()
            auth_type   = header[0].lower()
            credentials = header[1]
            payload     = None

            logger.debug('Authorization header:')
            logger.debug(header)

            if auth_type == 'bearer':
                logger.debug('Bearer auth')
                user = requests.get(
                    settings.AUTH_SERVICE['BASE_URL'] + '/users/current',
                    headers={
                        'Authorization': 'Bearer ' + credentials,
                    },
                )
                auth_type   = 'user'
                payload     = user.json()

            elif auth_type == 'basic':
                logger.debug('Basic auth')
                credentials = credentials.split(':')
                client = requests.get(
                    settings.AUTH_SERVICE['BASE_URL'] + '/clients/current',
                    headers={
                        'Authorization': 'Basic ' + credentials[0] + ':' + credentials[1],
                    },
                )
                auth_type   = 'client'
                payload     = client.json()

            else:
                raise exceptions.AuthenticationFailed("The Authorization header wasn't formatted properly")

            return (payload, auth_type)
        except exceptions.AuthenticationFailed as e:
            raise exceptions.AuthenticationFailed(e)
        except:
            raise exceptions.AuthenticationFailed('Not authenticated. Try putting a valid token in the Authorization header.')
