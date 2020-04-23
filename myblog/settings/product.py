from .base import * #NOQA

DEBUG=False

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