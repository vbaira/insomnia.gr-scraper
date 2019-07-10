#Script to showcase the use of InsomniaScraper and Analysis classes

import sys
from scraper import InsomniaScraper
from analysis import Analysis


def main():
	if len(sys.argv)<=1:
		print("usage: python main.py <input_file>")
		sys.exit()	
	input_file = sys.argv[1]

	#create a scraper object
	scraper = InsomniaScraper(input_file)

	#start scrapping for data and collect them to "output.csv"
	scrapped_data_file = input("Export scrapped data to file : ")
	if (".csv" not in scrapped_data_file):
		scrapped_data_file += ".csv" 
	scraper.scrap(scrapped_data_file)	

	#clean and analyze scrapped data
	an = Analysis(scrapped_data_file)

	wordcloud_file = input("Save wordcloud of posts to file : ")
	if (".png" not in wordcloud_file):
		wordcloud_file += ".png" 	
	an.generate_wordcloud(wordcloud_file)

	plot1 = input("Save post/hour plot to file : ")
	if (".png" not in plot1):
		plot1 += ".png" 	
	an.post_time_plot(plot1)

	plot2 = input("Save user preference plot to file : ")
	if (".png" not in plot2):
		plot2 += ".png" 	
	an.user_preference(plot2)



if __name__ == '__main__':
	main()

