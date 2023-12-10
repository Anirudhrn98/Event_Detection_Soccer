from SoccerNet.Downloader import SoccerNetDownloader

mySoccerNetDownloader = SoccerNetDownloader(
    LocalDirectory="directory_toProject/Dataset")

# To download the videos, please first fill in this form:
# "https://docs.google.com/forms/d/e/1FAIpQLSfYFqjZNm4IgwGnyJXDPk2Ko_lZcbVtYX73w5lf6din5nxfmA/viewform"
mySoccerNetDownloader.password = "password"

# download game videos in low quality
mySoccerNetDownloader.downloadGames(files=["1_224p.mkv", "2_224p.mkv"],
                                   split=["train", "valid", "test", "challenge"])

# download labels SN v2
mySoccerNetDownloader.downloadGames(files=["Labels-v2.json"], split=["train","valid","test", "challenge"])
# download labels for camera shot
mySoccerNetDownloader.downloadGames(files=["Labels-cameras.json"], split=["train","valid","test", "challenge"] )
