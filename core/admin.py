from django.contrib import admin
from .models import UserProfile, BuyProduct, Product, Category, Subscriber
from django.contrib.auth.models import Group, User
# from django.contrib.sites.models import Site

admin.site.site_header = "MnadaOnline Website Application"
admin.site.site_title = "MnadaOnline Admin Portal"
admin.site.index_title = "Welcome to MnadaOnline Admin Portal"

admin.site.register(UserProfile)
admin.site.register(BuyProduct)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Subscriber)

admin.site.unregister(Group)
# admin.site.unregister(User)
# admin.site.unregister(Site)
