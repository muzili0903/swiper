# Python原生的
import random

# Python第三方的
import requests
from django.core.cache import cache

# Python个人定义的
from swiper import config
from worker import call_by_worker


def gen_verify_code(length=6):
    '''产生一个验证码'''
    return random.randrange(10 ** (length - 1), 10 ** length)


@call_by_worker
def send_verify_code(phonenum):
    '''发送验证码'''
    vcode = gen_verify_code()
    key = 'VerifyCode-%s' % phonenum
    cache.set(key, vcode, 120)
    sms_cfg = config.HY_SMS_PARAMS.copy()
    sms_cfg['param'] = sms_cfg['param'] % vcode
    sms_cfg['mobile'] = phonenum
    response = requests.post(config.HY_SMS_URL, json=sms_cfg)
    return response


def check_vcode(phonenum, vcode):
    '''检查验证码是否正确'''
    key = 'VerifyCode-%s' % phonenum
    saved_vcode = cache.get(key)
    return saved_vcode == vcode
