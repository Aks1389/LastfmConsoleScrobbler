import tinytag
import time
from datetime import datetime

def get_track_info(track_path):
    track = tinytag.TinyTag.get(track_path)
    
    return {
        "artist": track.artist,
        "track": track.title,
        "album": track.album,
        "duration": track.duration,
        "chosenByUser": 1
    }

def get_track_list(filepath, start_time):
    # batch_track_limit = 50
    date_time = datetime.strptime(start_time, '%d-%m-%Y_%H:%M %z')
    start_timestamp = time.mktime(date_time.timetuple())
    with open(filepath, "r", encoding='utf-8') as file:
        tracklist = file.read().splitlines()
    
    tracks = {}
    prev_track_duration = 0
    for i in range(0, len(tracklist)):
        track_info = get_track_info(tracklist[i])
        if i==0:
            timestamp = start_timestamp
        else:
            timestamp += prev_track_duration + 30
        track = {
            f"artist[{i}]": track_info["artist"],
            f"track[{i}]": track_info["track"],
            f"album[{i}]": track_info["album"],
            f"timestamp[{i}]": int(timestamp),
            f"chosenByUser[{i}]": 1
        }
        prev_track_duration = track_info["duration"]
        tracks.update(track)
    return tracks