from django.shortcuts import render

from .logic import send_verify_code

def get_verify_code(request):
    '''手机注册'''
    phonenum = request.GET.get('phonenum', '')
    send_verify_code(phonenum)
    pass


def login(request):
    '''短信验证登录'''
    pass


def get_profile(request):
    '''获取个人资料'''
    pass


def modify_profile(request):
    pass


def upload_avatar(request):
    pass
