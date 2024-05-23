from django.core.management.base import BaseCommand
from django.db.models import Count
from app.models import Cart
#for removing duplicate cart items
class Command(BaseCommand):
    help = 'Remove duplicate cart items for each user-product combination'

    def handle(self, *args, **kwargs):
        duplicates = (
            Cart.objects.values('user', 'product')
            .order_by()
            .annotate(count=Count('id', distinct=True))
            .filter(count__gt=1)
        )

        for duplicate in duplicates:
            user = duplicate['user']
            product = duplicate['product']
            carts = Cart.objects.filter(user_id=user, product_id=product)
            quantity_sum = sum(cart.quantity for cart in carts)
            first_cart = carts.first()
            first_cart.quantity = quantity_sum
            first_cart.save()

            # Delete all but the first cart
            carts.exclude(id=first_cart.id).delete()

        self.stdout.write(self.style.SUCCESS('Successfully removed duplicate cart items'))
