import tweepy

class MyListener(tweepy.Stream):
    def on_data(self, data):
        try:
            with open('tweettwo.json', 'wb') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = MyListener(
  "dH3QEI7Zrv5xgyM1JgNvPs7Ba", "oeN8HZJp3PIn3n0XZzMS7BePe4tI9FYz6ZBeIISAqV1YtpBMZI",
  "1031787320834486272-4rp0l8PIubzl3orECrFSXhH8UGwKvl", "aecV9aw9mrQcZkVSs73gBCqPH7oH7JpWGHUTsPwtQyMa2"
)
twitter_stream.filter(track=['#renewableenergy'])