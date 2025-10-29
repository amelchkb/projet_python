# -*- coding: utf-8 -*-
"""
directory_scanner.py
Exploration récursive d'un dossier pour trouver des fichiers MP3/FLAC.
filtrage par extension ET par type MIME, parcours de toute l'arborescence.
"""

from __future__ import annotations
from pathlib import Path
from typing import Iterable, List, Set, Optional
import mimetypes
import os

# Vérification de contenu facultative via mutagen (écarte quelques faux positifs MIME)
from mutagen import File as MutagenFile


class DirectoryScanner:
    """
    Scanner de dossiers récursif.
    - Filtre par EXTENSION (".mp3", ".flac")
    - Filtre par TYPE MIME ("audio/mpeg", "audio/flac")
    - Optionnel : vérifie que mutagen peut ouvrir le fichier (sanity check)
    """

    SUPPORTED_EXTS: Set[str] = {".mp3", ".flac"}
    SUPPORTED_MIMES: Set[str] = {"audio/mpeg", "audio/mp3", "audio/flac"}  # selon plateformes

    def __init__(self, include_hidden: bool = False, sanity_check_with_mutagen: bool = True):
        self.include_hidden = include_hidden
        self.sanity_check = sanity_check_with_mutagen

    def _is_hidden(self, path: Path) -> bool:
        # Cache les fichiers/dossiers commençant par un point si demandé
        return any(part.startswith(".") for part in path.parts)

    def _looks_supported(self, p: Path) -> bool:
        """Test rapide extension + MIME."""
        if p.suffix.lower() not in self.SUPPORTED_EXTS:
            return False
        mime, _ = mimetypes.guess_type(str(p))
        if mime not in self.SUPPORTED_MIMES:
            # Certains systèmes renvoient None pour FLAC → on tolère si extension OK
            if p.suffix.lower() == ".flac" and mime is None:
                return True
            return False
        return True

    def _mutagen_ok(self, p: Path) -> bool:
        """Vérifie que mutagen reconnaît le fichier audio (sécurise les cas limites)."""
        try:
            mf = MutagenFile(str(p))
            return mf is not None
        except Exception:
            return False

    def iter_files(self, root: str | Path) -> Iterable[Path]:
        """
        Générateur sur tous les fichiers audio valides dans l'arborescence.
        Respecte : filtrage extension + MIME (exigence du sujet).
        """
        root_path = Path(root)
        if not root_path.exists():
            return  # rien

        for dirpath, dirnames, filenames in os.walk(str(root_path)):
            # Option : filtrer les dossiers cachés
            if not self.include_hidden:
                dirnames[:] = [d for d in dirnames if not d.startswith(".")]

            for name in filenames:
                p = Path(dirpath, name)

                if not self.include_hidden and self._is_hidden(p):
                    continue

                if not self._looks_supported(p):
                    continue

                if self.sanity_check and not self._mutagen_ok(p):
                    # mime disait OK mais mutagen ne sait pas l'ouvrir → on écarte
                    continue

                yield p.resolve()

    def scan(self, root: str | Path) -> List[str]:
        """
        Retourne la liste *str* des chemins valides (utilisable directement en CLI).
        """
        return [str(p) for p in self.iter_files(root)]
