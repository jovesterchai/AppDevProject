class Product:
    countID = 0

    def __init__(self, itemID, name, price, color, size, quantity, gender, description):
        self.__class__.countID += 1
        self.__itemCount = self.__class__.countID
        self.__itemID = itemID
        self.__name = name
        self.__price = price
        self.__color = color
        self.__size = size
        self.__quantity = quantity
        self.__gender = gender
        self.__description = description

    def get_itemID(self):
        return self.__itemID

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_color(self):
        return self.__color

    def get_size(self):
        return self.__size

    def get_quantity(self):
        return self.__quantity

    def get_gender(self):
        return self.__gender

    def get_description(self):
        return self.__description

    def set_itemID(self, itemID):
        self.__itemID = itemID

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_color(self, color):
        self.__color = color

    def set_size(self, size):
        self.__size = size

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_gender(self, gender):
        self.__gender = gender

    def set_description(self, description):
        self.__description = description
