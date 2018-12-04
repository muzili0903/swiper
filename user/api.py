from lib.http import render_json
from user.models import User
from user.logic import send_verify_code, check_vcode, save_upload_file, change_perm_level
from common import error
from user.forms import ProfileForm
from vip.models import Vip


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
    form = ProfileForm(request.POST)
    if form.is_valid():
        user = request.user
        user.profile.__dict__.update(form.cleaned_data)
        user.profile.save()
        return render_json(None)
    else:
        return render_json(form.errors, error.PROFILE_ERROR)


def upload_avatar(request):
    '''头像上传'''
    file = request.FILES.get('avatar')
    if file:
        save_upload_file(request.user, file)
        return render_json(None)
    else:
        return render_json(None, error.FILE_NOT_FOUND)


def check_perm(request):
    '''检查用户权限'''
    user = request.user
    perms = user.vip.perms()
    perm_list = [perm.to_dict() for perm in perms]
    return render_json({'perm': perm_list})


def change_perm(request):
    '''修改用户权限'''
    price = int(request.POST.get('price'))
    level = change_perm_level(request.user, price)
    return render_json({'vip_level': level})
