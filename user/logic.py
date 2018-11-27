# Python原生的
import random

# Python第三方的
import requests

# Python个人定义的
from swiper import config


def gen_verify_code(length=6):
    '''产生一个验证码'''
    return random.randrange(10 ** (length -1), 10**length)


def send_verify_code(phonenum):
    vcode = gen_verify_code()
    sms_cfg = config.HY_SMS_PARAMS.copy()
    sms_cfg['content'] = config.HY_SMS_PARAMS % vcode
    sms_cfg['mobile'] = config.HY_SMS_PARAMS % phonenum
    response = requests.post(config.HY_SMS_URL, data=sms_cfg)
    return response
