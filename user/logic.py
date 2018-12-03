# Python原生的
import os
import random
from urllib.parse import urljoin

# Python第三方的
import requests
from django.core.cache import cache

# Python个人定义的
from lib.qncloud import async_upload_to_qiniu
from swiper import config
from worker import call_by_worker
from swiper import settings


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

def save_upload_file(user, upload_file):
    '''保存上传文件，并上传到七牛云'''
    # 获取文件并保存到本地
    ext_name = os.path.splitext(upload_file.name)[-1]
    filename = 'Avator-%s%s' % (user.id, ext_name)
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, filename)

    with open(filepath, 'wb') as newfile:
        for chunk in upload_file.chunks():
            newfile.write(chunk)

    # 异步将头像传到七牛云
    async_upload_to_qiniu(filepath, filename)

    # 保存URL到数据库
    url = urljoin(config.QN_BASE_URL, filename)
    user.avatar = url
    user.save()
