from django.contrib import admin
from . import models


class ProductTypeAdmin(admin.ModelAdmin):
    ...


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAttributeValueInline(admin.TabularInline):
    model = models.ProductAttributeValue
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'quantity', 'category', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductAttributeValueInline]
    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    ...


class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'slug')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(models.ProductType, ProductTypeAdmin)
admin.site.register(models.ProductAttribute, ProductAttributeAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Tag, TagAdmin)