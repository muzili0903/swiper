import datetime

from user.models import User
from social.models import Swiperd, Friend


def get_rcmd_users(user):
    '''
    获取用户列表
    :param user:
    :return:

       max_year        min_year     current_year
    ----|-----------------|----------------|--------------|-------->
                                          2018           2019
    '''
    sex = user.profile.dating_sex
    location = user.profile.location
    min_age = user.profile.min_dating_age
    max_age = user.profile.max_dating_age

    current_year = datetime.date.today().year
    min_year = current_year - min_age
    max_year = current_year - max_age

    users = User.objects.filter(sex=sex, location=location,
                                birth_year__gte=max_year,
                                birth_year__lte=min_year)

    return users

def like(user, sid):
    '''喜欢一个用户'''
    Swiperd.mark(user.id, sid, 'like')
    if Swiperd.is_liked(sid, user.id):
        Friend.be_friends(user.id, sid)
        return True
    else:
        return False


def superlike(user, sid):
    Swiperd.mark(user.id, sid, 'superlike')
    if Swiperd.is_liked(sid, user.id):
        Friend.be_friends(user.id, sid)
        return True
    else:
        return False


def dislike(user, sid):
    Swiperd.mark(user.id, sid, 'dislike')


def rewind(user, sid):
    try:
        Swiperd.objects.get(uid=user.id, sid=sid).delete()
    except Swiperd.DoesNotExist:
        pass
    Friend.break_off(user.id, sid)

