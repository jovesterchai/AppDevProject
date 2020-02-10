class UpdateStaffboard:

    def __init__(CompanyDeveloper, Company):
        self.__feedbackID = Feedback.countID
        self.__name = name
        self.__number = number
        self.__feedbackZ = feedbackZ

    def get_feedbackID(self):
        return self.__feedbackID

    def get_name(self):
        return self.__name

    def get_number(self):
        return self.__number

    def get_feedbackZ(self):
        return self.__feedbackZ

    def set_feedbackID(self, feedbackID):
        self.__feedbackID = feedbackID

    def set_number(self, number):
        self.__number = number

    def set_feedbackZ(self, feedbackZ):
        self.__feedbackZ = feedbackZ
