from django.db import models
from django.core.urlresolvers import reverse

from django.conf import settings
import re 
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import pre_save



def upload_location(instance,filename):
	return "%s/%s" %(instance, filename)

def phone_validator(value):
	reg = re.compile(r'^\d\d\d\d\d\d\d\d\d\d$')
	number = reg.match(value)
	if number is None:
		raise ValidationError("The number is not valid")
	return value 

class Pillo(models.Model):
	name = models.CharField(max_length=30)
	slug = models.SlugField(blank=True,null=True)
	description = models.TextField(max_length=400,null=True)
	price = models.IntegerField()
	timestamp = models.DateTimeField(auto_now=True)
	image = models.ImageField(upload_to=upload_location)
	view_count = models.IntegerField(default=0)


	def raise_view_count(self):
		self.view_count = self.view_count +1
		return True

	def get_absolute_url(self):
		return reverse("gifts:individual_gift", kwargs={"slug": self.slug})

	def __str__(self):
		return "%s" % self.name

	def __unicode__(self):
		return "%s" % self.name


class OrderPillo(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='giftorderuser')
	gift = models.ForeignKey(Pillo,related_name='pillo')
	delivery_date = models.DateField()
	delivery_time = models.TimeField(null=True)
	quantity = models.IntegerField()
	gift_message = models.TextField(max_length=200)
	phone_number = models.CharField(max_length=15,validators=[phone_validator])
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True,null=True)


	def total_price(self):
		marked_price = float(self.gift.price)
		price = marked_price * self.quantity
		price = int(price)
		
		return price

	def __str__(self):
		return "%s ordered %s." %(self.user,self.gift) 

	def __unicode__(self):
		return "%s ordered %s." %(self.user,self.gift) 

def create_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Pillo.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Pillo)








