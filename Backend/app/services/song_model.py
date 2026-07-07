class Song:
    def __init__(self, id, name, artist, priority, img, settings):
        self.id = id

        self.name = name
        self.artist = artist
        self.priority = priority
        self.img = img

        self.chance = settings[str(priority)]['chance']
        self.cooldown = settings[str(priority)]['cooldown']
        self.up = settings[str(priority)]['up']

        self.idle = 0
        self.played = 0

    def __eq__(self, other):
        return self.id == other.id

    def play(self):
        self.idle = 0
        self.chance = 0
        self.played += 1

    def update(self):
        self.idle += 1
        if self.idle >= self.cooldown:
            self.chance += self.up

    def to_dict(self):
        return {
                'name': self.name,
                'artist': self.artist,
                'priority': self.priority,
                'img': self.img
        }