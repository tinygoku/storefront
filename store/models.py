from django.db import models


class Promotions(models.Model):
    # Promotions we could have for products
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    # or Categories, under what label will Products go
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    # Item being sold
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    last_updated = models.DateField(auto_now=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    inventory = models.IntegerField
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    promotions = models.ManyToManyField(Promotions)


class Customer(models.Model):
    # Dummy person.
    MEMBERSHIP_COMMON = 'C'
    MEMBERSHIP_UNCOMMON = 'U'
    MEMBERSHIP_RARE = 'R'
    MEMBERSHIP_MYTHIC_RARE = 'M'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_COMMON, 'COMMON'),
        (MEMBERSHIP_UNCOMMON, 'UNCOMMON'),
        (MEMBERSHIP_RARE, 'RARE'),
        (MEMBERSHIP_MYTHIC_RARE, 'MYTHIC RARE'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=9)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_COMMON)


class Order(models.Model):
    # Receipt basically
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_OPTIONS = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_OPTIONS)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    # Detail of the receipt
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)


class Address(models.Model):
    # Not sure why it would go on a different class, and not under customer
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    # Created to hold items
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # Objects in cart, before being purchased.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
