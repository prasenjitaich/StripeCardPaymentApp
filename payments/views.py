import logging

import stripe
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView

import constants
from stripe_card_payment import settings
from response_utils import ApiResponse

logger = logging.getLogger('django')
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_public_key = settings.STRIPE_PUBLIC_KEY
stripe_webhook_secret = settings.STRIPE_WEBHOOK_SECRET


class CreatePayment(APIView):
    """
    Class is used to Create PaymentIntent.
    """

    def calculate_amount(self, no_count, default_price):
        """
        Function is used to calculate the total amount and return the total amount.
        :param no_count:No of count based on that calculate the total amount.
        :param default_price: based on that calculate the total amount.
        :return:amount .
        """
        min_amount = constants.MIN_AMOUNT
        per_no_price = default_price
        no_count = int(no_count)
        amount = (no_count * per_no_price) if (no_count * per_no_price) >= min_amount else min_amount
        return amount

    def post(self, request):
        """
        Function is used to create new PaymentIntent object and return status.
        :param request:request header with required info for creating new PaymentIntent.
        :return:PaymentIntent details or error message.
        """
        try:
            default_price = constants.DEFAULT_PRICE
            no_count = request.data.get(constants.PARAM_NO_COUNT)
            if not no_count:
                return ApiResponse(status=0,
                                   message=constants.MISSING_PARAM.format(
                                       constants.PARAM_NO_COUNT),
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            user_obj = request.user
            user_id = user_obj.pk
            user_mail = user_obj.email
            if user_obj.customer_id is None:
                customer = stripe.Customer.create(
                    name=user_obj.username,
                    email=user_obj.email,
                    phone=user_obj.phone_number,
                )
                user_obj.customer_id = customer['id']
                user_obj.save()
            user_customer_id = user_obj.customer_id
            total_amount = self.calculate_amount(no_count, default_price)
            amount = int(total_amount * constants.CONVERT_CENT)
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                customer=user_customer_id,
                receipt_email=user_mail,
                shipping=constants.STRIPE_SHIPPING_ADDRESS,
                description=constants.STRIPE_DESCRIPTION,
                metadata={
                    'user_id': user_id,
                }
            )
            data = {'amount': total_amount, 'clientSecret': intent.client_secret, 'payment_intent': intent.id,
                    'stripe_public_key': stripe_public_key}
            api_response = ApiResponse(status=1, data=data,
                                       message=constants.CREATE_PAYMENT_INTENT_SUCCESS,
                                       http_status=status.HTTP_201_CREATED)
            return api_response.create_response()

        except Exception as e:
            logger.exception("CreatePayment post exception {}".format(e))
            api_response = ApiResponse(status=0, message=constants.CREATE_PAYMENT_INTENT_FAIL,
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return api_response.create_response()


class CreateRefund(APIView):
    """
    Class is used to Create PaymentRefund.
    """

    def post(self, request):
        """
        Function is used to create new PaymentRefund object and return the details & the status.
        :param request:request header with required info for creating new PaymentRefund.
        :return:PaymentRefund details or error message.
        """
        try:
            payment_intent = request.data.get(constants.PARAM_PAYMENT_INTENT_ID)
            if not payment_intent:
                return ApiResponse(status=0,
                                   message=constants.MISSING_PARAM.format(
                                       constants.PARAM_PAYMENT_INTENT_ID)).create_response()
            refund_list = stripe.Refund.list(payment_intent=payment_intent)
            if refund_list.data:
                api_response = ApiResponse(status=0,
                                           message=constants.PAYMENT_ALREADY_REFUND,
                                           http_status=status.HTTP_200_OK)
                return api_response.create_response()
            refund = stripe.Refund.create(
                payment_intent=payment_intent,
            )
            api_response = ApiResponse(status=1, data=refund,
                                       message=constants.CREATE_PAYMENT_REFUND_SUCCESS,
                                       http_status=status.HTTP_200_OK)
            return api_response.create_response()
        except Exception as e:
            logger.exception("CreateRefund post exception {}".format(e))
            api_response = ApiResponse(status=0, message=constants.CREATE_PAYMENT_REFUND_FAIL,
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return api_response.create_response()


class CancelPaymentIntent(APIView):
    """
    Class is used to Cancel PaymentIntent.
    """

    def post(self, request):
        """
        Function is used to cancel PaymentIntent with an incomplete status & return the details.
        :param request:request header with required info for canceling PaymentIntent.
        :return:PaymentIntent details with cancellation status or error message.
        """
        try:
            payment_intent = request.data.get(constants.PARAM_PAYMENT_INTENT_ID)
            if not payment_intent:
                return ApiResponse(status=0,
                                   message=constants.MISSING_PARAM.format(
                                       constants.PARAM_PAYMENT_INTENT_ID)).create_response()
            intent = stripe.PaymentIntent.cancel(payment_intent)
            data = {'cancel_intent': intent}
            api_response = ApiResponse(status=1, data=data,
                                       message=constants.CANCEL_PAYMENT_INTENT_SUCCESS,
                                       http_status=status.HTTP_200_OK)
            return api_response.create_response()
        except Exception as e:
            logger.exception("CancelPaymentIntent post exception {}".format(e))
            api_response = ApiResponse(status=0, message=constants.CANCEL_PAYMENT_INTENT_FAIL,
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return api_response.create_response()


class CardManagement(APIView):
    """
    Class is used to Create,retrieved,update,delete Card objects.
    """

    def get(self, request):
        """
        Function is used to get all cards details of a user & return the details.
        :param request: request header with required info.
        :return: all cards list with json
        """
        try:
            customer_id = request.user.customer_id
            if customer_id is None:
                return ApiResponse(status=0,
                                   message=constants.MISSING_CUSTOMER_ID,
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            card_list = stripe.Customer.list_sources(
                customer_id,
                object="card",
            )
            api_response = ApiResponse(status=1, data=card_list,
                                       message=constants.GET_ALL_CARD_SUCCESS,
                                       http_status=status.HTTP_200_OK)
            return api_response.create_response()
        except Exception as e:
            logger.exception("CardManagement get exception {}".format(e))
            api_response = ApiResponse(status=0, message=constants.GET_ALL_CARD_FAIL,
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return api_response.create_response()

    def post(self, request):
        """
        Function is used to Create Card objects of a user/customer & return the details.
        :param request: request header with required info.
        :return: card details with json or error message.
        """
        try:
            user_obj = request.user
            source_id = request.data.get(constants.PARAM_SOURCE_ID)
            if not source_id:
                return ApiResponse(status=0,
                                   message=constants.MISSING_PARAM.format(
                                       constants.PARAM_SOURCE_ID),
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            if user_obj.customer_id is None:
                customer = stripe.Customer.create(
                    name=user_obj.username,
                    email=user_obj.email,
                    phone=user_obj.phone_number,
                )
                user_obj.customer_id = customer['id']
                user_obj.save()
            customer_id = user_obj.customer_id
            token_obj = stripe.Token.retrieve(
                source_id,
            )
            fingerprint = token_obj.card.fingerprint
            card_list = stripe.Customer.list_sources(
                customer_id,
                object="card",
            )
            for card in card_list:
                if fingerprint == card.fingerprint:
                    api_response = ApiResponse(status=0,
                                               message=constants.CARD_ALREADY_EXIST,
                                               http_status=status.HTTP_400_BAD_REQUEST)
                    return api_response.create_response()
            new_card = stripe.Customer.create_source(
                customer_id,
                source=source_id,
            )
            api_response = ApiResponse(status=1, data=new_card,
                                       message=constants.CREATE_CARD_SUCCESS,
                                       http_status=status.HTTP_200_OK)
            return api_response.create_response()
        except Exception as e:
            logger.exception("CardManagement post exception {}".format(e))
            api_response = ApiResponse(status=0, message=constants.CREATE_CARD_FAIL,
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return api_response.create_response()

    def put(self, request):
        """
        Function is used to update Card objects of a user/customer & return the status.
        :param request: request header with required info.
        :return: card object with json
        """
        try:
            customer_id = request.user.customer_id
            card_id = request.data.get(constants.PARAM_CARD_ID)
            card_holder_name = request.data.get(constants.PARAM_CARD_HOLDER_NAME)
            exp_month = request.data.get(constants.PARAM_EXP_MONTH)
            exp_year = request.data.get(constants.PARAM_EXP_YEAR)
            if customer_id is None:
                return ApiResponse(status=0,
                                   message=constants.MISSING_CUSTOMER_ID,
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            if not card_id:
                return ApiResponse(status=0,
                                   message=constants.MISSING_PARAM.format(
                                       constants.PARAM_CARD_ID),
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            update_card = stripe.Customer.modify_source(
                customer_id,
                card_id,
                name=card_holder_name,
                exp_month=exp_month,
                exp_year=exp_year,
            )
            api_response = ApiResponse(status=1, data=update_card,
                                       message=constants.UPDATE_CARD_SUCCESS,
                                       http_status=status.HTTP_200_OK)
            return api_response.create_response()
        except Exception as e:
            logger.exception("CardManagement put exception {}".format(e))
            api_response = ApiResponse(status=0, message=constants.UPDATE_CARD_FAIL,
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return api_response.create_response()

    def delete(self, request):
        """
        Function is used to delete Card objects of a user/customer & return the status.
        :param request: request header with required info.
        :return: card id,object & status with json
        """
        try:
            customer_id = request.user.customer_id
            card_id = request.data.get(constants.PARAM_CARD_ID)
            if customer_id is None:
                return ApiResponse(status=0,
                                   message=constants.MISSING_CUSTOMER_ID,
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            if not card_id:
                return ApiResponse(status=0,
                                   message=constants.MISSING_PARAM.format(
                                       constants.PARAM_CARD_ID),
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            delete_card = stripe.Customer.delete_source(
                customer_id,
                card_id,
            )
            api_response = ApiResponse(status=1, data=delete_card,
                                       message=constants.DELETE_CARD_SUCCESS,
                                       http_status=status.HTTP_200_OK)
            return api_response.create_response()
        except Exception as e:
            logger.exception("CardManagement delete exception {}".format(e))
            api_response = ApiResponse(status=0, message=constants.DELETE_CARD_FAIL,
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return api_response.create_response()


class DefaultCard(APIView):
    """
    Class is used to Set/Get Default Card objects.
    """

    def get(self, request):
        """
        Function is used to get default card of a customer & return the card id.
        :param request: request header with required info.
        :return: card id with json
        """
        try:
            customer_id = request.user.customer_id
            if customer_id is None:
                return ApiResponse(status=0,
                                   message=constants.MISSING_CUSTOMER_ID,
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            default_card = stripe.Customer.retrieve(
                customer_id
            )
            api_response = ApiResponse(status=1, data=default_card.default_source,
                                       message=constants.DEFAULT_CARD_SUCCESS,
                                       http_status=status.HTTP_200_OK)
            return api_response.create_response()
        except Exception as e:
            logger.exception("DefaultCard get exception {}".format(e))
            api_response = ApiResponse(status=0, message=constants.DEFAULT_CARD_FAIL,
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return api_response.create_response()

    def post(self, request):
        """
        Function is used to Set Default Card of a user/customer & return the details.
        :param request: request header with required info.
        :return: card details with json
        """
        try:
            customer_id = request.user.customer_id
            card_id = request.data.get(constants.PARAM_CARD_ID)
            if not card_id:
                return ApiResponse(status=0,
                                   message=constants.MISSING_PARAM.format(
                                       constants.PARAM_CARD_ID),
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            if customer_id is None:
                return ApiResponse(status=0,
                                   message=constants.MISSING_CUSTOMER_ID,
                                   http_status=status.HTTP_404_NOT_FOUND).create_response()
            set_default_card = stripe.Customer.modify(
                customer_id,
                default_source=card_id,
            )
            api_response = ApiResponse(status=1, data=set_default_card,
                                       message=constants.SET_DEFAULT_CARD_SUCCESS,
                                       http_status=status.HTTP_200_OK)
            return api_response.create_response()
        except Exception as e:
            logger.exception("DefaultCard post exception {}".format(e))
            api_response = ApiResponse(status=0, message=constants.SET_DEFAULT_CARD_FAIL,
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return api_response.create_response()


class WebhookView(APIView):
    """
    Class is used to handle the Stripe events.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Function is used to handle the events and return status.
        :param request:request header with required info.
        :return:Success message with status or error message.
        """
        try:
            payload = request.body
            sig_header = request.META['HTTP_STRIPE_SIGNATURE']
            endpoint_secret = stripe_webhook_secret
            event = None
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, endpoint_secret
                )
            except ValueError as e:
                # Invalid payload
                logger.exception("WebhookView post ValueError exception {}".format(e))
                return HttpResponse(status=400)
            except stripe.error.SignatureVerificationError as e:
                # Invalid signature
                logger.exception("WebhookView post SignatureVerificationError exception {}".format(e))
                return HttpResponse(status=400)
            # Handle the event
            if event.type == 'payment_intent.succeeded':
                payment_intent_success = event.data.object

            elif event.type == 'payment_intent.payment_failed':
                payment_intent_fail = event.data.object

            elif event.type == 'charge.refunded':
                refund_update = event.data.object

            elif event.type == 'charge.refund.updated':
                refund_update = event.data.object

            return HttpResponse(status=200)

        except Exception as e:
            logger.exception("WebhookView post exception {}".format(e))
            return HttpResponse(status=400)
