from django.db import models
from django.db.models import Q

from user.models import User


class Swiperd(models.Model):
    '''滑动记录'''
    STATUS = (
        ('superlike', '超级喜欢'),
        ('like', '喜欢'),
        ('dislike', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动者的 UID')
    sid = models.IntegerField(verbose_name='被滑动者的 UID')
    status = models.CharField(max_length=8, choices=STATUS)
    time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def mark(cls, uid, sid, status):
        '''标记一次滑动'''
        if status in ['superlike', 'like', 'dislike']:
            defaults = {'status': status}
            cls.objects.update_or_create(uid=uid, sid=sid, status=defaults)

    @classmethod
    def is_liked(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid, status__in=['like', 'superlike']).exists()

    @classmethod
    def delete_mark(cls, uid, sid):
        condition = Q(uid=uid, sid=sid) | Q(uid=sid, sid=uid)
        cls.objects.filter(condition).delete()


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def be_friends(cls, uid, sid):
        '''成为好友关系'''
        uid1, uid2 = (uid, sid) if uid < sid else (sid, uid)
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)

    @classmethod
    def break_off(cls, uid, sid):
        '''绝交'''
        uid1, uid2 = (uid, sid) if uid < sid else (sid, uid)
        try:
            cls.objects.get(uid1=uid1, uid2=uid2).delete()
        except cls.DoesNotExist:
            pass

    @classmethod
    def friends(cls, uid):
        condition = Q(uid1=uid) | Q(uid2=uid)
        relations = cls.objects.filter(condition)

        friend_id_list = []
        for r in relations:
            friend_id = r.uid1 if r.uid2 == uid else r.uid2
            friend_id_list.append(friend_id)
        return User.objects.filter(id__in=friend_id_list)

    @classmethod
    def delete_friend(cls,uid, sid):
        condition = Q(uid1=sid, uid2=uid) | Q(uid2=sid, uid1=uid)
        cls.objects.filter(condition).delete()
