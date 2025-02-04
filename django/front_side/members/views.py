from django.views import generic
from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfile, PasswordChangingForm
from webside_side.models import Profile, Post, WebSiteName
from django.db.models import Q

# Create your views here.

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/profile.html'
    #slug_field = 'user'

    def get_context_data(self, *args, **kwargs):
        try:
            products = Post.objects.all()
            webname = WebSiteName.objects.first()
            products_active = products.filter(Q(author=self.kwargs['pk']) & Q(itemStatus='Active')).count()
            products_inactive = products.filter(Q(author=self.kwargs['pk']) & Q(itemStatus='Inactive')).count()
            products_featured = products.filter(Q(author=self.kwargs['pk']) & Q(featured='Yes')).count()
            products_sold = products.filter(Q(author=self.kwargs['pk']) & Q(itemStatus='Sold')).count()
            context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
            data = {'webname': webname}
            context['products_active'] = products_active
            context['products_inactive'] = products_inactive
            context['products_featured'] = products_featured
            context['products_sold'] = products_sold 
            context['data'] = data   
        except Post.DoesNotExist:
                context = super(ShowProfilePageView, self).get_context_data(**kwargs)
        return context    


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('pass_success')

def password_success(request):
    return render(request, 'registration/pass_success.html', {})

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditProfile
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

