import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _

def recipe_image_file_path(instance, filename):
    # Generate file path for new recipe image.
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    # Manager for users.

    def create_user(self, email, password=None, **extra_fields):
        # Create and save a new user.
        if not email:
            raise ValueError(_('Users must have an email address.'))
        user = self.model(email=self.normalize_email(str(email).lower().strip()), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create and save a new superuser.
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # User in the system.
    email = models.EmailField(_('email'),max_length=255, unique=True)
    name = models.CharField(_('name'),max_length=255)
    is_active = models.BooleanField(_('is active'),default=True)
    is_staff = models.BooleanField(_('is staff'),default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Recipe(models.Model):
    # Recipe object.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('title'),max_length=255)
    description = models.TextField(_('description'),blank=True)
    time_minutes = models.IntegerField(_('time in minutes'),)
    price = models.DecimalField(_('price'),max_digits=5, decimal_places=2)
    link = models.CharField(_('link'),max_length=255, blank=True)
    recipe_created_at = models.DateTimeField(_('recipe created at'),auto_now_add=True)
    recipe_updated_at = models.DateTimeField(_('recipe updated at'),auto_now=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(_('image'),null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        # Return the model as a string.
        return self.title

    class Meta:
        # Meta class for the recipe model.
        ordering = ['-id']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

class Tag(models.Model):
    # Tag for filtering recipes.

    name = models.CharField(_('name'),max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag_created_at = models.DateTimeField(_('tag created at'),auto_now_add=True)

    def __str__(self):
        # Return the model as a string.
        return self.name

    class Meta:
        # Meta class for the tag model.
        ordering = ['-id']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

class Ingredient(models.Model):
    # Ingredient for filtering recipes.

    name = models.CharField(_('name'),max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    ingredient_created_at = models.DateTimeField(_('ingredient created at'),auto_now_add=True)

    def __str__(self):
        # Return the model as a string.
        return self.name

    class Meta:
        # Meta class for the tag model.
        ordering = ['-id']
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')