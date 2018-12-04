from lib.http import render_json
from social import logic
from social.models import Friend, Swiperd
from vip.logic import perm_require


def get_users(request):
    '''获取推荐列表'''
    users = logic.get_rcmd_users(request.user)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logic.like(request.user, sid)
    return render_json({'is_matched': is_matched})


@perm_require('superlike')
def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logic.superlike(request.user, sid)
    return render_json({'is_matched': is_matched})


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    logic.dislike(request.user, sid)
    return render_json(None)


@perm_require('rewind')
def rewind(request):
    '''反悔'''
    sid = int(request.POST.get('sid'))
    logic.rewind(request.user, sid)
    return render_json(None)


def friends(request):
    '''好友列表'''
    my_friend = Friend.friends(request.user.id)
    friends_info = [friend.to_dict() for friend in my_friend]
    return render_json({'friend': friends_info})


def delete(request):
    sid = request.POST.get('sid')
    Friend.delete_friend(request.user.id, sid)
    Swiperd.delete_mark(request.user.id, sid)
    return render_json(None)
