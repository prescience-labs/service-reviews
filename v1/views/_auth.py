# from django.core.exceptions import PermissionDenied
# from rest_framework.exceptions import PermissionDenied as PermissionException

# from common.services.auth import check_user_auth

# def check_auth(request):
#     """Wraps the check_user_auth function in a DRF-compatible format

#     Args:
#     - request (HttpRequest)

#     Raises:
#     - PermissionDenied: A DRF-compatible exception with the same message
#     """
#     try:
#         check_user_auth(request)
#     except PermissionDenied as e:
#         raise PermissionException(e)
