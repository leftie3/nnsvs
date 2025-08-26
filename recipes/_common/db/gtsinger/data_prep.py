"""Data preparation for GTSinger database."""

import cutlet
import sys
import unicodedata
from glob import glob
from os.path import expanduser, join
from shutil import rmtree, copytree
from pathlib import Path

import pysinsy
import yaml
from tqdm import tqdm


def create_temp_db(temp_db_root, songs, config):
    """Create temporary database."""
    Path.mkdir(temp_db_root, parents=True)
    katsu = cutlet.Cutlet()

    for song in songs:
        song_path = Path(song)

        # Skip excluded songs
        name = unicodedata.normalize("NFC", song_path.stem)

        if name in config["exclude_songs"]:
            print(f"Skipping {name}")
            continue

        # Convert Japanese song names to romaji
        romaji_parts = list(song_path.parts[-3:])
        romaji_parts[-1] = katsu.romaji(romaji_parts[-1])

        out_dir_path = temp_db_root / "_".join(romaji_parts)
        control_dir = song_path / "Control_Group"
        copytree(control_dir, out_dir_path)


def main():
    """Execute main routine."""
    # Load config
    config = None
    with open(sys.argv[1], "r", encoding="utf_8") as yml:
        config = yaml.load(yml, Loader=yaml.FullLoader)
    if config is None:
        print(f"Cannot read config file: {sys.argv[1]}.")
        sys.exit(-1)

    # generate full/mono labels by sinsy
    sinsy = pysinsy.sinsy.Sinsy()

    # Only Japanese is supported currently
    assert sinsy.setLanguages("j", config["sinsy_dic"])

    print("Convert musicxml to label files.")
    # Get directories to all songs, including duplicates
    songs = sorted(glob(join(expanduser(config["db_root"]), "Japanese", config["spk"], "*/*/")))

    temp_db_root = Path(config["out_dir"], "db")
    create_temp_db(temp_db_root, songs, config)

    temp_songs = sorted(temp_db_root.glob("*"))

    for song in tqdm(temp_songs):
        files = sorted(glob(join(song, "*.*xml")))
        for path in files:
            print(f"asserting {path}")
            assert sinsy.loadScoreFromMusicXML(path)

    rmtree(temp_db_root)


if __name__ == "__main__":
    # Handle expected command line arguments
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} config_path")
        sys.exit(-1)

    main()
