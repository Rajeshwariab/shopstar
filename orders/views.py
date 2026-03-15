from django.shortcuts import render, redirect
from .models import ShippingAddress

def checkout(request):

    if request.method == "POST":

        ShippingAddress.objects.create(
            user=request.user,
            full_name=request.POST['name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode']
        )

        return redirect('place_order')

    return render(request, 'checkout.html')