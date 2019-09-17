from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

def api_error_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if type(response.data) is list:
            # cast to dict to handle DRF inconsistent exceptions
            response.data = dict({ 'detail': response.data[0] })
        message = 'No additional information is available. :('
        if 'detail' in response.data.keys():
            message = response.data['detail']
            del response.data['detail']
        response.data['error'] = {
            'code': response.status_code,
            'message': message,
        }
    return response
