class Feedback:
    countID = 0

    def __init__(self, name, country, feedbackZ):
        Feedback.countID += 1
        self.__feedbackID = Feedback.countID
        self.__name = name
        self.__country = country
        self.__feedbackZ = feedbackZ

    def get_feedbackID(self):
        return self.__feedbackID

    def get_name(self):
        return self.__name

    def get_country(self):
        return self.__country

    def get_feedbackZ(self):
        return self.__feedbackZ

    def set_feedbackID(self, feedbackID):
        self.__feedbackID = feedbackID

    def set_country(self, country):
        self.__country = country

    def set_feedbackZ(self, feedbackZ):
        self.__feedbackZ = feedbackZ
