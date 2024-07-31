from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class ProductType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    name = models.CharField(max_length=32)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='attributes')

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'Category', on_delete=models.PROTECT, blank=True, null=True, related_name='sub_categories'
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='products')
    price = models.IntegerField(default=0)
    discount = models.SmallIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='products/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, related_name='products')
    tag = models.ManyToManyField('Tag', blank=True, related_name='products')

    def __str__(self):
        return self.name

    def discounted_price(self):
        return self.price - int((self.price * self.discount) / 100)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='images')


class ProductAttributeValue(models.Model):
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.PROTECT, related_name='values')

    def __str__(self):
        return f"{self.product}({self.attribute}): {self.value}"


class Comment(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='comments')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, related_name='tags')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
