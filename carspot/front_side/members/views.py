from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfile, PasswordChangingForm
from website_side.models import Profile, Post
from django.db.models import Q


# Create your views here.

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/profile.html'

    def get_context_data(self, *args, **kwargs):
        products = Post.objects.all()
        products_active = products.filter(Q(author=self.kwargs['pk']) & Q(itemStatus='Active')).count()
        products_inactive = products.filter(Q(author=self.kwargs['pk']) & Q(itemStatus='Inactive')).count()
        products_featured = products.filter(Q(author=self.kwargs['pk']) & Q(featured='Yes')).count()
        products_sold = products.filter(Q(author=self.kwargs['pk']) & Q(itemStatus='Sold')).count()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['products_active'] = products_active
        context['products_inactive'] = products_inactive
        context['products_featured'] = products_featured
        context['products_sold'] = products_sold
        print(context)        
        return context    


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'registration/change-password.html'
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

