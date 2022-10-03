from django.contrib import admin
from . models import * # connecting the models here(the asterik means all instead of typing ' from . models import Category, Products ')


# This classes are created to created to modify the admin
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # We are connecting the slug field with the name so that, what we type in the name reflects in the slug field
    list_display = ['id', 'name', 'img'] # this organises how the registered category are displayed in the admin panel

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)} # We are connecting the slug field with the title so that, what we type in the title reflects in the slug field
    list_display = ['id', 'category', 'title', 'slug', 'pics', 'price', 'details', 'featured', 'latest'] # this organises how the registered products are displayed in the admin panel

class ContactAdmin(admin.ModelAdmin):
    # Fieldsets helps give a section a sub-heading
    fieldsets = [
        ('User', {'fields': ['full_name', 'email']}), #User is the sub-section, full_name and email will be found under it
        ('Messages', {'fields': ['message', 'admin_note']}), #messages is the sub-section, message and admin_note will be found under it
    ]
    list_display = ['id', 'full_name', 'email'] # this organises how the registered products are displayed in the admin panel

class RegisterAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']
    

# Register your models here.
# we are registering the models that have been created
admin.site.register(Category, CategoryAdmin) # the classes created, can only show when we connect them to this registered section, they can be added by: (, CategoryAdmin)
admin.site.register(Product, ProductAdmin) # the classes created, can only show when we connect them to this registered section, they can be added by: (, ProductAdmin)
admin.site.register(Contact, ContactAdmin) # the classes created, can only show when we connect them to this registered section, they can be added by: (, ContactAdmin)
admin.site.register(Register, RegisterAdmin)
admin.site.register(Cart)