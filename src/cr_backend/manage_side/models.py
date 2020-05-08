from django.db import models
import jwt
from cr_backend import settings
from datetime import datetime, timedelta
from django.conf import settings


class User(models.Model):
    user_name = models.CharField(max_length=200)
    pass_word = models.CharField(max_length=200)
    shool = models.CharField(max_length=200)
    club_name = models.CharField(max_length=200)
    stu_id = models.CharField(max_length=200)
    pho_num = models.CharField(max_length=200)

    def __str__(self):
        return self.stu_id

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'data': {
                'pho_num': self.pho_num
            }
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


