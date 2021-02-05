from basketapp.models import Basket


def basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.select_related()
        # basket = Basket.get_items(request.user)
    return {
        'basket': basket,
    }
