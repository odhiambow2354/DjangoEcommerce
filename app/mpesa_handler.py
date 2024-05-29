import time
import os
import requests
import base64
import math
import json
from datetime import datetime
from requests.auth import HTTPBasicAuth


class MpesaHandler:
    now = None
    shortcodes = None
    consumer_key = None
    consumer_secret = None
    access_token = None
    access_token_url = None
    stkpush_url = None
    my_callback_url = None
    passkey = None
    timestamp = None
    query_status_url = None

    def __init__(self):
        self.now = datetime.now()
        self.shortcodes = os.getenv('SHORTCODES')  # Using os.getenv
        self.consumer_key = os.getenv('CONSUMER_KEY')
        self.consumer_secret = os.getenv('CONSUMER_SECRET')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_url = os.getenv('ACCESS_TOKEN_URL')
        self.stkpush_url = os.getenv('STKPUSH_URL')
        self.my_callback_url = os.getenv('MY_CALLBACK_URL')
        self.passkey = os.getenv('PASSKEY')
        self.timestamp = self.now.strftime('%Y%m%d%H%M%S')
        self.query_status_url = os.getenv('QUERY_STATUS_URL')
        self.password =self.generate_password()

        try:
            self.access_token = self.get_mpesa_access_token()

            if self.access_token is None:
                raise Exception("Access token not generated")
            else:
                self.access_token_expiration = time.time() + 3599

        except Exception as e:
            # Log the error
            print(str(e))

    def get_mpesa_access_token(self):
        try:
            response = requests.get(self.access_token_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
            data = response.json()
            access_token = data['access_token']

            self.headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

        except Exception as e:
            # Log the error
            print(str(e), 'Error getting access token')
            raise e
        return access_token
    
    def generate_password(self):
        self.timestamp = self.now.strftime('%Y%m%d%H%M%S')
        password_str = f'{self.shortcodes}{self.passkey}{self.timestamp}'
        password_bytes = password_str.encode('utf-8')

        return base64.b64encode(password_bytes).decode('utf-8')
    
    def make_stk_push(self, payload):
        amount = payload['amount']
        phone_number = payload['phone_number']

        push_data = {
            "BusinessShortCode": self.shortcodes,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcodes,
            "PhoneNumber": phone_number,
            "CallBackURL": self.my_callback_url,
            "AccountReference": "DairyProducts",
            "TransactionDesc": "confirm payment of dairy products"
        }

        response = requests.post(
            self.stkpush_url, 
            headers=self.headers, 
            json=push_data)
        
        response_data = response.json()
        return response_data
    
    def query_transaction_status(self, checkout_request_id):
        query_data = {
            "BusinessShortCode": self.shortcodes,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        response = requests.post(
            self.query_status_url, 
            headers=self.headers, 
            json=query_data)
        
        response_data = response.json()
        return response_data
 

