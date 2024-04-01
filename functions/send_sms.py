import os
from dotenv import load_dotenv
import requests

load_dotenv()

SUCCESS = 200
PROCESSING = 102
FAILED = 400
INVALID_NUMBER = 160
MESSAGE_IS_EMPTY = 170
SMS_NOT_FOUND = 404
SMS_SERVICE_NOT_TURNED = 600

ESKIZ_EMAIL = os.getenv('email')
ESKIZ_PASSWORD = os.getenv('password')


def limit():
    data = {
        'email': ESKIZ_EMAIL,
        'password': ESKIZ_PASSWORD,
    }
    AUTHORIZATION_URL = 'http://notify.eskiz.uz/api/auth/login'

    r = requests.request('POST', AUTHORIZATION_URL, data=data)
    token = r.json()['data']['token']

    CHECK_STATUS_URL = "http://notify.eskiz.uz/api/user/get-limit"

    HEADERS = {
        'Authorization': f'Bearer {token}'
    }
    r = requests.request("GET", CHECK_STATUS_URL, headers=HEADERS)
    return r.json()


def history(from_date, to_date):
    login = {
        'email': ESKIZ_EMAIL,
        'password': ESKIZ_PASSWORD,
    }

    AUTHORIZATION_URL = 'http://notify.eskiz.uz/api/auth/login'

    r = requests.request('POST', AUTHORIZATION_URL, data=login)
    token = r.json()['data']['token']

    CHECK_STATUS_URL = "http://notify.eskiz.uz/api/message/sms/get-user-messages"

    payload = {'from_date': from_date,
               'to_date': to_date,
               'user_id': '1'
               }

    HEADERS = {
        'Authorization': f'Bearer {token}'
    }

    r = requests.request("GET", CHECK_STATUS_URL, headers=HEADERS, data=payload)
    return r


class SendSmsApiWithEskiz:
    def __init__(self, message, phone, email=ESKIZ_EMAIL, password=ESKIZ_PASSWORD):
        self.message = message
        self.phone = phone
        self.spend = None
        self.email = email
        self.password = password

    def send(self):
        status_code = self.custom_validation()
        if status_code == SUCCESS:
            result = self.calculation_send_sms(self.message)
            if result == SUCCESS:
                return self.send_message(self.message)
            else:
                return result
        return status_code

    def custom_validation(self):
        if len(str(self.phone)) < 1:
            return INVALID_NUMBER
        if self.message == '' or not self.message:
            return MESSAGE_IS_EMPTY
        return SUCCESS

    def authorization(self):
        data = {
            'email': self.email,
            'password': self.password,
        }

        AUTHORIZATION_URL = 'http://notify.eskiz.uz/api/auth/login'

        r = requests.request('POST', AUTHORIZATION_URL, data=data)
        if r.json()['data']['token']:
            return r.json()['data']['token']
        else:
            return FAILED

    def send_message(self, message):
        token = self.authorization()
        if token == FAILED:
            return FAILED

        SEND_SMS_URL = "http://notify.eskiz.uz/api/message/sms/send"

        PAYLOAD = {
            'mobile_phone': str(self.phone),
            'message': message,
            'from': '4546',
            # 'callback_url': 'http://afbaf9e5a0a6.ngrok.io/sms-api-result/'
        }

        FILES = [

        ]
        HEADERS = {
            'Authorization': f'Bearer {token}'
        }
        r = requests.request("POST", SEND_SMS_URL, headers=HEADERS, data=PAYLOAD, files=FILES)
        print(f"Eskiz: {r.json()}")
        return r

    def calculation_send_sms(self, message):
        try:
            length = len(message)
            if length:
                if length >= 0 and length <= 160:
                    self.spend = 1
                elif length > 160 and length <= 306:
                    self.spend = 2
                elif length > 306 and length <= 459:
                    self.spend = 3
                elif length > 459 and length <= 612:
                    self.spend = 4
                elif length > 612 and length <= 765:
                    self.spend = 5
                elif length > 765 and length <= 918:
                    self.spend = 6
                elif length > 918 and length <= 1071:
                    self.spend = 7
                elif length > 1071 and length <= 1224:
                    self.spend = 8
                else:
                    self.spend = 30

                print(f"spend: {self.spend}")

                return SUCCESS
        except Exception as e:
            print(e)
            return FAILED

