from django.db import models
import jwt
from cr_backend import settings
from datetime import datetime, timedelta
from django.conf import settings


class User(models.Model):
    user_name = models.CharField(max_length=200)
    pass_word = models.CharField(max_length=200)
    stu_id = models.CharField(max_length=200)
    pho_num = models.CharField(max_length=200)

    class Meta:
        # 抽象类不产生数据
        abstract = True

    def __str__(self):
        return self.stu_id

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=10),
            'iat': datetime.utcnow(),
            'data': {
                'id': self.pk
            }
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Admin(User):
    """
    管理员
    """


class Student(User):
    """
    学生
    """
    college = models.CharField(max_length=200)
    stu_class = models.CharField(max_length=200)
    mailbox = models.CharField(max_length=200)
    school = models.CharField(max_length=200, default='')


class Club(models.Model):
    """
    社团
    """
    club_name = models.CharField(max_length=200, default='')
    school = models.CharField(max_length=200, default='')
    club_desc = models.TextField()
    Admin = models.ForeignKey('Admin', on_delete=models.CASCADE)

    def __str__(self):
        return self.club_name


class Recruitment(models.Model):
    stu_name = models.CharField(max_length=200, default='')
    stu_id = models.CharField(max_length=200, default='')
    pho_num = models.CharField(max_length=200, default='')
    mailbox = models.CharField(max_length=200, default='')
    stu_desc = models.TextField()
    Club = models.ForeignKey('Club', on_delete=models.CASCADE)
    Student = models.ForeignKey('Student', on_delete=models.CASCADE)


class Notice(models.Model):
    Club = models.ForeignKey('Club', on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.TextField()
    title = models.CharField(max_length=200, default='')




