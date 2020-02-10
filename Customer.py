class Customer:


    def __init__(self, firstName, lastName, username, password, gender, country, address, number):
        self.__firstName = firstName
        self.__lastName = lastName
        self.__username = username
        self.__password = password
        self.__gender = gender
        self.__country = country
        self.__address = address
        self.__number = number


    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_gender(self):
        return self.__gender

    def get_country(self):
        return self.__country

    def get_address(self):
        return self.__address

    def get_number(self):
        return self.__number

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_gender(self, gender):
        self.__gender = gender

    def set_country(self, country):
        self.__country = country

    def set_address(self, address):
        self.__address = address

    def set_number(self, number):
        self.__number = number
