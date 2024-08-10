from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.dispatch import receiver



@receiver(user_logged_in,sender=User)
def login_success(request,sender,user,**kwargs):
    ip=request.META.get('REMOTE_ADDR')             #used to get ip address
    request.session['ip']=ip