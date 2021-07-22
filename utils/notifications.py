class Notification:

    def __init__(self, data_set):
        self.id = data_set[0]
        self.type = data_set[1]
        self.publisher = data_set[2]
        self.subscriber = data_set[3]
        self.datetime = data_set[4]
        self.status = data_set[5]