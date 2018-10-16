import feedparser as fp
import json
import requests
import datetime

entries = fp.parse('https://thepiratebay.org/rss/top100/201')['entries']

replace = [".avi", "1.4", "5.1", "DVDRip", "DVDSCR", "BRRip", "XviD", "1CDRip", "aXXo", "[", "]", "(", ")", "{", "}",
           "{{", "}}", "x264", "x265", "720p", "StyLishSaLH (StyLish Release)", "DvDScr", "MP3", "HC HDRip", "HC HDRIP",
           "HDRip", "WebRip", "ETRG", "YIFY", "StyLishSaLH", "StyLish Release", "TrippleAudio", "EngHindiIndonesian",
           "385MB", "CooL GuY", "a2zRG", "x264", "Hindi", "AAC", "PSK", "CyBorG", "AC3", "MP3", " R6", "HDRip", "H264",
           "ESub", "AQOS", "ALLiANCE", "UNRATED", "ExtraTorrentRG", "BrRip", "mkv", "mpg", "DiAMOND", "UsaBitcom",
           "AMIABLE", "BRRIP", "XVID", "AbSurdiTy", "DVDRiP", "TASTE", "BluRay", "HR", "COCAIN", "_", ".", "BestDivX",
           "MAXSPEED", "Eng", "500MB", "FXG", "Ac3", "Feel", "Subs", "S4A", "BDRip", "FTW", "Xvid", "Noir", "1337x",
           "ReVoTT", "GlowGaze", "mp4", "Unrated", "hdrip", "ARCHiViST", "TheWretched", "www", "torrentfive", "com",
           "1080p", "1080", "SecretMyth", "Kingdom", "Release", "RISES", "DvDrip", "ViP3R", "RISES", "BiDA", "READNFO",
           "HELLRAZ0R", "tots", "BeStDivX", "UsaBit", "FASM", "NeroZ", "576p", "LiMiTED", "Series", "ExtraTorrent",
           "DVDRIP", "~", "BRRiP", "699MB", "700MB", "greenbud", "B89", "480p", "AMX", "007", "DVDrip", "h264", "phrax",
           "ENG", "TODE", "LiNE", "XVid", "sC0rp", "PTpower", "OSCARS", "DXVA", "MXMG", "3LT0N", "TiTAN", "4PlayHD",
           "HQ", "HDRiP", "MoH", "MP4", "BadMeetsEvil", "XViD", "3Li", "PTpOWeR", "3D", "HSBS", "CC", "RiPS", "WEBRip",
           "R5", "PSiG", "'GokU61", "GB", "GokU61", "NL", "EE", "Rel", "NL", "PSEUDO", "DVDScr", "Rip", "NeRoZ",
           "EXTENDED", "xvid", "WarrLord", "SCREAM", "MERRY", "XMAS", "iMB", "7o9", "Exclusive", "171",
           "DiDee", "v2", "WEB", "DL", "EVO", "EtMovies", "HEVC", "RMTeam", "X264", "N1C", "-EtMov", "Hive-CM8",
           "Hive CM8", "anoXmous", "CataVentos", "-Manning", "-"]

month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
              "Nov": 11, "Dec": 12}


def trim_magnet(magnet_link):
    show_name = magnet_link.replace(".", " ").strip()
    show_name = show_name.replace("+", " ").strip()
    for value in replace:
        show_name = show_name.replace(value, "")

    for y in range(1900, 2020):
        if str(y) in show_name:
            show_name = show_name.replace(str(y), "")

    return show_name


resp_list = []
for entry in entries:
    magnet_link = entry['title']
    if "HDCAM" not in magnet_link \
            and "TS" not in magnet_link \
            and "HD-TS" not in magnet_link \
            and "HDTS" not in magnet_link \
            and "HD-TC" not in magnet_link \
            and "HDTC" not in magnet_link:
        title = trim_magnet(magnet_link)
        try:
            url = "http://www.omdbapi.com/?t=" + title + "&tomatoes=true&apikey=1b1c7b21"
            resp = requests.get(url)
            jsonvalues = resp.json()
            if "Title" in jsonvalues:
                if "N/A" not in jsonvalues["Released"]:
                    date_list = jsonvalues["Released"].split()
                    year = int(date_list[2])
                    month = month_dict.get(date_list[1])
                    day = int(date_list[0])
                    new_date = "{}".format(datetime.date(year, month, day))
                    print(new_date)
                    jsonvalues["Released"] = new_date
                resp_list.append(jsonvalues)
        except KeyError:
            continue

with open("report.json", "w") as out_file:  # Writes output to file
    json.dump(resp_list, out_file)
