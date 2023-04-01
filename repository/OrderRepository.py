from core.database.Database import Database
from model.Order import Order


class OrderRepository:

    def create(self, order: Order, storage: list):
        """
        Store new order in database
        :param order:
        :param storage:
        :return:
        """
        query1 = """INSERT INTO orders VALUES(null,%s,%s,NOW())"""
        query2 = """INSERT INTO order_dishes VALUES(null,%s,%s,%s)"""
        query3 = """UPDATE ingredients SET count=%s WHERE id=%s"""

        dishes = []
        # Init connection
        with Database() as con:
            con.autocommit = False
            cursor = con.cursor()
            # Create an order in database
            cursor.execute(query1, (order.name, order.sum,))
            idx = cursor.lastrowid
            # Transform order dishes to array with tuples
            for dish in order.dishes:
                dishes.append((idx, dish.idx, dish.count))
            # Add into database dishes which was ordered
            cursor.executemany(query2, dishes)
            # Decrease the count of ingredients was used
            cursor.executemany(query3, storage)

            con.commit()

        return idx
