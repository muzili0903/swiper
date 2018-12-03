

from lib.http import render_json
from social import logic

def get_users(request):
    '''获取推荐列表'''
    users = logic.get_rcmd_users(request.user)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    '''喜欢'''
    pass
    # return reder_json()


def superlike(request):
    '''超级喜欢'''
    pass
    # return reder_json()


def dislike(request):
    '''不喜欢'''
    pass
    # return reder_json()


def rewind(request):
    '''反悔'''
    pass
    # return reder_json()


def friends(request):
    '''好友列表'''
    pass
    # return reder_json()
