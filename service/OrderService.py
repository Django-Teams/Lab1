from model.Dish import Dish
from model.IngredientStorage import IngredientStorage
from model.Order import Order
from repository.DishRepository import DishRepository
from repository.OrderRepository import OrderRepository


class OrderService:
    MARKUP = 105

    def __init__(self):
        # Init ingredients storage
        self.ist = IngredientStorage()

    def order(self, dishes: list[Dish]) -> Order:
        """
        Make an order
        :param dishes:
        :return:
        """
        name = self.__get_name(dishes)
        # Check if enough ingredients in the storage
        overflow = self.check_ingredients(dishes)
        if len(overflow) != 0:
            raise ValueError("Недостатньо інградієнтів \"{}\"".format('\" \"'.join([i.name for i in overflow])))
        sum = self.get_dishes_sum(dishes)
        # Make order object
        order = Order(name, sum, dishes)
        # Store order in database
        OrderRepository().create(order, self.ist.to_update())

        return order

    def get_dishes(self):
        """
        Return all dishes with price
        :return:
        """
        dishes = DishRepository().get_dishes()
        for dish in dishes:
            dish.price = self.get_dish_price(dish)

        return dishes

    def __get_name(self, dishes) -> str:
        """
        Return generated name of the order
        :param dishes:
        :return:
        """
        names = [dish.name for dish in dishes]
        return ", ".join(names)

    def check_ingredients(self, dishes: list) -> list[Dish]:
        """
        Calculate ingredient expense and return list with insufficient ingredients
        :param dishes:
        :return:
        """
        storage = {}
        # Generate dict with ingredients and its amount in dishes
        for dish in dishes:
            for ing, count in dish.ingredients:
                if ing.idx in storage:
                    storage[ing.idx] += count * dish.count
                else:
                    storage[ing.idx] = count * dish.count

        overflow = []
        # Checking whether there are enough ingredients to prepare a dish
        for idx, amount in storage.items():
            if self.ist.storage[idx].count < amount:
                overflow.append(self.ist.storage[idx])
            self.ist.storage[idx].count -= amount

        return overflow

    def get_dishes_sum(self, dishes: list) -> float:
        """
        Return amount due of the order
        :param dishes:
        :return:
        """
        amount = 0
        # Calculate pricce of dishes
        for dish in dishes:
            amount += self.get_dish_price(dish) * dish.count
        return amount

    def get_dish_price(self, dish: Dish) -> float:
        """
        Return price of the dish
        :param dish:
        :return:
        """
        price = 0
        # Calculate price of the dish
        # Sum all ingredients price and amount, add markup
        for ing, count in dish.ingredients:
            price += round((ing.price * count / 1000) * (100 + self.MARKUP) / 100)

        return price
