from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.slug} - {self.created}'
    def get_absolute_url(self):
        return reverse('home:detail', args=[self.id , self.slug])
    def like_count(self):
        return self.pvote.count()
    def user_can_like(self,user):
        if self.pvote.filter(user=user).exists():
            return True
        return False
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ucomment')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pcomment')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='rcomment',null=True,blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} posted {self.body[:30]}'
    
class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uvote')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pvote')

    def __str__(self):
        return f'{self.user} liked {self.post.slug[:10]}'
        