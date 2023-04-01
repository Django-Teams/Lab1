from core.database.Database import Database
from model.Dish import Dish
from model.Ingredient import Ingredient


class DishRepository:

    def get_dishes(self) -> list[Dish]:
        """
        Get all dishes from database
        :return:
        """
        query = """SELECT d.*, i.*, di.count FROM dishes d 
                    INNER JOIN dish_ingredients di ON d.id=di.dish_id 
                    INNER JOIN ingredients i ON i.id=di.ingredient_id"""

        dishes = []
        # Init db connection
        with Database() as con:
            cursor = con.cursor()
            # Execute query
            cursor.execute(query)

            data = {}
            for row in cursor.fetchall():
                if row[0] not in data.keys():
                    data[row[0]] = [row]
                else:
                    data[row[0]].append(row)
            # Convert data to array of dishes
            for d in data.values():
                dishes.append(self.__extract_dish(d))

        return dishes

    def create(self, dish: Dish):
        """
        Store a new dish in database
        :param dish:
        :return:
        """
        query1 = """INSERT INTO dishes VALUES(null,%s)"""
        query2 = """INSERT INTO dish_ingredients VALUES(null,%s,%s,%s)"""

        ingredients = []
        # Init connection
        with Database() as con:
            con.autocommit = False
            cursor = con.cursor()
            # Insert a dish into the database
            cursor.execute(query1, (dish.name,))
            idx = cursor.lastrowid
            # Add ingredients which dish consists of
            for ing in dish.ingredients:
                ingredients.append((idx, ing.idx, ing.count))
            cursor.executemany(query2, ingredients)

            con.commit()

        return idx

    def update(self, dish: Dish):
        """
        Update dish
        :param dish:
        :return:
        """
        query1 = """UPDATE dishes SET name=%s WHERE id=%s"""
        query2 = """DELETE FROM dish_ingredients WHERE dish_id=%s"""
        query3 = """INSERT INTO dish_ingredients VALUES(null,%s,%s,%s)"""

        ingredients = []
        with Database() as con:
            # Start transaction
            con.autocommit = False
            cursor = con.cursor()
            # Update name of the dish
            cursor.execute(query1, (dish.name, dish.idx))
            # Delete dish ingredients
            cursor.execute(query2, (dish.idx,))
            # Insert new ingredients including old
            for ing in dish.ingredients:
                ingredients.append((dish.idx, ing.idx, ing.count))
            cursor.executemany(query3, ingredients)

            con.commit()

    def delete(self, dish: Dish):
        """
        Delete the dish
        :param dish:
        :return:
        """
        query1 = """DELETE FROM dishes WHERE id=%s"""

        with Database() as con:
            cursor = con.cursor()
            # Delete dish by id
            cursor.execute(query1, (dish.idx,))
            con.commit()

    def __extract_dish(self, data: list) -> Dish:
        """
        Convert result data to Dish object
        :param data:
        :return:
        """
        ingredients = []
        # Make Ingredient object and add to ingredients
        for i in data:
            ingredient = Ingredient(i[3], i[4], i[5], i[2])
            ingredients.append((ingredient, i[6]))
        # Create dish with ingredients
        dish = Dish(data[0][1], ingredients, data[0][0])

        return dish
