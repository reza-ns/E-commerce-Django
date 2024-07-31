from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from . import models
from .forms import CommentForm


class HomeView(View):
    def get(self, request):
        latest_products = models.Product.objects.all().order_by('-created_at')[:4]
        discounted_products = models.Product.objects.filter(discount__isnull=False).order_by('-created_at')[:4]
        context = {
            'latest_products': latest_products,
            'discounted_products': discounted_products,
        }
        return render(request, 'shop/home.html', context)


class ProductPageView(View):
    def get(self, request, product_slug):
        comment_form = CommentForm()
        # add_to_cart_form = AddToCartForm()
        product = get_object_or_404(models.Product, slug=product_slug, is_active=True)
        products_similar_tags = models.Product.objects.filter(tag__in=product.tag.all()).exclude(id=product.id)
        products_similar_category = models.Product.objects.filter(category=product.category).exclude(id=product.id)
        related_products = products_similar_category.intersection(products_similar_tags)[:4]
        attributes_values = models.ProductAttributeValue.objects.filter(product=product)
        context = {
            'product': product,
            'related_products': related_products,
            'attributes_values': attributes_values,
            'comment_form': comment_form,
            # 'add_to_cart_form': add_to_cart_form
        }
        return render(request, 'shop/product.html', context)

    def post(self, request, product_slug):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = get_object_or_404(models.Product, slug=product_slug)
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
        return HttpResponseRedirect(self.request.path_info)


class CategoryPageView(View):
    def get(self, request, category_slug, page=1):
        category = get_object_or_404(models.Category, slug=category_slug)
        products = models.Product.objects.filter(category=category, is_active=True).order_by('-created_at')
        paginator = Paginator(products, per_page=8)
        page_object = paginator.get_page(page)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=1, on_ends=2)
        context = {
            'products': products,
            'category': category,
            'page_obj': page_object,
        }
        return render(request, 'shop/category.html', context=context)


class TagPageView(View):
    template_name = 'shop/tag.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(models.Tag, slug=tag_slug)
        products = tag.products.all().order_by('-created_at')
        return products
