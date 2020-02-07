class Customer:


    def __init__(self, firstName, lastName, username, password, gender):
        self.__firstName = firstName
        self.__lastName = lastName
        self.__username = username
        self.__password = password
        self.__gender = gender


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
