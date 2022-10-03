import requests
import json
import uuid

from django.shortcuts import render, redirect #this makes it possible to redirect after sending your message
from django.http import HttpResponse
from .models import * # import inour models from models.py
from django.contrib import messages #this makes us able to use messages function/method
from . forms import * #we are importing our forms from forms.py
# from .forms import ContactForm, CheckoutForm, RegisterForm, UpdateUserForm #we are importing our the forms from forms.py
from django.contrib.auth import authenticate, login, logout #this library is what makes the authenticate part activate
from django.contrib.auth.decorators import login_required

# Create your views here.
###### HOME ######
def index(request):
    featured = Product.objects.filter(featured = True)
    latest = Product.objects.filter(latest = True)

    context = {
        'featured': featured,
        'latest': latest,
    }
    return render(request, 'index.html', context)

###### STORE ######
def store(request):
    gown = Product.objects.filter(category_id = 1)
    bag = Product.objects.filter(category_id = 2)
    skirt = Product.objects.filter(category_id = 3)
    shoe = Product.objects.filter(category_id = 4)

    context = {
        'gown': gown,
        'bag': bag,
        'skirt': skirt,
        'shoe': shoe,
    }
    return render(request, 'store.html', context)


###### DETAIL OF PRODUCTS ######
def detail(request, id, slug):
    detail = Product.objects.get(pk = id)

    context = {
        'detail': detail
    }
    return render(request, 'detail.html', context)


###### CONTACT ######
def contact(request):
    contact = ContactForm() #instantiate the form for a Get request 
    if request.method == 'POST': #method POST is used to collect data from users so as to persist the data to the Database
        contact = ContactForm(request.POST) #instantiate the form for a POST request
        if contact.is_valid(): # form validations holds at this point
            contact.save() #form is saved if it passes the validation check
            messages.success(request, 'Your messages has been sent successfully ! We will contact you shortly, Thank you.') #alert pop up 
            return redirect('contact')

    context = {
        'contact': contact,
    }
    return render(request, 'contact.html', context)

def about(request):
    return render(request, 'about.html')


###### ADD TO CART ######
# @login_required(login_url='signin')
def add_to_cart(request):
    if request.method == 'POST':
        quantity = int(request.POST['qty'])
        store_id = request.POST['storeid']
        size = request.POST.get('pick_size', None)
        main = Product.objects.get(pk=store_id)
        order = Cart.objects.filter(user__username=request.user.username, paid=False)
        if order:
            basket = Cart.objects.filter(user__username=request.user.username, paid=False, product_id=main.id, qty=quantity, size=size)
            if basket:
                basket.qty = quantity
                basket.size = size
                basket.amount = main.price * basket.qty
                # basket.save()
                messages.success(request, 'One item added to cart')
                return redirect('index')
            else:
                newitem = Cart()
                newitem.user = request.user
                newitem.product = main
                newitem.qty = quantity
                newitem.size = size
                newitem.price = main.price
                newitem.amount = main.price * quantity
                newitem.paid = False
                newitem.save()
                messages.success(request, 'One item added to cart')
                return redirect('index')
        else:
            neworder = Cart()
            neworder.user = request.user
            neworder.product = main
            neworder.qty = quantity
            neworder.size = size
            neworder.price = main.price
            neworder.amount = main.price * quantity
            neworder.paid = False
            neworder.save()
            messages.success(request, 'One item added to cart')
        return redirect('index')



###### CART ######
@login_required(login_url='signin')
def cart(request):
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)

    for item in cart:
        item.amount = item.price * item.qty
        item.save()

    subtotal = 0
    vat = 0
    total = 0

    for item in cart:
        subtotal += item.price * item.qty
    
    vat = 0.075 * subtotal
    total = subtotal + vat

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'vat': vat,
        'total': total,
    }

    return render(request, 'cart.html', context)


###### DELETE ######
@login_required(login_url='signin')
def delete(request):
    if request.method == 'POST':
        del_item = request.POST['del_id']
        Cart.objects.filter(pk=del_item).delete()
        messages.success(request, 'One item deleted')
        return redirect('cart') 



###### QUANTITY UPDATE ######
@login_required(login_url='signin')
def update(request):
    if request.method == 'POST':
        qty_item = request.POST['quan_id']
        new_qty = int(request.POST['quanty'])
        newqty = Cart.objects.get(pk=qty_item)
        newqty.qty = new_qty
        newqty.amount = newqty.price * newqty.qty
        newqty.save()
        messages.success(request, 'Quantity updated')
        return redirect('cart') 


###### CHECKOUT ######
# @login_required(login_url='signin')
def checkout(request):
    checkout = CheckoutForm()
    # if request.method == 'POST': #method POST is used to collect data from users so as to persist the data to the Database
    #     checkout = Form(request.POST) #instantiate the form for a POST request
    #     if contact.is_valid(): # form validations holds at this point
    #         contact.save() #form is saved if it passes the validation check
    #         messages.success(request, 'Your messages has been sent successfully ! We will contact you shortly, Thank you.') #alert pop up 
    #         return redirect('contact')
    profile = Register.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for item in cart:
        subtotal += item.price * item.qty

    vat = 0.075 * subtotal
    total = subtotal + vat

    context = {
        'checkout': checkout,
        'cart': cart,
        'subtotal': subtotal,
        'vat': vat,
        'total': total,
    }
    return render(request, 'checkout.html', context)


###### SIGN OUT ######
def signout(request):
    logout(request)
    messages.success(request, 'You have successfully signed out!')
    return redirect('index')


###### SIGN IN ######
def signin(request):
    if request.method == 'POST':
        username = request.POST[ 'username' ]
        password = request.POST[ 'password' ]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome {user.username.upper()}!')
            return redirect('index')
        else:
            messages.info(request, 'Username/Password is incorrect, Please try again.')
            return redirect('signin')
    
    return render(request, 'signin.html')


###### REGISTER ######
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            newuser = Register(user = user)
            newuser.first_name = user.first_name
            newuser.last_name = user.last_name
            newuser.username = user.username
            newuser.email = user.email
            newuser.save()
            login(request, user)
            messages.success(request, f'Congratulations {user.username.upper()}, Your Registration is Successful')
            return redirect('signin')
        else:
            messages.error(request, f'The username or E-mail or Password you have provided is invalid')
            return redirect('register')

    return render(request, 'register.html')



###### PROFILE ######
@login_required
def profile(request):
    profile = Register.objects.get(user__username = request.user.username)

    context = {
        'profile':profile,
    }
    return render(request, 'profile.html', context)


# ###### PROFILE UPDATE ######
def profile_update(request):
    # profile = Register.objects.filter(user__username = request.user.username)
    profile = Register.objects.get(user__username = request.user.username)
    update = UpdateUserForm(instance = request.user.register)
    if request.method == 'POST':
        update = UpdateUserForm(request.POST, instance = request.user.register)
        if update.is_valid:
            update.save()
            messages.success(request, 'Profile update successful!')
            return redirect('profile')
        else:
            messages.error(request, 'invalid data')
            return redirect('profile_update')


    context = {
        'profile':profile,
        'update':update,
    }
        
    return render(request, 'profile_update.html', context)



###### FORGOT PASSWORD ######
def forgot_password(request):
    return render(request, 'forgot_password.html')


###### PAYMENT ######
@login_required(login_url='signin')
def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_6d0333c2928a65b4aa4f3d24596876a2252e3565'#secret key from paystack
        curl = 'https://api.paystack.co/transaction/initialize' #paystack call url
        cburl = 'http://44.204.172.38/callback/'#sleek_store callback url to send payment success message
        ref = str(uuid.uuid4()) # reference number required by paystack as an additional order number
        profile = Register.objects.get(user__username = request.user.username)
        pay_code = profile.id # main pay order number
        total = float(request.POST['total']) * 100 #total amount to be charged from the client's bank
        user = User.objects.get(username = request.user.username) # query the User model for the client's details
        email = user.email # store client's email detail to send to paystack
        first_name = request.POST['first_name'] # collect from the template incase there is change
        last_name = request.POST['last_name'] # collect from the template incase there is change
        phone = request.POST['phone'] # collect from the template incase there is change
        
        # collect data to send to paystack via call
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': ref, 'amount': int(total), 'email': user.email, 'callback_url': cburl, 'order_number':  pay_code, 'currency': 'NGN'}
        
        # make a call to paystack
        try:
            r = requests.post(curl, headers=headers, json=data) #pip install requests
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback = json.loads(r.text)
            print('READING DATA', transback)
            rdurl = transback['data']['authorization_url']
            account = Payment()
            account.user = user
            account.first_name = user.first_name
            account.last_name = user.last_name
            account.amount = total/100
            account.paid = True
            account.phone = phone
            account.pay_code = ref
            account.save()

            return redirect(rdurl)
    
    return redirect('checkout')


def callback(request):
    return render(request, 'callback.html')

###### PASSWORD RESET ######
def password_reset(request):
    return render(request, 'password_reset.html')


###### 404 PAGE ######
def error_page(request):
    return render(request, '404.html')

