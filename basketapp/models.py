from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super(BasketQuerySet, self).delete(*args. **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return Basket.objects.filter(user=self.user).select_related()

    def total_quantity(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, items)))

    def total_cost(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, items)))

    @staticmethod
    def get_items(user):
        items = Basket.objects.filter(user=user)
        return items

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @staticmethod
    def get_product(product, user):
        return Basket.objects.filter(product=product, user=user)

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_items(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save()
    #
    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()


