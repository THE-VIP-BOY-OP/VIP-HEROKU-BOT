import os
import shutil


def dir():
    files = [
        ".jpg",
        ".jpeg",
        ".mp3",
        ".m4a",
        ".mp4",
        ".webm",
        ".png",
        ".session",
        ".session-journal",
    ]

    for file in os.listdir():
        if any(file.endswith(ext) for ext in files):
            os.remove(file)

    if "downloads" in os.listdir():
        shutil.rmtree("downloads")
        os.mkdir("downloads")
