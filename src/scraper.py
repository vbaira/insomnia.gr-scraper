import csv
import time
import requests
from bs4 import BeautifulSoup


#Class for scraping data from threads 
#of insomnia.gr website
class InsomniaScraper:

	#Initialize object by reading input_file containing the urls to be crawled.
	#Place them all in a list
	def __init__(self,input_file):
		self.urls=[]
		with open(input_file,'r') as file:
			for line in file:
			 	if line != '\n':
			 		self.urls.append(line.rstrip('\n'))



	#Scrap each given url and its pages for the data we want(authors,messages,publish date)
	def scrap(self,output_file="insomnia.csv"):
		authors,dates,times,messages=([] for i in range(4))
		for url in self.urls:
			next_page_url=url
			while next_page_url != '':
				response = requests.get(next_page_url)
				if not response :
					print("Unsuccessful request to URL-> ",next_page_url," , STATUS CODE : ",response.status_code)
					break
				soup = BeautifulSoup(response.text,"html.parser")
				
				#get an iterable object containing all the posts (<article> tag)
				posts = soup.find_all("article")

				#for each post get author,message,date
				for post in posts:
					authors.append( InsomniaScraper.__get_author(post) )

					datetime = InsomniaScraper.__get_datetime(post)
					dates.append(datetime[0])
					times.append(datetime[1])

					messages.append( InsomniaScraper.__get_message(post) )

				#go to the next page if there is one
				next_button = soup.find("li",class_="ipsPagination_next")
				if "ipsPagination_inactive" not in next_button.attrs["class"]:
					next_page_url = next_button.find('a').get("href")
				else:
					next_page_url=''
				#delay between requests to not overload server
				time.sleep(2)
		#export data		
		InsomniaScraper.__export_to_csv(output_file,authors,dates,times,messages)



	#Export scrapped data to csv file
	def __export_to_csv(output_file,authors,dates,times,messages):
		rows = zip(authors,dates,times,messages)
		with open(output_file,'w') as f:
			writer = csv.writer(f,delimiter='\t',quotechar='"',quoting=csv.QUOTE_ALL)
			writer.writerow(("id","author","date","time","message"))
			for id,row in enumerate(rows):
				writer.writerow((id,)+row)


				
	#Extract author from post
	def __get_author(post):
		author = post.find("span",style="color:#")
		if author == None :
			return "placeholder"
		else:		
			return author.get_text()



	#Extract date and time from post(<time> tag 'title' attr)
	def __get_datetime(post):
		datetime = post.find("time").get("title").split()
		#convert pm times to 24h format
		if ("μμ" in datetime[2]) and ("12:" not in datetime[1]) :
			x = datetime[1].split(':')
			datetime[1]=str(int(x[0])+12) + ":" + x[1]
		return datetime		



	#Extract message from post(text from <p> tags)
	def __get_message(post):
		message=""
		par = post.find_all('p')
		for p in par:
			message += (p.get_text(strip=True) + " ")
		return message



	#Print urls list
	def print_urls(self):
		for x in self.urls:
			print(x)
