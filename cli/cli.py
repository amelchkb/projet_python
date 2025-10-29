import argparse
import sys
import os

# Import des modules de la bibliothèque (vos collègues vont les créer)
# Décommentez au fur et à mesure qu'ils sont disponibles
# from library.audiofile import AudioFile
# from library.directory_scanner import DirectoryScanner
# from library.playlist import Playlist

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from library.xspf_writer import write_xspf


def parse_arguments():
    """
    Parse les arguments de la ligne de commande.
    
    Returns:
        argparse.Namespace: Arguments parsés
    """
    parser = argparse.ArgumentParser(
        description="Gestionnaire de bibliothèque musicale MP3/FLAC",
        epilog="Exemple: python3 cli.py -f musique.mp3"
    )
    
    # Groupe mutuellement exclusif : soit fichier, soit dossier
    group = parser.add_mutually_exclusive_group(required=False)
    
    group.add_argument(
        '-f', '--file',
        type=str,
        metavar='FICHIER',
        help='Analyser un fichier MP3 ou FLAC'
    )
    
    group.add_argument(
        '-d', '--directory',
        type=str,
        metavar='DOSSIER',
        help='Scanner un dossier récursivement'
    )
    
    group.add_argument(
        '-p', '--play',
        type=str,
        metavar='FICHIER',
        help='Jouer un fichier audio'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        metavar='FICHIER.xspf',
        help='Fichier de sortie pour la playlist (format XSPF)'
    )
    
    return parser.parse_args()


def display_file_metadata(file_path):
    """
    Affiche les métadonnées d'un fichier audio.
    
    Args:
        file_path (str): Chemin vers le fichier
    """
    print(f"\n{'='*60}")
    print(f"Analyse du fichier : {file_path}")
    print(f"{'='*60}\n")
    
    # Vérifier que le fichier existe
    if not os.path.exists(file_path):
        print(f"❌ Erreur : Le fichier '{file_path}' n'existe pas.")
        sys.exit(1)
    
    # Vérifier l'extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ['.mp3', '.flac']:
        print(f"❌ Erreur : Format non supporté. Seulement MP3 et FLAC.")
        sys.exit(1)
    
    # TODO: Utiliser la classe AudioFile de vos collègues
    # audio = AudioFile(file_path)
    # metadata = audio.get_metadata()
    
    # Pour l'instant, affichage de démonstration
    print("📁 Informations du fichier :")
    print(f"  - Nom : {os.path.basename(file_path)}")
    print(f"  - Taille : {os.path.getsize(file_path)} octets")
    print(f"  - Format : {ext[1:].upper()}")
    
    print("\n🎵 Métadonnées :")
    print("  - Titre : [À implémenter avec AudioFile]")
    print("  - Artiste : [À implémenter avec AudioFile]")
    print("  - Album : [À implémenter avec AudioFile]")
    print("  - Durée : [À implémenter avec AudioFile]")
    print("  - Année : [À implémenter avec AudioFile]")
    
    # Exemple de ce que ça donnera :
    # print(f"  - Titre : {metadata['title']}")
    # print(f"  - Artiste : {metadata['artist']}")
    # print(f"  - Album : {metadata['album']}")
    # print(f"  - Durée : {metadata['duration']} secondes")


def scan_directory(directory_path, output_file=None):
    """
    Scanne un dossier récursivement et liste les fichiers audio.
    
    Args:
        directory_path (str): Chemin vers le dossier
        output_file (str, optional): Fichier de sortie pour la playlist
    """
    print(f"\n{'='*60}")
    print(f"Scan du dossier : {directory_path}")
    print(f"{'='*60}\n")
    
    # Vérifier que le dossier existe
    if not os.path.isdir(directory_path):
        print(f"❌ Erreur : Le dossier '{directory_path}' n'existe pas.")
        sys.exit(1)
    
    # TODO: Utiliser DirectoryScanner de vos collègues
    # scanner = DirectoryScanner(directory_path)
    # files = scanner.scan()
    
    # Pour l'instant, démonstration simple
    print("🔍 Recherche de fichiers MP3 et FLAC...\n")
    
    found_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.mp3', '.flac')):
                file_path = os.path.join(root, file)
                found_files.append(file_path)
                print(f"  ✓ {file_path}")
    
    print(f"\n📊 Total : {len(found_files)} fichier(s) trouvé(s)")
    
    # Si option -o spécifiée, créer la playlist
    if output_file:
        print(f"\n💾 Génération de la playlist : {output_file}")
        
        # Créer des objets factices pour le moment
        # TODO: Remplacer par les vraies classes Playlist et Track quand disponibles
        class SimpleTrack:
            def __init__(self, path):
                self.path = os.path.abspath(path)
                self.title = os.path.basename(path)
                self.artist = "Artiste inconnu"
                self.album = "Album inconnu"
                self.duration = None
        
        class SimplePlaylist:
            def __init__(self, name, files):
                self.name = name
                self.tracks = [SimpleTrack(f) for f in files]
        
        # Créer la playlist
        playlist = SimplePlaylist("Playlist générée automatiquement", found_files)
        write_xspf(playlist, output_file)
        
        print(f"🔗 Validez-la sur : https://validator.xspf.org/")


def play_file(file_path):
    """
    Joue un fichier audio.
    
    Args:
        file_path (str): Chemin vers le fichier
    """
    print(f"\n{'='*60}")
    print(f"Lecture du fichier : {file_path}")
    print(f"{'='*60}\n")
    
    if not os.path.exists(file_path):
        print(f"❌ Erreur : Le fichier '{file_path}' n'existe pas.")
        sys.exit(1)
    
    # TODO: Implémenter la lecture audio
    print("🎵 Lecture en cours...")
    print("⏸️  [Fonction de lecture à implémenter]")
    print("💡 Utilisez pygame.mixer ou python-vlc")


def main():
    """Fonction principale du programme CLI."""
    
    # Si aucun argument, afficher l'aide
    if len(sys.argv) == 1:
        print("❌ Erreur : Aucun argument fourni.")
        print("💡 Utilisez -h ou --help pour afficher l'aide.\n")
        sys.exit(1)
    
    # Parser les arguments
    args = parse_arguments()
    
    # Traitement selon les options
    if args.file:
        display_file_metadata(args.file)
    
    elif args.directory:
        scan_directory(args.directory, args.output)
    
    elif args.play:
        play_file(args.play)
    
    else:
        print("❌ Erreur : Option non reconnue.")
        print("💡 Utilisez -h ou --help pour afficher l'aide.\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programme interrompu par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        sys.exit(1)