"""
Django settings for cr_backend project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

PAGES = 30

# 发送邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# SMTP地址
EMAIL_HOST = 'smtp.163.com'
# SMTP端口
EMAIL_PORT = 465
# 自己的邮箱
EMAIL_HOST_USER = '13652831404@163.com'
# 自己的邮箱授权码，非密码
EMAIL_HOST_PASSWORD = 'LUICSMSJSIJAWWRG'

EMAIL_SUBJECT_PREFIX = '[招新通]'
# 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = '13652831404@163.com'

DEFAULT_IMG = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:' \
              'ANd9GcR1ks4rXUNoVTm_y7GtSfvDIpfrDORnuQYONBNV4wPDFV0dl8E&s'

REP_STATUS = {
    100: dict(code=100, message='正常'),
    101: dict(code=101, message='token错误'),
    110: dict(code=110, message='token过期'),
    111: dict(code=111, message='请求类型错误'),
    200: dict(code=200, message='登陆时手机号或密码错误'),
    201: dict(code=201, message='注册错误，手机号已被注册'),
    210: dict(code=210, message='无验证头部或验证类型错误'),
    211: dict(code=211, message='请求目标不存在'),
    300: dict(code=300, message='请求字段错误或为空'),
    301: dict(code=301, message='请求内容无数据'),
    310: dict(code=310, message='密码错误'),
    311: dict(code=311, message='时间设置错误'),
    400: dict(code=400, message='数据重复'),
    401: dict(code=401, message='游客不可登录'),

    666: dict(code=666, message='未知错误')
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 媒体文件地址
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
WEB_PATH = 'https://re.boycharse.top/clubRecruitment/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i!_d+iyptw!y22+ihpi7l_7)0gr47819^6bht@!g#owmb9c%pf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", ]


# Application definition

INSTALLED_APPS = [
    'clubRecruitment.apps.ClubrecruitmentConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cr_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cr_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': 'utils/dbs/my.cnf',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
