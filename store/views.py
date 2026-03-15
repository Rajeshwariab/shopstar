from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Wishlist
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404



def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, id):

    product = Product.objects.get(id=id)

    cart_item, created = Cart.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/')


def cart(request):
    cart_items = Cart.objects.all()

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('/cart/')

def increase_quantity(request, id):
    item = Cart.objects.get(id=id)
    item.quantity += 1
    item.save()
    return redirect('/cart/')
def decrease_quantity(request, id):
    item = Cart.objects.get(id=id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('/cart/')


def register(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('/')

    return render(request, 'register.html')

def user_login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/')


from .models import Cart, Order

def checkout(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    cart_items = Cart.objects.all()

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity
        )

    cart_items.delete()

    return render(request, 'order_success.html')

def my_orders(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders.html', {'orders': orders})







from .models import Wishlist


@login_required(login_url='/login/')


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist_page')  # Change to your wishlist page URL name
@login_required(login_url='/login/')
def wishlist_page(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required(login_url='/login/')
def wishlist_view(request):
    # Get all wishlist items for the logged-in user
    items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': items
    }
    return render(request, 'store/wishlist.html', context)
@login_required(login_url='/login/')
def remove_from_wishlist(request, wishlist_id):
    item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    item.delete()
    return redirect('wishlist_page')

from django.contrib.auth.decorators import login_required

@login_required
def place_order(request):
    cart_items = Cart.objects.all()

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()

    return redirect('/orders/')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders.html', {
        'orders': orders
    })