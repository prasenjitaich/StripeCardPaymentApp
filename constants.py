# users

CREATE_USER_SUCCESS = "User created successfully."
UPDATE_USER_SUCCESS = "User updated successfully."
DELETE_USER_SUCCESS = "User deleted successfully."
GET_USER_SUCCESS = "User retrieved successfully."
USER_DOES_NOT_EXIST = "User does not exist."

# Payments
PARAM_PAYMENT_INTENT_ID = 'payment_intent'
PARAM_CARD_ID = "card_id"
PARAM_SOURCE_ID = "source_id"
PARAM_CARD_HOLDER_NAME = "name"
PARAM_EXP_MONTH = "exp_month"
PARAM_EXP_YEAR = "exp_year"
PARAM_NO_COUNT = "no_count"

MISSING_PARAM = "Request is missing required parameter {}"
STRIPE_SHIPPING_ADDRESS = {
    'name': 'Jenny Rosen',
    'address': {
        'line1': '510 Townsend St',
        'postal_code': '98140',
        'city': 'San Francisco',
        'state': 'CA',
        'country': 'US',
    },
}
STRIPE_DESCRIPTION = 'Software development services'
CREATE_PAYMENT_INTENT_SUCCESS = "Payment intent created successfully."
CREATE_PAYMENT_REFUND_SUCCESS = "Payment is refunded successfully."
PAYMENT_ALREADY_REFUND = "Payment is already refunded."
CANCEL_PAYMENT_INTENT_SUCCESS = "Payment intent is canceled successfully."
CREATE_PAYMENT_INTENT_FAIL = "Something went wrong could not create Payment intent."
CREATE_PAYMENT_REFUND_FAIL = "Something went wrong could not create Payment refund."
CANCEL_PAYMENT_INTENT_FAIL = "Something went wrong could not cancel Payment intent."

MISSING_CUSTOMER_ID = "User does not have any customer_id,please contact site maintainer."
GET_ALL_CARD_SUCCESS = "All cards retrieved successfully."
GET_ALL_CARD_FAIL = "Something went wrong could not get list of all card,please contact site maintainer."
CREATE_CARD_SUCCESS = "Card is created successfully."
CARD_ALREADY_EXIST = "Card with that number is already exist."
UPDATE_CARD_SUCCESS = "Card is updated successfully."
DELETE_CARD_SUCCESS = "Card is deleted successfully."
CREATE_CARD_FAIL = "Something went wrong could not create card,please contact site maintainer."
UPDATE_CARD_FAIL = "Something went wrong could not update card,please contact site maintainer."
DELETE_CARD_FAIL = "Something went wrong could not delete card,please contact site maintainer."
SET_DEFAULT_CARD_SUCCESS = "Set default card successfully."
SET_DEFAULT_CARD_FAIL = "Something went wrong could not set default card,please contact site maintainer."

DEFAULT_PRICE = 0.5
MIN_AMOUNT = 0.5
CONVERT_CENT = 100
DEFAULT_CARD_SUCCESS = "Default card retrieved successfully."
DEFAULT_CARD_FAIL = "Default card does not retrieved."
