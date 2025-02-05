from continuum.algo import Algorithm
from alpaca.data.models.news import News
from os import getenv

class NewsTest(Algorithm):
	def __init__(self):
		super().__init__(getenv("API_KEY"), getenv("SECRET_KEY"), True)
		self.add_equity("TSLA")
		self.add_equity("F")
	
	def on_news(self, news: News):
		print(news)

if __name__ == '__main__':
	algo = NewsTest()
	algo.run()

