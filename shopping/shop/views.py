from django.http import HttpResponse
from . models import Product,Contact,Orders
from django.utils import timezone
import logging
from decimal import Decimal
from  django . conf  import  settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum
from .paytm.Checksum import generate_checksum, verify_checksum


PAYTM_SECRET_KEY = 'hMeivIIuJ2nqJ51f'

# Get an instance of a logger
logger = logging.getLogger(__name__)



# Create your views here.

def index(request):
    products= Product.objects.all()
    print(products)
    n=len(products)
    print(n)
    params={'range':range(1,n), 'product': products}
    
   
    return render(request,'shop/index.html',params)

def home(request):
    return render(request,'shop/home.html')

def cart(request):
    return render(request,'shop/cart.html')

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method =='POST':
        first=request.POST.get('first', '')
        last=request.POST.get('last', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        print(first,last,email,phone,desc)
        contact =Contact(first=first ,last=last, email=email, phone=phone, desc=desc)
        contact.save()
    
    return render(request,'shop/contact.html')

def productview(request,myid):
    product=Product.objects.filter(id=myid)
    print(product)
    dictpro={'product':product[0]}
    return render(request,'shop/productview.html',dictpro)

@csrf_exempt
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        #thank = True
        id = order.order_id
        PAYTM_SECRET_KEY = 'hMeivIIuJ2nqJ51f'
        merchant_key = settings.PAYTM_SECRET_KEY
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'RWwriI30442924973366',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/callback/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, merchant_key)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'shop/canceled.html')

        return render(request, 'shop/callback.html', context=received_data)

@csrf_exempt
def canceled(request):
    return render(request, 'shop/canceled.html')