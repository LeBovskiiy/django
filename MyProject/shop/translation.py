from modeltranslation.translator import register, TranslationOptions
from .models import Product, ProductCategory, ProductTags

@register(Product)
class ProductTranslationOption(TranslationOptions):
    fields = ('name', 'description',)
    
    
@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('category',)
    
    
@register(ProductTags)
class ProductTagsTranslationsOption(TranslationOptions):
    fields = ('tag_name',)