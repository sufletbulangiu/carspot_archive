from django.urls import path
#from . import views
from .views import HomeView, AddPostView, UpdatePostView, DeletePostView, AddCategoryView, CategoryView, AboutView, SearchView, ListingsView, ArticleDetailsView, ContactView, MyListingsView
#from . import views

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('about_us/', AboutView.as_view(), name="about"),
    path('item/<int:pk>', ArticleDetailsView.as_view(), name='item_detail'),
    path('add_item/', AddPostView.as_view(), name='add_item'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('update_item/edit/<int:pk>', UpdatePostView.as_view(), name='update_item'),
    path('delete_item/<int:pk>', DeletePostView.as_view(), name='delete_item'),
    path('category/<str:cats>/', CategoryView, name='category'),
    #path('search', views.SearchView, name='search_items'),
    path('search/', SearchView.as_view(), name='search_items'),
    path('listings/', ListingsView.as_view(), name='all_items'),
    path('contact_us/', ContactView.as_view(), name='contact'),
    path('my_listings/', MyListingsView.as_view(), name='user_items'),
    #path('item/<int:pk>', views.formDetailView, name='item_detail'),
    

]
handler404 = 'webside_side.views.error_404_view'