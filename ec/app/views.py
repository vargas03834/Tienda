from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
import payu # type: ignore
import hashlib
import json
import requests
from .models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import hashlib
import time
from ec import settings
from .forms import ProductForm

# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html",locals())

@login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem= len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html",locals())

def chatbot(request):
    if request.method == 'POST':
        # Obtener el mensaje del usuario desde la solicitud POST
        user_message = request.POST.get('message')

        # Analizar el mensaje del usuario para identificar la pregunta
        if 'celular' in user_message and 'recomiendas' in user_message:
            # Generar la respuesta del chatbot
            bot_response = "Te recomiendo el Samsung Galaxy A32. Es un excelente celular con buenas características y un precio asequible en Colombia."
        elif 'celular' in user_message and 'economico' in user_message:
            # Generar respuesta para el celular más económico en Colombia
            bot_response = "Te recomiendo el Motorola Moto E7. Es un celular económico con un buen rendimiento y disponible a un precio accesible en Colombia."
        elif 'celular' in user_message and 'caro' in user_message:
            # Generar respuesta para el celular más caro en Colombia
            bot_response = "El iPhone 13 Pro Max es uno de los celulares más caros disponibles en Colombia. Ofrece características premium y un rendimiento excepcional."
        elif 'celular' in user_message and 'tendencia' in user_message:
            # Generar respuesta para el celular en tendencia en Colombia
            bot_response = "El Xiaomi Redmi Note 10 Pro es un celular muy popular en Colombia en este momento. Ofrece una gran relación calidad-precio y muchas personas lo están eligiendo."
        else:
            # Si la pregunta del usuario no se reconoce, dar una respuesta genérica
            bot_response = "Lo siento, no entendí tu pregunta. ¿Podrías ser más específico?"

        # Devolver la respuesta del chatbot como JSON
        return JsonResponse({'message': bot_response})
    else:
        # Si la solicitud no es POST, renderizar la plantilla chatbot.html con las variables de contexto
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/chatbot.html", {'totalitem': totalitem, 'wishitem': wishitem})


@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.values("title").distinct()
        brand_name = val  
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        context = {
            'product': product,
            'title': title,
            'brand_name': brand_name,
            'totalitem': totalitem,
            'wishitem': wishitem,
        }
        return render(request, "app/category.html", context)
    
@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values("title")
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
                wishitem= len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/category.html",locals())
    
@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem= len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem= len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Contratulations! User Register Succesfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())

@method_decorator(login_required,name='dispatch')  
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem= len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/profile.html', locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality  = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request,'app/profile.html', locals())
    
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem= len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem= len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile update succesfully")
        else:
            messages.warning(request, "Invalid input data")
        return redirect("address")

@login_required  
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    
    # Verificar si el producto ya está en el carrito del usuario
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        # Si el producto ya está en el carrito, aumentar su cantidad
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Si el producto no está en el carrito, agregarlo como un nuevo elemento
        Cart.objects.create(user=user, product=product)
    
    return redirect("/cart")

@login_required    
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 10
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem= len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html',locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem= len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request,"app/wishlist.html",locals())
    

def generate_signature(api_key, merchant_id, reference_code, amount, currency):
    signature_str = f"{api_key}~{merchant_id}~{reference_code}~{amount}~{currency}"
    return hashlib.sha512(signature_str.encode()).hexdigest().upper()

# Función para generar el session_id del dispositivo
def generate_device_session_id():
    return str(int(time.time() * 1000))  # Puede ser algo único por sesión

@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 10  # Añadiendo un costo de envío fijo
        payuamount = int(totalamount)
        
        # Crear los valores para la firma y el session_id
        api_key = settings.PAYU_API_KEY
        merchant_id = settings.PAYU_MERCHANT_ID
        reference_code = f"order_{user.id}_{int(time.time())}"
        currency = "COP"  # Usar la moneda correcta
        signature = generate_signature(api_key, merchant_id, reference_code, payuamount, currency)
        device_session_id = generate_device_session_id()

        # Realizar la solicitud POST a la API de PayU
        data = {
            "language": "es",
            "command": "SUBMIT_TRANSACTION",
            "merchant": {
                "apiKey": api_key,
                "apiLogin": settings.PAYU_API_LOGIN
            },
            "transaction": {
                "order": {
                    "accountId": merchant_id,
                    "referenceCode": reference_code,
                    "description": "Compra de producto",
                    "language": "es",
                    "signature": signature,
                    "notifyUrl": "https://www.yoursite.com/notification",  # URL para notificaciones
                    "additionalValues": {
                        "TX_VALUE": {
                            "value": payuamount,
                            "currency": currency
                        }
                    }
                },
                "payer": {
                    "fullName": user.first_name + " " + user.last_name,  # Nombre del usuario
                    "emailAddress": user.email,
                    "contactPhone": "123456789"
                }
            }
        }

        try:
            response = requests.post(
                "https://sandbox.api.payulatam.com/payments-api/4.0/service.cgi",
                json=data
            )

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    order_id = response_data.get('id', None)
                    order_status = response_data.get('status', None)

                    # Si la orden se ha creado correctamente, guardamos los detalles del pago
                    if order_status == 'created':
                        payment = Payment(
                            user=user,
                            amount=totalamount,
                            payu_order_id=order_id,
                            payu_payment_status=order_status
                        )
                        payment.save()
                    else:
                        order_id = None
                except ValueError:
                    print(f"Error parsing JSON response: {response.text}")
                    order_id = None
            else:
                print(f"Error in response from PAYU: {response.status_code} - {response.text}")
                order_id = None
        except Exception as e:
            print(f"Error creating PAYU order: {e}. Response: {getattr(e.response, 'text', 'No response text')}")
            order_id = None

        # Renderizamos el template con los datos de la orden
        return render(request, 'app/checkout.html', {
            'order_id': order_id,
            'totalitem': totalitem,
            'wishitem': wishitem,
            'add': add,
            'cart_items': cart_items,
            'famount': famount,
            'totalamount': totalamount,
            'signature': signature,  # Pasamos la firma a la plantilla
            'device_session_id': device_session_id,  # Pasamos el deviceSessionId a la plantilla
        })
    
    def post(self, request):
        # Aquí gestionamos el pago, una vez que el cliente presione "Pagar"
        order_id = request.POST.get('order_id')

        if not order_id:
            return redirect('checkout')  # Si no tenemos un order_id, regresamos al checkout

        # Suponiendo que la transacción fue aprobada por el cliente
        # Verificamos el estado de la transacción de PayU
        try:
            # Realizamos una solicitud GET para verificar el estado de la orden
            response = requests.get(
                f"https://api.payulatam.com/payments-api/4.0/service.cgi/{order_id}",
                params={"apiKey": settings.PAYU_API_KEY, "apiLogin": settings.PAYU_API_LOGIN}
            )

            if response.status_code == 200:
                payment_response = response.json()
                if payment_response.get('status') == 'success':
                    # Actualizamos el estado del pago en tu base de datos
                    payment = Payment.objects.get(payu_order_id=order_id)
                    payment.payu_payment_status = 'success'
                    payment.save()
                    return redirect('orders')  # Redirige a una página de éxito
                else:
                    return redirect('app/payment_failed')  # Redirige a una página de fallo en el pago
            else:
                return redirect('app/payment_failed')
        except Exception as e:
            print(f"Error verifying PAYU payment status: {e}")
            return redirect('app/payment_failed')

@login_required
def payment_done(request):
    order_id=request.GET.get(order_id)
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(payu_order_id=order_id)
    payment.paid= True
    payment.payu_payment_id = payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem= len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())

def calculate_cart_amount(cart):
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value
    total_amount = amount + 10  # Asumiendo que 10 es el costo de envío
    return amount, total_amount

def plus_cart(request):
    if request.method == 'POST':
        prod_id = request.POST['prod_id']
        c = Cart.objects.filter(user=request.user, product=prod_id).first()
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount, totalamount = calculate_cart_amount(cart)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(user=request.user, product=prod_id).first()
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount, totalamount = calculate_cart_amount(cart)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(user=request.user, product=prod_id).first()
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount, totalamount = calculate_cart_amount(cart)
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def plus_wishlist(request):
    if request.method == 'GET' :
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist Added Successfully',
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        try:
            wishlist_item = Wishlist.objects.get(user=user, product_id=prod_id)
            wishlist_item.delete()
            data = {'message': 'Wishlist Removed Successfully'}
        except Wishlist.DoesNotExist:
            data = {'message': 'Wishlist item not found'}
        return JsonResponse(data)

    
# views.py
def home(request):
    brands = [
        ('SAMSUNG', 'app/images/product/samsung.png', 'ML'),
        ('XIAOMI', 'app/images/product/xiaomi.png', 'CR'),
        ('APPLE', 'app/images/product/apple.png', 'LS'),
        ('MOTOROLA', 'app/images/product/motorola.png', 'MS'),
        ('TECNO', 'app/images/product/tecno.png', 'PN'),
        ('REALME', 'app/images/product/realme.png', 'GH'),
        ('VIVO', 'app/images/product/vivo.png', 'CZ'),
        ('HONOR', 'app/images/product/honor.png', 'IC'),
    ]
    context = {
        'brands': brands,
    }
    return render(request, 'app/home.html', context)

@login_required
def search(request):
    query = request.GET.get('search')
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())


def crear_producto(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # Usamos request.FILES para manejar imágenes
        if form.is_valid():
            form.save()  # Guarda el nuevo producto
            return redirect('listar_productos')  # Redirige a la lista de productos
    else:
        form = ProductForm()  # Si es GET, inicializa un formulario vacío
    return render(request, 'app/crear_producto.html', {'form': form})


# views.py

def listar_productos(request):
    productos = Product.objects.all()  # Obtener todos los productos
    return render(request, 'app/listar_productos.html', {'productos': productos})

def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Product, pk=producto_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()  # Guarda los cambios
            return redirect('listar_productos')  # Redirige a la lista de productos
    else:
        form = ProductForm(instance=producto)  # Carga el formulario con los datos del producto
    return render(request, 'app/actualizar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Product, pk=producto_id)
    if request.method == "POST":
        producto.delete()  # Elimina el producto de la base de datos
        return redirect('listar_productos')  # Redirige a la lista de productos
    return render(request, 'app/eliminar_producto.html', {'producto': producto})

