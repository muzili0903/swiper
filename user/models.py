from django.db import models
from django.utils.functional import cached_property

import datetime


class User(models.Model):
    '''用户数据模型'''

    SEX = (
        ('M', '男'),
        ('F', '女'),
    )
    nickname = models.CharField(max_length=32, unique=True)
    phonenum = models.CharField(max_length=16, unique=True)

    sex = models.CharField(default='M', max_length=8, choices=SEX)
    avatar = models.CharField(max_length=256)
    location = models.CharField(max_length=32)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)

    @cached_property  # 只计算一次
    def age(self):
        today = datetime.date.today()
        birth_date = datetime.date(self.birth_year, self.birth_month, self.birth_day)
        times = today - birth_date
        return times.days // 365

    # 把方法属性化，变成只读属性
    @property  # 用户表的关联(手动构建关联，一对一的关联)
    def profile(self):
        '''用户的配置项'''
        # if '_profile' not in self.__dict__:
        if not hasattr(self, '_profile'):  # 判断是否有_profile这个属性，有返回True,没有返回False
            _profile, _ = Profile.objects.get_or_create(id=self.id)  # _ 接收一个值,但不使用
            self._profile = _profile
        return self._profile


class Profile(models.Model):
    '''用户配置'''

    SEX = (
        ('M', '男'),
        ('F', '女'),
    )

    location = models.CharField(max_length=32, verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=45, verbose_name='最大交友年龄')
    dating_sex = models.CharField(default='M', max_length=16, choices=SEX, verbose_name='匹配的性别')

    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matche = models.BooleanField(default=False, verbose_name='不让为匹配的人看我的相册')
    auto_play = models.BooleanField(default=False, verbose_name='自动播放视频')
