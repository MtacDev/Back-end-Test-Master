from django.db import models

# Create your models here.

class User(models.Model):
    id_user = models.BigAutoField(primary_key= True)
    name = models.CharField( max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=300)
    nationality = models.CharField( max_length=100)
    access = models.CharField( max_length=100)

class Menu(models.Model):
    id_menu = models.CharField(max_length=150, primary_key=True)
    fecha_menu = models.DateField(unique=True)
    desc_menu = models.CharField(max_length=500)

class Menu_Selected(models.Model):
    id_menu_select = models.BigAutoField(primary_key= True)
    option_selected = models.IntegerField()
    customization = models.CharField(max_length=250)
    fecha_menu_selec = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)