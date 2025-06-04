"""Data preparation for GTSinger database."""

import sys
import unicodedata
from glob import glob
from os.path import expanduser, join
from pathlib import Path

import pysinsy
import yaml
from tqdm import tqdm


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
    # Get directories to all songs, including duplicates with different singing styles
    songs = sorted(glob(join(expanduser(config["db_root"]), "Japanese", config["spk"], "*/行*/")))

    for song_path in tqdm(songs):
        # Skip excluded songs
        name = unicodedata.normalize("NFC", Path(song_path).stem)

        if name in config["exclude_songs"]:
            print(f"Skipping {name}")
            continue


if __name__ == "__main__":
    # Handle expected command line arguments
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} config_path")
        sys.exit(-1)

    main()
