from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail
from django.conf import settings
import razorpay
from .models import Order  
from core.models import UserProfile, Post  

razorpay_client = razorpay.Client(auth=("api_key", "api_secret"))

# Create your views here.
def order_view(request):
    user = request.user.username
    orders = Orders.objects.filter(buyer=user)
    return render(request, 'Orders/orders.html', {'orders': orders})

def detail(request, author, url):
    post = get_object_or_404(Post, freelancer__user_id__username=author, link=url)
    orders = Order.objects.filter(service=post).count()
    post_amount = post.amount
    total_amount = orders * post_amount / 100
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=int(post.amount * 100),  # Convert to paise
        currency='INR',
        payment_capture='0'
    ))
    
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/' + url

    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = post.amount
    context['amount'] = float(post.amount)//100
    context['currency'] = 'INR'
    context['callback_url'] = callback_url
    context['title'] = post.name
    context['intro'] = post.description
    context['body'] = post.description
    context['created_at'] = post.timestamp
    context['post'] = post

    return render(request, 'Orders/detail.html', context=context)

def post_detail(request, url):
    post = get_object_or_404(Post, link=url)
    orders = Order.objects.filter(service=post).count()
    post_amount = post.amount
    total_amount = orders * post_amount / 100
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=int(post.amount * 100),  # Convert to paise
        currency='INR',
        payment_capture='0'
    ))
    
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/' + url

    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = post.amount
    context['amount'] = float(post.amount)//100
    context['currency'] = 'INR'
    context['callback_url'] = callback_url
    context['title'] = post.name
    context['intro'] = post.description
    context['body'] = post.description
    context['created_at'] = post.timestamp
    context['post'] = post

    return render(request, 'crowdfunding/detail.html', context=context)

@csrf_exempt
def paymenthandler(request, author, url):
    post = get_object_or_404(Post, freelancer__user_id__username=author, link=url)
    referer = request.META.get('HTTP_REFERER')
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = post.amount 
                try:
                    # capture the payment
                    razorpay_client.payment.capture(payment_id, amount)

                    # create a Transaction instance and save it to the database
                    order = Order(
                        amount=amount/100,
                        buyer=request.user.userprofile,
                        service=post,
                    )
                    order.save()
                    donated_amount = int(post.amount)
                    subject = f'Successful donation to {post.name}'
                    message = (f'Hello {request.user.username}. Thank you for making a contribution of Rs. '
                               f'{donated_amount} for {post.name}. Your payment id is: {payment_id}')
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [request.user.userprofile.email]  # List of recipient email addresses

                    send_mail(subject, message, from_email, recipient_list)
 
                    # render success page on successful caputre of payment
                    return redirect(referer)
                except:
                    # if there is an error while capturing payment.
                    return redirect(referer)
            else:
                # if signature verification fails.
                return redirect(referer)
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()