import spacy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer


#Class for cleanup , analysis and visualization of
#data scraped from insomnia.gr threads
class Analysis:

	#Read data from input file and perform a cleanup
	def __init__(self,input_file):
		self.data = pd.read_csv(input_file,sep='\t')
		self.data.loc[:,"time"]=pd.to_datetime(self.data["time"],format="%H:%M")
		self.__data_cleanup()
		##print(self.data.to_string())



	#Cleanup of messages 
	def __data_cleanup(self):
		#load spacy greek model and enchance stopwords with their non punctuated counterparts
		nlp = spacy.load("el")
		translationTable = str.maketrans("άέίήόύώ", "αειηουω")
		more_stopwords = [w.translate(translationTable) for w in nlp.Defaults.stop_words]
		more_stopwords.extend(["Και","Δεν"])
		for word in more_stopwords:
			nlp.vocab[word].is_stop = True

		#for each message perform cleanup opert
		for i,row in self.data.iterrows():
			s = row["message"]
			#remove punctuated letters
			s=s.translate(translationTable)
			#remove punctuation
			s = s.translate(str.maketrans( punctuation," "*len(punctuation) ))
			#tokenize and remove stopwords
			##tokens = nlp(s) 
			tokens = s.split()
			tokens = [t for t in  tokens if (not nlp.vocab[t].is_stop) and (len(t)>2) ]
			#place clean data into the original dataframe
			s=' '.join(tokens)
			(self.data).at[i,"message"] = s



	#Create a wordcloud of the most frequent terms in messages
	def generate_wordcloud(self,output_file):
		all_messages = ""
		for index,row in self.data.iterrows():
			all_messages += (" "+row["message"])
		wc = WordCloud(background_color="white", max_words=150)
		wc.generate(all_messages)
		wc.to_file(output_file)



	#Create a bar graph between number of posts and the hour they are posted
	def post_time_plot(self,output_file):
		#calculate post frequecy per hour
		self.data.set_index("time",drop="false",inplace=True)	#set time as index to use between_time()
		time_ranges = [str(i)+":00" for i in range (24)]
		time_ranges.append("23:59")
		post_freq = []
		for i,v in enumerate(time_ranges[:-1]):
			post_freq.append( len(self.data.between_time(time_ranges[i],time_ranges[i+1],include_end=False)) )

		#create the bar graph
		x_labels = [str(i)+":00-"+str(i+1)+":00" for i in range(24) ]
		x_pos = np.arange(len(x_labels))
		plt.bar(x_pos,post_freq,align="center")
		plt.xticks(x_pos,x_labels,rotation="vertical")
		plt.ylabel("Number of Posts")
		plt.title("Post per hour")
		plt.savefig(output_file,bbox_inches="tight")

		self.data.reset_index(inplace=True)		#reset index



	#Count references of each user to AMD/NVIDIA and plot the reference distribution
	def user_preference(self,output_file):
		vocabulary=["amd","vega","radeon","rtx","nvidia","2080ti","1080ti"]
		#group each user's messages
		users = self.data.groupby("author")["message"].apply(lambda message: ' '.join(message)).to_frame()
		users.reset_index(inplace=True)
		author_list = users["author"].tolist()
		#create word count vectors for each user using the above vocabulary 
		count_vectorizer = CountVectorizer(vocabulary=vocabulary)
		count_vectors = count_vectorizer.fit_transform(users["message"]).toarray()
		count_vectors = pd.DataFrame(count_vectors,index=author_list, columns=vocabulary)	#transform the count vectors into a dataframe
		#calculate amd and nvidia  references
		amd_ref,nvidia_ref=[],None
		for i,row in count_vectors.iterrows():
			total_ref = row.sum(axis=0)
			if total_ref == 0:
				amd_ref.append(0.5) #user is viewed as neutral
			else:
				amd_ref.append(row.iloc[0:4].sum()/total_ref)
		nvidia_ref = [1-i for i in amd_ref]

		#present results in a bar graph
		y_labels = author_list
		y_pos = np.arange(0,len(y_labels)*3,3)
		plt.figure(figsize=(50,100))
		p1 = plt.barh(y_pos, [1]*len(nvidia_ref) ,align="center",color='g',height=2)
		p2 = plt.barh(y_pos,amd_ref,align="center",color='r',height=2)
		plt.yticks(y_pos,y_labels,fontsize=25,rotation=45)
		plt.xticks(fontsize=50)
		plt.axvline(0.5,linewidth=6,linestyle="--",color='k')
		plt.legend((p1[0],p2[0]),("AMD","NVIDIA"),loc="upper left",fontsize=50)
		plt.title("User references to AMD/NVIDIA",fontsize=50)	
		plt.savefig(output_file,bbox_inches="tight")