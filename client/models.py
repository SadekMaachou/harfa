from django.db import models
from django.contrib.auth.models import User




    
class artiste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preuve = models.FileField(blank=True, null=True)
    profession = models.CharField(max_length=50, null=False, default="")

class Annonce(models.Model):
    titre = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(default="no description")
    likes = models.IntegerField(default=0, null=True, blank=True)
    photo1=models.ImageField(upload_to='images_annonce/',null=True,blank=True)
    photo2=models.ImageField(upload_to='images_annonce/',null=True,blank=True)
    photo3=models.ImageField(upload_to='images_annonce/',null=True,blank=True)
class Comment(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class product(models.Model):
    product_name=models.CharField(blank=False,null=False,max_length=100)
    description = models.TextField(default="no description")
    price=models.IntegerField(blank=False,null=False)
    prodect_owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='products')
    quantity=models.IntegerField()
    published_date=models.DateTimeField(auto_now_add=True)
    photo1=models.ImageField(upload_to='images_products/',null=True,blank=True)
    photo2=models.ImageField(upload_to='images_products/',null=True,blank=True)
    photo3=models.ImageField(upload_to='images_products/',null=True,blank=True)

class panier(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='panier')
    product=models.ForeignKey(product,on_delete=models.CASCADE,related_name='panier')
    added_at=models.DateTimeField(auto_now_add=True)
    quantity=models.IntegerField(default=0)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', default=None)
    content = models.TextField(blank=False, null=False)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)



