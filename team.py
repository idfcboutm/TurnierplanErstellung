class Team:
    def __init__(self, name):
        self.free = True
        self.belonging = None
        self.name = name
        self.games_played = 0

    def increment_games_played(self):
        self.games_played += 1

    def set_belonging(self, belonging):
        self.belonging = belonging

    def set_free(self, free):
        self.free = free

    def set_name(self, name):
        self.name = name
