from django.shortcuts import render,HttpResponse,redirect
from storeapp.models import Product,Cart,Orders
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.
'''
def function_name(request):
    function body
    return HttpResponse(data)
'''
def home(request): #dashboard
    p=Product.objects.all()#list of objects in variable p
    print(p)
    context={}
    context['user']="Itvedant-thane"
    context['x']=30
    context['y']=40
    context['l']=[10,20,30,40,60]
    context['d']={'id':1,'name':'Machine','price':2500,'qty':5}
    context['data']=[

            {'id':1,'name':'Machine','price':2500,'qty':5},
            {'id':2,'name':'Samsung','price':15000,'qty':2},
            {'id':3,'name':'jeans','price':550,'qty':5},

    ]


    context['products']=p
    return render(request,'home.html',context)#passing context to home.html

def contact(request):
    return HttpResponse("Hello from contact page")

def delete(request,rid):

   p=Product.objects.filter(id=rid) #select * from storeapp_product where id=rid
   p.delete()
   return redirect('/home')

def edit(request,rid):

    if request.method=="GET":
        p=Product.objects.filter(id=rid)#select * from storeapp_product where id=2
        context={} #creating empty dictionary
        context['data']=p # assigning fetch product to key data in context dictionary
        return render(request,'editproduct.html',context) #passing dict context to editproduct.html
    else:
      uname=request.POST['pname']
      uprice=request.POST['price']
      uqty=request.POST['qty']
      #print("Name:",uname)
      #print("Price:",uprice)
      #print("QTY:",uqty)
      p=Product.objects.filter(id=rid)
      p.update(name=uname,price=uprice,qty=uqty)
      return redirect('/home')


   

def greet(request):
    return render(request,'base.html')

def addproduct(request):
    #print(request.method)
    if request.method=="GET":#GET==GET True | POST == GET F
        #print("In if part")
        return render(request,'addproduct.html')
    else:
        #print("In else part")
        product_name=request.POST['pname']#machine
        price=request.POST['price']#2000
        q=request.POST['qty']#2

        #print("Name:",product_name)
        #print("Price:",price)
        #print("Quantity:",q)
        #insert record into table
        p=Product.objects.create(name=product_name,price=price,qty=q)#(name="machine",price=2000,qty=2)
        #print("Product Object:",p)
        p.save()
        #return HttpResponse("Data is inserted in table")
        return redirect('/home')
    


#function views for ecommerce application

def index(request):
    uid=request.user.id
    print("User id:",uid)
    print(request.user.is_authenticated)
    print(request.user.username)
    p=Product.objects.filter(is_active=True)
    #print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def detail(request,id):
    #print("ID:"+id)
    p=Product.objects.filter(id=id)
    #print(p)
    context={}
    context['products']=p
    return render(request,'details.html',context)

def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=1)
    #p=Product.objects.filter(cat=cv)
    #print(p)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)


def pricerange(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=1)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv == '1':
        para='-price'
    else:
        para='price'
       
    p=Product.objects.order_by(para).filter(is_active=1)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def register(request):
    context={}
    if request.method=="GET":
       return render(request,'register.html')
    else:
        #Data fetch
        user=request.POST['uname']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        #validations
        if user=='' or p=='' or cp=='':
            context['errmsg']="Fields cannot be Empty"
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']="Password and Confirm Password didn't Matched"
            return render(request,'register.html',context)
        else:
            #Insert 
            try:
                u=User.objects.create(username=user)
                u.set_password(p)
                u.save()
                context['success']="User Created Successfully"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User already Exists."
                return render(request,'register.html',context)
           

def user_login(request):
    context={}
    if request.method=="GET":
       return render(request,'login.html')
    else:
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print(uname)
        #print(upass)
        u=authenticate(username=uname,password=upass)
        if u is not None:
            login(request,u)
            return redirect('/index')
        else:
           context['errmsg']="Invalid Username and Password!!!"
           return render(request,'login.html',context)



def user_logout(request):
        logout(request)
        return redirect('/index')

# Cart Functionality

def addcart(request,rid):
    context={}
    #print(request.user.id)
    if request.user.id:
        p=Product.objects.filter(id=rid)
        u=User.objects.filter(id=request.user.id)
        #print(p)
        #print(p[0])
        q1=Q(pid=p[0])
        q2=Q(uid=u[0])
        res=Cart.objects.filter(q1 & q2)
        #print("Response:",res)
        if res:
            context['dup']="Product already exists in cart!!!"
            context['products']=p
            return render(request,'details.html',context)
        else:
          
            #print(u)
            #print(u[0])
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['products']=p
            context['success']="Product Added Successfully in Cart!!!"
            return render(request,'details.html',context)

    else:
        return redirect('/login')

   
def viewcart(request):
    context={}
    if request.user.is_authenticated:
       
       c=Cart.objects.filter(uid=request.user.id)
       cp=len(c)
       print("Count:",cp)
       s=0
       for x in c:
           #print(x)
           #print(x.qty)
           #print(x.pid.price)
           s=s+(x.qty*x.pid.price)
        
       print("Summation or Total:",s)
       context['total']=s
       context['cdata']=c
       context['items']=cp
       return render(request,'cart.html',context)

    else:
          return redirect('/login')


def removecart(request,rid):
    c=Cart.objects.filter(id=rid)
    c.delete()
    return redirect('/cart')

def cartqty(request,sig,pid):
    q1=Q(uid=request.user.id)
    q2=Q(pid=pid)
    c=Cart.objects.filter(q1 & q2)
    #print(c) 
    qty=c[0].qty
    #print(qty)
    if sig=='0':
        if qty>1:
           qty=qty-1
           c.update(qty=qty)
    else:
        qty=qty+1
        c.update(qty=qty)
   

    #print("Existing:",qty)
    return redirect('/cart')


def place_order(request):
    if request.user.is_authenticated:
            context={}
            c=Cart.objects.filter(uid=request.user.id)
            oid=random.randrange(1000,9999)
            #print("Order Id:",oid)
            s=0
            for x in c:
                    o=Orders.objects.create(order_id=oid,uid=x.uid,pid=x.pid,qty=x.qty)
                    o.save()
                    x.delete()
            
            o=Orders.objects.filter(uid=request.user.id)
            i=len(o)
            for y in o:
                s=s+(y.qty*y.pid.price)

            context['cdata']=o
            #print("Summation:",s)
            context['total']=s
            #print("Number of items:",i)
            context['items']=i     

            return render(request,'placeorders.html',context)   
    else:
            return redirect('/login')
    

def makepayment(request):
    context={}
    client = razorpay.Client(auth=("rzp_test_U9IgjOccEcYqI8", "EL3LHWHChiYEgXOwqQYav3oZ"))
    #print(client)
    #fetch incomplete orders for logged in user from orders table
    o=Orders.objects.filter(uid=request.user.id)
    oid=str(o[0].order_id)
    s=0
    for y in o:
        s=s+(y.qty*y.pid.price)
    #print("Order Id:",oid)
    #print("Total:",s)
    s=s*100 #Rs to paise 
    data = { "amount":s, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context['payment']=payment


    return render(request,'pay.html',context)

#Appcode: cohd uvtp lgso ayyr
def sendmail(request):
    pid=request.GET['p1']
    oid=request.GET['p2']
    sign=request.GET['p3']
    rec_email=request.user.email
    #print(rec_email)
    #print("Payment ID:",pid)
    #print("Order ID:",oid)
    #print("Signature:",sign)
    msg="Your Order had been Placed Successfully. Your Order Tracking ID:"+oid
    send_mail(
    "Ekart Order Status",
    msg,
    "shirishpatil137@gmail.com",
    [rec_email],
    fail_silently=False,
   )
    return HttpResponse("Email Send")

