class Details:

    def __init__(self, itemID,email, address, city, zip):
        self.__itemID = itemID
        self.__email = email
        self.__address = address
        self.__city = city
        self.__zip = zip



    def get_itemID(self):
        return self.__itemID

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_city(self):
        return self.__city

    def get_zip(self):
        return self.__zip


    def set_itemID(self, itemID):
        self.__itemID = itemID

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_city(self, city):
        self.__city = city

    def set_zip(self, zip):
        self.__zip = zip


