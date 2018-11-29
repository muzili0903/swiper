from lib.http import render_json
from user.models import User
from user.logic import send_verify_code, check_vcode
from common import error


def get_verify_code(request):
    '''手机注册'''
    phonenum = request.POST.get('phonenum', '')
    send_verify_code(phonenum)
    return render_json(None, 0)


def login(request):
    '''短信验证登录'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    if check_vcode(phonenum, vcode):
        user, created = User.objects.get_or_create(phonenum=phonenum)
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        return render_json(None, error.VCODE_ERROR)



def get_profile(request):
    '''获取个人资料'''
    user = request.user
    return render_json(user.profile.to_dict())


def modify_profile(request):
    '''修改个人资料'''
    pass


def upload_avatar(request):
    '''头像上传'''
    pass
