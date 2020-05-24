from .base import * #NOQA

DEBUG=False

ALLOWED_HOST=['196.168.248.128']

DATABASES={
    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':"myblog",
        'HOST':'127.0.0.1',
        "PORT":'3306',
        "USER":'lyp',
        "PASSWORD":'123456'
    }
}
