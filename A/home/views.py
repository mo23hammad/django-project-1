from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Post,Comment,Vote
from django.contrib import messages
from .forms import PostCreateUpdateForm , PostCommentForm , CommentReplyForm , PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    form_class = PostSearchForm

    def get(self,request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request,'home/index.html',{'posts':posts,'form':self.form_class})
    
    
class PostView(View):
    form_class = PostCommentForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args , **kwargs):
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        comments = self.post_instance.pcomment.filter(is_reply=False)
        return render(request, 'home/detail.html', {'post': self.post_instance, 'comments': comments,'form':self.form_class(),'reply_form':self.form_class_reply(),'can_like':can_like})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request,'your comment submitted successfully','success')
            return redirect('home:detail',self.post_instance.id , self.post_instance.slug)
    
class DeletePostView(LoginRequiredMixin,View):

    def get(self,request,post_id,post_slug):
        post=get_object_or_404(Post,pk=post_id,slug=post_slug)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request,'your post deleted successfully','success')
        else:
            messages.error(request,'you cant delete this file','danger')
        return redirect('home:home')
    

class UpdatePostView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get()
        if not request.user.id == post.user.id:
            messages.error(request, 'You can\'t update this post', 'danger')
            return redirect('home:home') 
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)  
        return render(request, self.template_name, {'form': form, 'post': post})

    def post(self,request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST,instance=post)  
        if form.is_valid():
            post=form.save(commit=False)
            post.slug=slugify(form.cleaned_data['body'][:30])
            post.save()
            messages.success(request,'your post updated successfully','success')
        return redirect('home:detail',post.id,post.slug)
    

class CreatePostView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm
    def get(self,request):
        form = self.form_class()
        return render(request,'home/create.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request,'your post created successfully','success')
            return redirect('home:detail',new_post.id,new_post.slug)

class ReplyPostView(LoginRequiredMixin,View):
    form_class = CommentReplyForm
    
    def post(self,request,post_id,comment_id):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post,id = post_id)
        comment = get_object_or_404(Comment,id = comment_id)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request,'your reply submitted successfully','success')
        return redirect('home:detail', post.id,post.slug)

class LikePostView(LoginRequiredMixin,View):
    
    def get(self,request,post_id):
        post = get_object_or_404(Post,id=post_id)
        like = Vote.objects.filter(post=post,user=request.user)
        if like.exists():
            messages.error(request,'you liked this post befor','danger')
        else:
            Vote.objects.create(post=post,user=request.user)
            messages.success(request,'you liked this post','success')
        return redirect('home:detail',post.id,post.slug)
