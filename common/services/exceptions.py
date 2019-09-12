from rest_framework.views import exception_handler

def api_error_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['error'] = {
            'code': response.status_code,
            'message': response.data['detail']
        }
        del response.data['detail']
    return response
