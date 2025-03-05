from collection.models import LegoSet


def update_all_prices():
    """Met à jour les prix de tous les sets LEGO de la base de données."""
    for lego_set in LegoSet.objects.all():
        lego_set.update_price()
        print(f"Prix mis à jour pour {lego_set.name}: {lego_set.price} €")


if __name__ == "__main__":
    update_all_prices()
