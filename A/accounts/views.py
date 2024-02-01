from django.shortcuts import render,redirect
from django.views import View
from . import forms
from .models import Relation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_view

class UserRegisterView(View):
    form_class=forms.UserRegisterForm
    template_name = 'accounts/register.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)


    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            User.objects.create_user(username=cd['username'],email=cd['email'],password=cd['password1'])
            messages.success(request,'your account Registered successfully:)))','success')
            return redirect('home:home')
        return render(request,self.template_name,{'form':form})

    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
class UserLoginView(View):
    form_class = forms.UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'your account logged in successfully:)))','success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request,'your password or username is not correct:(((','danger')
        return render(request,self.template_name,{'form':form})
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
class UserLogoutView(LoginRequiredMixin,View):
    login_url='/accounts/login/'
    def get(self,request):
        logout(request)
        messages.success(request,'your account logged out successfully:)))','success')
        return redirect('home:home')
class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(id = user_id)
        is_following=False
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            is_following=True
        posts = user.posts.all()
        return render(request,'accounts/profile.html',{'user':user , 'posts':posts,'is_following':is_following})
class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'
class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
class UserFollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        relation = Relation.objects.filter(from_user = request.user,to_user=User.objects.get(id=user_id))
        if relation.exists():
            messages.error(request,'already you have followed','danger')
        else:
            Relation(from_user = request.user,to_user=User.objects.get(id=user_id)).save()
            messages.success(request,'you followed successfully','success')
        return redirect('accounts:profile' , user_id)
    

class UserUnfollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request,'this user unfollowed successfully','success')
        else:
            messages.error(request,'you didn\'t follow this user yet','danger')
        return redirect('accounts:profile', user_id)

class EditProfileView(LoginRequiredMixin,View):
    form_class = forms.EditProfileForm

    def get(self,request):
        form = self.form_class(instance = request.user.profile,initial = {'email':request.user.email})
        return render(request,'accounts/edit_profile.html',{'form':form})
    def post(self,request):
        form = self.form_class(request.POST,instance = request.user.profile,initial = {'email':request.user.email})
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request,'your profile edited successfully','success')
        return redirect('accounts:profile', request.user.id)
        
        

