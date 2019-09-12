import logging

from rest_framework import generics

from common.models import ReviewRequest
from common.services.email import Email
from v1.serializers import ReviewRequestSerializer

logger = logging.getLogger(__name__)

class ReviewRequestList(generics.ListCreateAPIView):
    queryset            = ReviewRequest.objects.all()
    serializer_class    = ReviewRequestSerializer

    def post(self, request, *args, **kwargs):
        # create the data, delay the response
        result = super().post(request, *args, **kwargs)

        # send an email to the customer
        logger.debug(result.data)
        customer_email  = result.data['target_customer_email']
        product_name    = result.data['product_name']
        email           = Email(customer_email)
        email_result    = email.send_review_request(product_name)
        logger.debug(email_result)

        return result

class ReviewRequestDetail(generics.RetrieveUpdateAPIView):
    queryset            = ReviewRequest.objects.all()
    serializer_class    = ReviewRequestSerializer
