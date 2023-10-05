class Song_Attributes:
    track_id = ''
    danceability = 0.0
    loudness = 0.0
    valence = 0.0
    energy = 0.0
    speechiness = 0.0
    


    def __init__(self, id, attribute) -> None:
        self.track_id = id
        self.danceability = attribute['danceability']
        self.loudness = attribute['loudness']
        self.valence = attribute['valence']
        self.energy = attribute['energy']
        self.speechiness = attribute['speechiness']


