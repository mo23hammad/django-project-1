from django.contrib.auth.models import User

class EmailBackend:
    def authenticate(self,request,username=None,password=None,**kwargs):
        try:
            user = User.objects.get()
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
    def get_user(self,user_id):
        try:
            return User.objects.get()
        except User.DoesNotExist:
            return None