import requests
from django.conf import settings
import base64
from datetime import datetime

def generate_access_token():
    """
    Generates an access token for M-Pesa API interactions.
    """
    consumer_key = settings.env('CONSUMER_KEY')
    consumer_secret = settings.env('CONSUMER_SECRET')
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # Sandbox environment

    auth_string = f"{consumer_key}:{consumer_secret}"  # Base64 encode for Basic authorization
    encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': f'Basic {encoded_auth_string}'
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    data = response.json()
    return data["access_token"]

def initiate_stk_push(user, order, phone_number, amount):
    """
    Initiates an M-Pesa STK Push transaction for a given order.
    """
    access_token = generate_access_token()
    business_short_code = settings.MPESA_BUSINESS_SHORTCODE
    callback_url = settings.MPESA_CALLBACK_URL  # URL for M-Pesa confirmation callbacks

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # Sandbox environment

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "BusinessShortCode": business_short_code,
        "Password": "<Your Base64 Encoded Password>",  # Replace with your Base64 encoded password
        "Timestamp": datetime.utcnow().strftime("%Y%m%dT%H:%M:%S.%fZ"),  # Adjust format if needed
        "TransactionType": "CustomerPayBillOnline",  # Or "CustomerBuyGoodsOnline"
        "Amount": amount * 100,  # Amount in cents
        "PartyA": 254700000000,  # Replace with your Paybill number (optional)
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": f"ORDER_{order.id}",  # Order reference for your system
        "TransactionDesc": f"Payment for Order {order.id}"
    }

    response = requests.post(api_url, json=data, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    return response.json()

def generate_password(consumer_key, consumer_secret):
    """
    Generates a Base64 encoded password for M-Pesa API requests.
    """
    password_string = f"{consumer_key}{base64.b64encode(consumer_secret.encode('utf-8')).decode('utf-8')}"
    encoded_password = base64.b64encode(password_string.encode('utf-8')).decode('utf-8')
    return encoded_password

def get_current_timestamp():
    """
    Returns the current timestamp in ISO 8601 format (YYYYMMDDTHHMMSS.sssZ).
    """
    return datetime.utcnow().strftime("%Y%m%dT%H:%M:%S.%fZ")
