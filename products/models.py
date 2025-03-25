from django.db import models
import os
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    group = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        help_text="Category group for navigation menu"
    )

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


def clean_filename(filename):
    """
    Clean filename to make it URL-friendly:
    - Remove spaces and special characters
    - Convert to lowercase
    - Handle duplicates with underscore and number
    """
    # Get the file extension
    base_name, extension = os.path.splitext(filename)

    # Clean the base name: remove spaces and special characters, convert to lowercase  # noqa
    clean_name = slugify(base_name)

    # Return cleaned filename with original extension
    return f"{clean_name}{extension.lower()}"


class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Override save method to clean image filename before saving"""
        if self.image:
            # Clean the filename
            original_name = self.image.name
            clean_name = clean_filename(original_name)

            # Only rename if the filename has changed
            if original_name != clean_name:
                self.image.name = clean_name

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
