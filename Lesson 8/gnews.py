from gnewsclient import gnewsclient

clint = gnewsclient()
clint.query = "sports india"
news = clint.get_news()

print(news)