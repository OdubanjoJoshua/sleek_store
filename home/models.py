from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50) # this is the value given to every Category been created
    img = models.ImageField(upload_to='img') # the string inserted in 'upload_to', creates a folder where all the images for that class is been stored
    slug = models.SlugField(unique=True) # this is a replica of the name in the url with an hyphen after every word with no space

    # this makes the name, which was set in the class Category display in the admin, when a category is been added
    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # this connect the product to become a sub-directory under the Category
    title = models.CharField(max_length=50) # this is the value given to every Product been created
    slug = models.SlugField(unique=True) # this is a replica of the title in the url with an hyphen after every word with no space
    pics = models.ImageField(upload_to='pics') # the string inserted in 'upload_to', creates a folder where all the images for that class is been stored
    price = models.IntegerField() # the price of the product
    details = models.TextField() # This is the description of the products 
    featured = models.BooleanField(default=True) # this is for the featured products in the homepage
    latest = models.BooleanField(default=True) # this is for the latest products in the homepage
    
    # this makes the name, which was set in the class Product display in the admin, when a Product is been added
    def __str__(self):
        return self.title
    

class Contact(models.Model):
    full_name = models.CharField(max_length=50)
    # phone = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateField(auto_now=True)
    cleared = models.DateField(auto_now=True)
    admin_note = models.TextField()

    def __str__(self):
        return self.full_name

    # class Meta:
    #     db_table = 'contact'
    #     managed = True
    #     verbose_name = 'Contact_Us'
    #     verbose_name_plural = 'Contact_Us'


class Checkout(models.Model):
    full_name = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=250)
    address_2 = models.CharField(max_length=250)
    zip_code = models.IntegerField()
    phone = models.IntegerField()
    use_or_not = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class Register(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.user.username
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    amount = models.IntegerField(blank=True, null=True)
    paid = models.BooleanField(default=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    qty = models.IntegerField(default=1)
    added_time = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    avatar = models.ImageField(default='default.png', upload_to='profile_img')
    bio = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    Last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return f'{self.user.username} Profile'
        return self.user.username
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    amount = models.IntegerField()
    paid = models.BooleanField()
    pay_code = models.CharField(max_length=36)
    payment_date = models.DateTimeField(auto_now_add=True)
    admin_update = models.DateTimeField(auto_now=True)
    admin_note = models.TextField(blank = True, null=True)

    def __str__(self):
        return self.user.username