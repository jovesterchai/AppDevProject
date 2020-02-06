class Feedback:
    countID = 0

    def __init__(self, name, country, feedbackz):
        Feedback.countID += 1
        self.__feedbackID = Feedback.countID
        self.__name = name
        self.__country = country
        self.__feedbackz = feedbackz

    def get_feedbackID(self):
        return self.__feedbackID

    def get_name(self):
        return self.__name

    def get_country(self):
        return self.__country

    def get_feedbackz(self):
        return self.__feedbackz

    def set_feedbackID(self, feedbackID):
        self.__feedbackID = feedbackID

    def set_country(self, country):
        self.__country = country

    def set_feedbackz(self, feedbackz):
        self.__feedbackz = feedbackz
