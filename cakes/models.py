from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save

def upload_location(instance,filename):
	return "%s/%s" %(instance, filename)

class Cake(models.Model):
	name = models.CharField(max_length=30)
	slug = models.SlugField(blank=True,null=True)
	description = models.TextField(max_length=400,null=True)
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
	cake_type = models.CharField(max_length=25,choices=CHOICES) 
	price = models.IntegerField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	image = models.ImageField(upload_to=upload_location)


	def get_absolute_url(self):
		return reverse('cakes:individual_cake', kwargs={'pk': self.pk,})

	def __str__(self):
		return "%s" % self.name

	def __unicode__(self):
		return "%s" % self.name


class CustomCake(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
	name = models.CharField(max_length=100)
	contact = models.EmailField()
	phone = models.IntegerField()
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
	phone_number = models.IntegerField()


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








