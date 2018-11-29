# Python原生的
import random

# Python第三方的
import requests

# Python个人定义的
from swiper import config
from worker import call_by_worker


def gen_verify_code(length=6):
    '''产生一个验证码'''
    return random.randrange(10 ** (length -1), 10**length)


@call_by_worker
def send_verify_code(phonenum):
    vcode = gen_verify_code()
    sms_cfg = config.HY_SMS_PARAMS.copy()
    sms_cfg['content'] = sms_cfg['content'] % vcode
    sms_cfg['mobile'] = phonenum
    response = requests.post(config.HY_SMS_URL, json=sms_cfg)
    return response
