from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
"""
# no model Contact
id: primary key (automatico), fisrt_name: str, last_name: str, phone: str, email: email, crete_date: date, description: text (> 255 caracteres),
category: foreign key, show: boolean,, picture: imagem
owner: foreign key
"""
# blank -> torna o campo opcional


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{str(self.name)}"


class Contact(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=85)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    created_date = models.DateTimeField(default=now)
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to="pictures/%Y/%m/%d")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f"{str(self.first_name)} {str(self.last_name)}"
