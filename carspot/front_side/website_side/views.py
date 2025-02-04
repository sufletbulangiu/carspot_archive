from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.views.generic.edit import FormView
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category
from django.views import View
from .forms import PostForm, EditForm, ContactForm, EmailForm
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def error_404_view(request, exception):
    return render(request, '404.html')


def SearchView(request):
    print('muie')
    if request.method == "POST":
        print(request.POST['searched'])
        searched = request.POST['searched']
        items = Post.objects.filter(title__contains=searched)
        return render(request, 'search.html', {'searched': searched, 'items': items})
    else:

        return render(request, 'search.html', {})



def CategoryListView(request, cats):
    cat_menu_list = Category.objects.all()
    return render(request, 'categories_list.html', {'cat_menu_list':cat_menu_list})         

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    cat_menu = Category.objects.all()    
    test = Post.objects.count()
    print(test)
    print(cats)
    return render(request, 'categories.html', {'cats': cats.title(), 'category_posts': category_posts, 'cat_menu': cat_menu })  


def ContactView(request):
    cat_menu = Category.objects.all() 
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email, ["admin@example.com"])
            except BadHeaderError:  
                return HttpResponse("Invalid header found.")
            return redirect("contact")
    return render(request, 'contact.html', {'cat_menu': cat_menu, "form": form }) 

       
# HOME
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    paginate_by = 10
    queryset = Post.objects.order_by('-date')[:10]

    def get_context_data(self, *args, **kwargs):
        print(self.kwargs)
        cat_menu = Category.objects.all() 
        #count_items = Post.objects.all().filter(itemStatus="Active").count()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        #context['count_items'] = count_items
        print(context)        
        return context


# LISTINGS
class ListingsView(ListView):
    model = Post
    template_name = "listings.html"
    paginate_by = 10
    #context_object_name = 'item_list'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all() 
        count_items = Post.objects.all().filter(itemStatus="Active").count()
        context = super(ListingsView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        context['count_items'] = count_items
        print(context)        
        return context


# ABOUT
class AboutView(ListView):
    model = Post
    template_name = 'about.html'  

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        #count_items = Post.objects.count()
        context = super(AboutView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        #context['count_items'] = count_items
        #print(context)        
        return context 


# CONTACT
class ContactView(ListView):

    model = Post
    template_name = 'contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.object_list = self.get_queryset()
        cat_menu = Category.objects.all()
        context = self.get_context_data(object_list=self.object_list, form=form)
        context['cat_menu'] = cat_menu
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list, form=form)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipients = ['to@example.com']
            send_mail(subject, message, email, recipients)
            return redirect(reverse('contact'))
        else:
            return self.render_to_response(context)        


# DETAIL - ITEM
class ArticleDetailsView(EmailForm,DetailView):
    model = Post
    template_name = 'details.html'
    #form_class = EmailForm
    paginate_by = 3
    #success_url = reversed('home')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = Post.objects.all().filter(itemStatus="Active")[:5]
        cat_menu = Category.objects.all()
        context = self.get_context_data(object=self.object)
        context['form'] = EmailForm()
        context['product'] = product
        context['cat_menu'] = cat_menu
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = EmailForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            author = form.cleaned_data['author']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            msg = f'Subject: {title} - {price}\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}'
            send_mail(f'Question {title}', msg, email, [author], fail_silently=True)
            return redirect(reverse('item_detail', args=[self.object.pk]))
        else:
            context['form'] = form
            return self.render_to_response(context)
          
  
# ADD ITEM 
class AddPostView(CreateView):
    model = Post  
    form_class = PostForm
    template_name = 'add_item.html'
    #fields = '__all__'
    #fields = ('title','location','price','description')

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        #count_items = Post.objects.count()
        context = super(AddPostView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        #context['count_items'] = count_items
        #print(context)        
        return context 

    def form_valid(self, form):
        print(form.changed_data)
        return super().form_valid(form)  


# UPDATE 
class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_item.html'
    #fields = '__all__'
   # fields =('title','location','author','price','description','make','year','bodytype','transmission','alloyWheels','abs','air','radio','cd','bonnet','airBags','coolBox','powerSteering')


# DELETE
class DeletePostView(DeleteView):
    model = Post
    #form_class = EditForm
    template_name = 'delete_item.html'
    success_url = reverse_lazy('home')


# CATEGORY  
class AddCategoryView(CreateView):
    model = Category #from models 
    # form_class = PostForm #from forms
    template_name = 'add_category.html'
    fields = '__all__'
    #fields = ('title','location','price','description')
   

# SEARCH   
class SearchView(ListView):
    model = Post
    template_name = "search.html"
    paginate_by = 2
    #context_object_name = 'item_list'
    #queryset = Post.objects.order_by('-date')[:3]

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get("search")
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        queryset = super().get_queryset()   
        print(queryset)     
        if self.query:
            queryset = queryset.filter(
                Q(title__icontains=self.query)
            )
        #print(f'aaaaaaaaaaaaaaaaaaaaaaaaaaaa{context}')
        print(f'a--->{queryset}')
        #context = queryset
        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        print(f'asdadas{self.object_list}')
        paginator = Paginator(self.object_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj
        print(context)
        return context        


    
    #queryset = Post.objects.order_by('-date')[:3]

    #def get(self, request, *args, **kwargs):
     #   name = request.GET.get('search', '')
        #print(f'GET: {name}')
      #  query = Post.objects.filter(title__contains=name)
       # paginator  = Paginator(query, 10)
        #page_number = request.GET.get('page', 1)
        #try:
        #    self.pagination = paginator.page(page_number)
        #except PageNotAnInteger:
        #    self.pagination = paginator.page(1)
        #except EmptyPage:
         #   self.pagination = paginator.page(paginator.num_pages)        
       
#        self.results = Post.objects.filter(title__contains=name)
        #self.results = Post.objects.filter(title__contains=name)
        #print(type(self.results))
        #print(f'aaaaaaaaaaaaaaaaaaa{aaa}')
        #context['plm'] aaa
        #return super().get(request, *args, **kwargs)

    #def get_context_data(self, **kwargs):
     #   """Add context to the template"""
      #  context = super().get_context_data(results=self.results, **kwargs)
       # context['pagina'] = super().get_context_data(pag=self.pagination, **kwargs)
        
        #print(f'AAAAAAAAAAAAA: {context}')
        #return context
    
 