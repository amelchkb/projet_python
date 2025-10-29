# -*- coding: utf-8 -*-
"""
audiofile.py
Gestion des fichiers audio MP3/FLAC et extraction de métadonnées.
Lecture des méta (ID3 pour MP3, Vorbis Comment pour FLAC).
"""

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any

# mutagen gère de nombreux formats audio ; ici on utilise MP3 et FLAC
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.id3 import ID3NoHeaderError


@dataclass
class Metadata:
    """Structure simple et typée pour transporter les métadonnées utiles."""
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    track_no: Optional[str] = None
    duration_sec: Optional[int] = None
    year: Optional[str] = None
    genre: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "track_no": self.track_no,
            "duration_sec": self.duration_sec,
            "year": self.year,
            "genre": self.genre,
        }


class AudioFile(ABC):
    """
    Classe abstraite : factorise l'interface commune.
    Deux implémentations concrètes : MP3AudioFile et FLACAudioFile.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)

    @abstractmethod
    def read_metadata(self) -> Metadata:
        """Retourne les métadonnées sous forme d'objet Metadata."""
        raise NotImplementedError

    def get_metadata_as_str(self) -> str:
        """Formatage lisible en console pour la CLI."""
        md = self.read_metadata().to_dict()
        lines = [
            f"Titre   : {md.get('title') or ''}",
            f"Artiste : {md.get('artist') or ''}",
            f"Album   : {md.get('album') or ''}",
            f"Piste # : {md.get('track_no') or ''}",
            f"Année   : {md.get('year') or ''}",
            f"Genre   : {md.get('genre') or ''}",
            f"Durée   : {md.get('duration_sec') or 0} s",
            f"Fichier : {self.path}",
        ]
        return "\n".join(lines)

    @staticmethod
    def from_path(path: str | Path) -> "AudioFile":
        """
        Fabrique le bon type (MP3 ou FLAC) à partir de l'extension.
        NB: le scanner fait déjà un filtrage extension+MIME ; ici on reste simple.
        """
        p = Path(path)
        ext = p.suffix.lower()
        if ext == ".mp3":
            return MP3AudioFile(p)
        if ext == ".flac":
            return FLACAudioFile(p)
        raise ValueError(f"Format non supporté pour {p} (attendu .mp3 ou .flac)")  # conforme au sujet


class MP3AudioFile(AudioFile):
    """Gestion des MP3 (ID3)."""

    def __init__(self, path: str | Path):
        super().__init__(path)
        # charge le conteneur ; peut lever ID3NoHeaderError si pas de tag
        try:
            self.audio = MP3(self.path)
        except ID3NoHeaderError:
            # Fichier MP3 valide sans header ID3 : on charge quand même pour récupérer la durée
            self.audio = MP3(self.path)

    def _get_id3_text(self, frame: str) -> Optional[str]:
        """
        Récupère la première valeur texte d'un frame ID3 (ex: 'TIT2', 'TPE1', 'TALB', 'TDRC', 'TCON').
        Retourne None si absent.
        """
        tag = self.audio.tags
        if not tag or frame not in tag:
            return None
        value = tag.get(frame)
        try:
            # mutagen normalise souvent en objets avec .text (liste)
            text_list = getattr(value, "text", None)
            if isinstance(text_list, list) and text_list:
                return str(text_list[0])
            return str(value)
        except Exception:
            return None

    def read_metadata(self) -> Metadata:
        # Durée (en secondes entières)
        duration = None
        if self.audio and self.audio.info:
            duration = int(self.audio.info.length)

        # Champs ID3 courants
        title = self._get_id3_text("TIT2")
        artist = self._get_id3_text("TPE1")
        album = self._get_id3_text("TALB")
        year = self._get_id3_text("TDRC") or self._get_id3_text("TYER")
        genre = self._get_id3_text("TCON")
        track_no = self._get_id3_text("TRCK")

        return Metadata(
            title=title,
            artist=artist,
            album=album,
            track_no=track_no,
            duration_sec=duration,
            year=year,
            genre=genre,
        )


class FLACAudioFile(AudioFile):
    """Gestion des FLAC (Vorbis Comment)."""

    def __init__(self, path: str | Path):
        super().__init__(path)
        self.audio = FLAC(self.path)

    def _get_vorbis(self, key: str) -> Optional[str]:
        """
        Dans FLAC/Vorbis Comment, les champs sont des listes de chaînes.
        On prend la première si disponible.
        """
        try:
            values = self.audio.get(key, None)
            if not values:
                return None
            if isinstance(values, list) and values:
                return str(values[0])
            return str(values)
        except Exception:
            return None

    def read_metadata(self) -> Metadata:
        duration = None
        if self.audio and self.audio.info:
            duration = int(self.audio.info.length)

        title = self._get_vorbis("title")
        artist = self._get_vorbis("artist")
        album = self._get_vorbis("album")
        track_no = self._get_vorbis("tracknumber")
        year = self._get_vorbis("date") or self._get_vorbis("year")
        genre = self._get_vorbis("genre")

        return Metadata(
            title=title,
            artist=artist,
            album=album,
            track_no=track_no,
            duration_sec=duration,
            year=year,
            genre=genre,
        )
