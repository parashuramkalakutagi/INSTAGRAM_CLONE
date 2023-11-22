import  string
import requests
import random

api_key = '812bd357-09ad-11ee-addf-0200cd936042'
def send_otp_phone(phone_number):
    try:
        otp = random.randint(1000,9999)
        url = f'https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/'
        response = requests.get(url)
        return otp
    except Exception as e:
        return None


