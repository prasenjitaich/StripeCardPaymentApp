import logging
import stripe
from rest_framework import status
from rest_framework.views import APIView

import constants
from response_utils import ApiResponse, get_error_message
from .models import User
from .serializers import UserSerializer
from stripe_card_payment import settings

logger = logging.getLogger('django')
stripe.api_key = settings.STRIPE_SECRET_KEY


class UsersList(APIView):
    """
    Class is used for list all the user or create new user.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Function is used to create new object or value in table and return status.
        :param request: request header with user info for creating new object.
        :return: user info
        """
        serializer = UserSerializer(data=request.data)
        logger.info("UserList post request data is {}".format(request.data))
        if serializer.is_valid():
            customer = stripe.Customer.create(
                name=request.data.get('username'),
                email=request.data.get('email'),
                phone=request.data.get('phone_number'),
            )
            serializer.save(customer_id=customer['id'])
            api_response = ApiResponse(status=1, data=serializer.data, message=constants.CREATE_USER_SUCCESS,
                                       http_status=status.HTTP_201_CREATED)
            return api_response.create_response()
        api_response = ApiResponse(status=0, message=get_error_message(serializer),
                                   http_status=status.HTTP_400_BAD_REQUEST)
        return api_response.create_response()


class UserDetails(APIView):
    """
    Class is used for retrieve, update or delete a user instance.
    """

    def get(self, request, pk):
        """
        Function is used for get user info with pk
        :param request: request header with required info.
        :return: user info or send proper error status
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            api_response = ApiResponse(status=0, message=constants.USER_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        serializer = UserSerializer(user)
        api_response = ApiResponse(status=1, data=serializer.data, message=constants.GET_USER_SUCCESS,
                                   http_status=status.HTTP_200_OK)
        return api_response.create_response()

    def put(self, request, pk):
        """
        Function is used for modify user info
        :param request: request header with required info.
        :return: user info or send proper error status
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            api_response = ApiResponse(status=0, message=constants.USER_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if user.customer_id:
                stripe.Customer.modify(
                    user.customer_id,
                    name=request.data.get('username', user.username),
                    email=request.data.get('email', user.email),
                    phone=request.data.get('phone_number', user.phone_number),
                )
            serializer.save()
            api_response = ApiResponse(status=1, data=serializer.data, message=constants.UPDATE_USER_SUCCESS,
                                       http_status=status.HTTP_201_CREATED)
            return api_response.create_response()
        api_response = ApiResponse(status=0, message=get_error_message(serializer),
                                   http_status=status.HTTP_400_BAD_REQUEST)
        return api_response.create_response()

    def delete(self, request, pk):
        """
        Function is used for deleting user object
        :param request: request header with required info.
        :param pk: primary field to get user info.
        :return: 200 ok or error message
        """

        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            api_response = ApiResponse(status=0, message=constants.USER_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        customer_id = user.customer_id
        user.delete()
        if customer_id:
            stripe.Customer.delete(customer_id)
        api_response = ApiResponse(status=1, message=constants.DELETE_USER_SUCCESS, http_status=status.HTTP_200_OK)
        return api_response.create_response()
