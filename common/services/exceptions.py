from rest_framework.views import exception_handler

def api_error_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        message = 'No additional information is available. :('
        if 'detail' in response.data.keys():
            message = response.data['detail']
            del response.data['detail']
        response.data['error'] = {
            'code': response.status_code,
            'message': message,
        }
    return response
