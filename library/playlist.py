import os

class Track:
    """Représente un morceau audio avec ses métadonnées minimales."""
    def __init__(self, path, title=None, artist=None, album=None, duration=None):
        self.path = path
        self.title = title or os.path.basename(path)
        self.artist = artist
        self.album = album
        self.duration = duration

    def __repr__(self):
        return f"{self.artist or 'Inconnu'} - {self.title}"


class Playlist:
    """Gère une liste de fichiers audio (MP3/FLAC)."""
    def __init__(self, name="Default Playlist"):
        self.name = name
        self.tracks = []

    def add_track(self, track):
        """Ajoute un morceau à la playlist."""
        self.tracks.append(track)

    def remove_track(self, track):
        """Supprime un morceau de la playlist."""
        self.tracks.remove(track)

    def list_tracks(self):
        """Affiche les morceaux de la playlist."""
        for t in self.tracks:
            print(t)

    def to_dict(self):
        """Transforme la playlist en dictionnaire pour l’export XML (XSPF)."""
        return {
            "title": self.name,
            "tracks": [
                {
                    "location": os.path.abspath(track.path),
                    "title": track.title,
                    "creator": track.artist,
                    "album": track.album,
                    "duration": track.duration
                }
                for track in self.tracks
            ]
        }