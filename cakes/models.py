from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
import re


def upload_location(instance,filename):
	return "%s/%s" %(instance, filename)


def phone_validator(value):
	reg = re.compile(r'^\d\d\d\d\d\d\d\d\d\d$')
	number = reg.match(value)
	if number is None:
		raise ValidationError("The number is not valid")
	return value


CHOICES = (('Birthday','Birthday'),
		('Marriage','Marriage'),
		('New year','New year'),
		('Congratulate','Congratulate'),
		('Surprise','Surprise'),
		('Anniversary','Anniversary'),
		('Valentines Day','Valentines Day'),
		('Party','Party'),
		('Special with Cakes','Special with Cakes'),
		('Send Gifts','Send Gifts'),
		('Propose','Propose'),
		('Festivals','Festivals'))

WEIGHTS = (('1','1'),
			('1.5','1.5'),
			('2','2'),
			('2.5','2.5'),
			('3','3'),
			('3.5','3.5'),
			('4','4'),
			('4.5','4.5'),
			('5','5'))

FLAVOUR = (('Vanila','Vanila'),
			('Whiteforest','Whiteforest'),
			('Blackforest','Blackforest'),
			('Choclate','Choclate'),
			('Butterscotch','Butterscotch'),
			('Mix Fruit','Mix Fruit'),
			('Pineapple','Pineapple'),
			('Strawberry','Strawberry'),
			('Ice Cream','Ice Cream'),
			('Mocha','Mocha'),
			('Blueberry','Blueberry'))


class Cake(models.Model):
	name = models.CharField(max_length=30)
	slug = models.SlugField(blank=True,null=True)
	description = models.TextField(max_length=400,null=True)
	cake_type = models.CharField(max_length=25,choices=CHOICES) 
	price = models.IntegerField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	image = models.ImageField(upload_to=upload_location)
	flavour = models.CharField(max_length=15,choices=FLAVOUR,null=True)
	weight = models.CharField(max_length=2,choices=WEIGHTS,null=True)


	def get_absolute_url(self):
		return reverse("cakes:individual_cake", kwargs={"slug": self.slug})

	def __str__(self):
		return "%s" % self.name

	def __unicode__(self):
		return "%s" % self.name


class CustomCake(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
	name = models.CharField(max_length=100)
	contact = models.EmailField()
	phone = models.CharField(max_length=15,validators=[phone_validator])
	details = models.CharField(max_length=500,blank=True)
	image = models.ImageField(upload_to=upload_location,blank=True)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

	def __str__(self):
		return "from %s " %self.name

	def __unicode__(self):
		return "from %s " %self.name


class OrderCake(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='orderuser')
	cake = models.ForeignKey(Cake,related_name='cake')
	delivery_date = models.DateField()
	delivery_time = models.TimeField(null=True)
	quantity = models.IntegerField()
	cake_message = models.TextField(max_length=200)
	phone_number = models.CharField(max_length=15,validators=[phone_validator])
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True,null=True)
	weight = models.CharField(max_length=5,choices=WEIGHTS,null=True,verbose_name='weight(pounds):')
	flavour = models.CharField(max_length=15,choices=FLAVOUR,null=True,verbose_name='Flavours')

	def total_price(self):
		marked_price = float(self.cake.price)
		marked_weight = float(self.cake.weight)
		price = marked_price/(1+0.8*(marked_weight-1))

		price = price + 0.8 * price * (float(self.weight) - 1)

		flavour = self.flavour
		if flavour == "Vanila":
			extra = 0
		elif flavour == "Whiteforest":
			extra = 0
		elif flavour == "Blackforest":
			extra = 0
		elif flavour == "Choclate":
			extra = 200
		elif flavour == "Butterscotch":
			extra = 200
		elif flavour == "Mix Fruit":
			extra = 450
		elif flavour == "Pineapple":
			extra = 350
		elif flavour == "Strawberry":
			extra = 350
		elif flavour == "Ice Cream":
			extra = 300
		elif flavour == "Mocha":
			extra = 450
		elif flavour == "Blueberry":
			extra = 350
		else:
			extra = 0
		price = price + extra
		price = price * self.quantity
		
		return price

	def __str__(self):
		return "%s ordered %s." %(self.user,self.cake)

	def __unicode__(self):
		return "%s ordered %s." %(self.user,self.cake) 



def create_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Cake.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Cake)






