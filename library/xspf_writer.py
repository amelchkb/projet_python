import xml.etree.ElementTree as ET

def write_xspf(playlist, output_file):
    """
    Génère un fichier XSPF à partir d'un objet Playlist.
    """
    # Élément racine
    playlist_el = ET.Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")

    # Titre de la playlist
    title_el = ET.SubElement(playlist_el, "title")
    title_el.text = playlist.name

    # Élément <trackList>
    tracklist_el = ET.SubElement(playlist_el, "trackList")

    for track in playlist.tracks:
        track_el = ET.SubElement(tracklist_el, "track")

        loc = ET.SubElement(track_el, "location")
        loc.text = f"file://{track.path}"

        if track.title:
            title = ET.SubElement(track_el, "title")
            title.text = track.title

        if track.artist:
            creator = ET.SubElement(track_el, "creator")
            creator.text = track.artist

        if track.album:
            album = ET.SubElement(track_el, "album")
            album.text = track.album

        if track.duration:
            duration = ET.SubElement(track_el, "duration")
            duration.text = str(track.duration)

    # Créer l’arbre XML et l’écrire dans un fichier
    tree = ET.ElementTree(playlist_el)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    print(f"✅ Playlist enregistrée sous : {output_file}")