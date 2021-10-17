from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'Account was created for {}'.format(user))
            return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html',context)


@unauthenticated_user
def loginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user =authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username Or Password is inCorrect")
    context={}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total_orders=orders.count()
    delivered_orders=orders.filter(status='Delivered').count()
    pending_orders=orders.filter(status='Pending').count()
    return render(request,'accounts/dashboard.html',{'customers':customers,'orders':orders,
                                                     'total_orders':total_orders,
                                                     'pending_orders':pending_orders,
                                                     'delivered_orders':delivered_orders})
@login_required(login_url='login')
def products(request):
    products=Products.objects.all()
    print(products)
    return render(request,'accounts/products.html',{'products':products})


@login_required(login_url='login')
def customers(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    total_orders=orders.count()
    filters=OrderFilter(request.GET,queryset=orders)
    orders=filters.qs
    context={'customer':customer,
             'orders':orders,
             'total_orders':total_orders,
             'filters':filters}
    return render(request,'accounts/customer.html',context)


@login_required(login_url='login')
def create_order(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,form=OrderForm,fields=('product','status'))
    customer = Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    #form=OrderForm(initial={'customer':customer})
    if request.method=='POST':
        data=OrderFormSet(request.POST,instance=customer)
        if data.is_valid():
            data.save()
            return redirect('/customers/{}'.format(pk))
    context={'form':formset}
    return render(request,'accounts/create_order.html',context)


@login_required(login_url='login')
def update_order(request,pk):
    object=Order.objects.get(id=pk)
    form=OrderForm(instance=object)
    if request.method=="POST":
        dataUpdated=OrderForm(request.POST,instance=object)
        if dataUpdated.is_valid():
            dataUpdated.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/update_order.html',context)



@login_required(login_url='login')
def delete_order(request,pk):
    object=Order.objects.get(id=pk)
    if request.method=="POST":
        object.delete()
        return redirect('/')
    return render(request,'accounts/delete_order.html',{'item':object})


@login_required(login_url='login')
def create_customer(request):
    form=CustomerForm()
    if request.method=="POST":
        print("yes")
        newobj=CustomerForm(request.POST)
        if newobj.is_valid():
            newobj.save()
            return redirect('/')
    return render(request,'accounts/create_customer.html',{'form':form})


@login_required(login_url='login')
def update_customer(request,pk,pk2):
    customer=Customer.objects.get(id=pk2)
    form=CustomerForm(instance=customer)
    if request.method=="POST":
        updatedObject=CustomerForm(request.POST,instance=customer)
        if updatedObject.is_valid():
            updatedObject.save()
            return redirect("/customers/{}".format(pk))
    return render(request,'accounts/update_customer.html',{'form':form})

@login_required(login_url='login')
def delete_customer(request,pk,pk2):
    customer=Customer.objects.get(id=pk2)
    if request.method=="POST":
        customer.delete()
        return redirect("/")
    return render(request,'accounts/delete_customer.html',{'customer':customer})


