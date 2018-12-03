import datetime

from user.models import User
from social.models import Swiperd

def get_rcmd_users(user):
    '''
    获取用户列表
    :param user:
    :return:
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
                                birth_day__lte=min_year)

    return users