class Entity:
    def __init__(self, entity_name):
        self.entity_name = entity_name
        self.surrounding_words = [] # list of strings
        self.surrounding_words_connotations = [] # list of numbers
        self.hero_score = 0
        self.villian_score = 0
        self.victim_score = 0