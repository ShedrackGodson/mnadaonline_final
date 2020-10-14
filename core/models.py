from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = [
            "-id"
        ]
    


class Product(models.Model):
    """ Product """
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField(max_length=2500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    status = models.CharField(
        max_length=1,
        choices = (
            ("a", "Available"),
            ("u", "Unavailable"),
        ),
        default = "a"
    )
    sold = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    valid_until = models.DateTimeField()

    def get_time_left(self):
        t_diff = relativedelta(self.valid_until.replace(tzinfo=None), timezone.now().replace(tzinfo=None))
        return "{h}H {m}M".format(
            h=t_diff.hours,
            m=t_diff.minutes,
            # s=t_diff.seconds
        )

    def display_status(self):
        for _ in Product.objects.all():
            if _ == self:
                if _.valid_until > timezone.now():
                    _.status = "a"
                    _.save()
                else:
                    _.status = "u"
                    _.save()

        return self.status
    
    def bid_winner(self):
        now = timezone.now()
        customer_placed_bids = []
        if self.valid_until < now:
            for x in BuyProduct.objects.all():
                if x.product.id == self.id:
                    customer_placed_bids.append(x.customer_price)
        
        maximum_placed_bid = max(customer_placed_bids)
        winner = BuyProduct.objects.filter(
            customer_price = maximum_placed_bid,
            product = self
        ).first()
        winnerObj = winner.customer
        winnerObj.stars += 1
        winnerObj.save()
        
        return winnerObj
    
    if __name__ == "__product__":
        display_status()
    
    def get_total_bids(self) -> int():
        """ This returns the total number of customers placed bids """
        bids_counter = int()
        for p in Product.objects.all():
            for b in p.buyproduct_set.all():
                if b.product == self:
                    bids_counter += 1
        return bids_counter

    def __str__(self):
        return "{}-{}".format(self.name, self.status)
    
    class Meta:
        ordering = [
            "-id"
        ]


class BuyProduct(models.Model):
    customer = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_price = models.IntegerField()

    def top_priced_customer(self):
        return BuyProduct.objects.all().order_by("-customer_price")
    
    def __str__(self):
        return "{}-{}".format(self.customer, self.product)
    
    def percentage_calc(self) -> int():
        return round((self.customer_price/self.product.price) * 100, 2)
    
    def price_bar_color(self):
        title = str()
        if self.customer_price > self.product.price:
            return "success"
        elif self.customer_price < self.product.price:
            title = "BID PRICE PLACED IS {} LESS THAN PRODUCT PRICE.".format(
                self.percentage_calc()
            )
            return "danger"
        else:
            return "secondary"
        
    def get_title(self):
        title = str()
        if self.customer_price > self.product.price:
            title = "BID PRICE PLACED IS {}% OF THE PRODUCT PRICE.".format(
                self.percentage_calc()
            )
        elif self.customer_price < self.product.price:
            title = "BID PRICE PLACED IS {}% OF THE PRODUCT PRICE.".format(
                self.percentage_calc()
            )
        else:
            title = "BID PRICE PLACED IS 100% OF THE PRODUCT PRICE."
        return title
    

    class Meta:
        ordering = [
            "-customer_price"
        ]


class UserProfile(AbstractUser):
    """ Profile Of The User """
    photo = models.ImageField(
        verbose_name="Profile Picture",
        upload_to="users/images/",
        null=True,
        blank=True
    )
    phone = models.CharField(
        max_length=13,
        null=True,
        blank=True
    )
    address = models.TextField(
        max_length=100,
        null=True,
        blank=True
    )
    stars = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.username
    
    
class Subscriber(models.Model):
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.email

    class Meta:
        ordering = [
            "-id"
        ]  
        verbose_name_plural = "Subscribers"
      