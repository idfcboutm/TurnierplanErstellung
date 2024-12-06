class Team:
    def __init__(self):
        self.free = True
        self.belonging = None;

    def set_belonging(self, belonging):
        self.belonging = belonging

    def set_free(self, free):
        self.free = free
