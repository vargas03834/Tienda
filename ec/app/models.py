from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES = (
    ('AMA', 'Amazonas'),
    ('ANT', 'Antioquia'),
    ('ARA', 'Arauca'),
    ('ATL', 'Atlántico'),
    ('BOL', 'Bolívar'),
    ('BOY', 'Boyacá'),
    ('CAL', 'Caldas'),
    ('CAQ', 'Caquetá'),
    ('CAS', 'Casanare'),
    ('CAU', 'Cauca'),
    ('CES', 'Cesar'),
    ('CHO', 'Chocó'),
    ('COR', 'Córdoba'),
    ('CUN', 'Cundinamarca'),
    ('DC', 'Distrito Capital de Bogotá'),
    ('GUA', 'Guainía'),
    ('GUV', 'Guaviare'),
    ('HUI', 'Huila'),
    ('GUV', 'La Guajira'),
    ('MAG', 'Magdalena'),
    ('MET', 'Meta'),
    ('NAR', 'Nariño'),
    ('NSA', 'Norte de Santander'),
    ('PUT', 'Putumayo'),
    ('QUI', 'Quindío'),
    ('RIS', 'Risaralda'),
    ('SAP', 'San Andrés y Providencia'),
    ('SAN', 'Santander'),
    ('SUC', 'Sucre'),
    ('TOL', 'Tolima'),
    ('VAC', 'Valle del Cauca'),
    ('VAU', 'Vaupés'),
    ('VID', 'Vichada')
)


CATEGORY_CHOICES=(
    ('ML','SAMSUNG'),
    ('CR','XIAOMI'),
    ('LS','APPLE'),
    ('MS','MOTOROLA'),
    ('PN','TECNO'),
    ('GH','REALME'),
    ('CZ','VIVO'),
    ('IC','HONOR'),  
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField(default=0)
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
  
STATUS_CHOICES = (
        ('Accepted','Accepted'),
        ('Packed','Packed'),
        ('On The Way','On The Way'),
        ('Delivered','Delivered'),
        ('Cancel','Cancel'),
        ('Pending','Pending'),
)
    
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    payu_order_id = models.CharField(max_length=100,blank=True,null=True)
    payu_payment_status =  models.CharField(max_length=100,blank=True,null=True)
    payu_payment_id =  models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
