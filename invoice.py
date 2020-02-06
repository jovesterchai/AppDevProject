class Invoice:
    def __init__(self, itemID, userID):
        self.__itemID = itemID
        self.__userID = userID

    def get_itemID(self):
        return self.__itemID

    def get_userID(self):
        return self.__userID

    def set_itemID(self, itemID):
        self.__itemID = itemID

    def set_userID(self, userID ):
        self.__userID = userID
