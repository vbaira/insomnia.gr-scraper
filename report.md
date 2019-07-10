#  isomnia.gr Data Scraper and Analysis of scraped data


### General

------

Project was developed and tested in Linux ennironment using the Anaconda python distribution.
Python version used was 3.7.3
Libraries used were : 

* [BeautifulSoup4](https://anaconda.org/anaconda/beautifulsoup4) for HTML parsing and  scraping of data
* [requests](https://anaconda.org/anaconda/requests) for making HTTP requests
* [wordcloud](https://github.com/amueller/word_cloud) for wordcloud generation
* [spacy](https://spacy.io/usage/) for nlp
* [matplotlib](https://matplotlib.org/) for plot generation
* pandas and numpy for data manipulation
* [sklearn](https://scikit-learn.org/stable/index.html) for its CountVectorizer class



### How to use

------

```
python main.py input_file
```

input_file is text file containing the insomnia.gr thread links to be crawled and scraped.

During execution the script prompts the user to insert the path where each output file will be placed. First file outputed is .csv containing the scraped data  which is then used for the analysis . Products of the analysis are 3 image files :

* A wordcloud of the most commonly used terms 
* A plot showcasing how many posts are posted per hour 
* A plot showing how many references each user made to AMD/NVIDIA



 ### Deliverables

------

#### src directory:

- **scraper.py** : contains InsomniaScraper class. An InsomniaScraper object is initialized with an input file which contains insomnia.gr thread links. Afterwards it scraps data from each link's thread(and all its pages) and outputs that data to a .csv file. Data scraped is :

  - post content
  - post author
  - posting date and time

- **analysis.py** : contains Analysis class. An Analysis object is initialized with  a csv file like the one exported from InsomniaScraper.

  Task of Analysis class is to clean the post contents and and use them to extract some insight about the data in the form of graphs and wordclouds.

* **main.py** : A script to showcase the use of InsomniaScraper and Analysis classes

  

   #### output directory :

Contains the output files produced by the classes above



### Comments about Analysis output

---

#### wordcloud

![](/home/yawda/Desktop/insomnia_scraper/output/wordcloud.png)

The wordcloud is produced using the 150 most common terms found in the posts(without stopwords).It is obvious that the threads were about amd/nvidia graphics cards and video games



#### Posts per hour

<img src="/home/yawda/Desktop/insomnia_scraper/output/post_hours.png " width="500" height="400" />

The above graph shows how many of the posts were posted during a certain hour of the day. As expected the peak of posting is around 12:00 pm and then it starts dropping gradually. The posting rate drops significantly during midnight and starts rising again around 5:00 am.



#### User preference

The graph below shows the distribution between  amd and nvidia references of each user. Users clearly refer to amd more , which is is expected mainly because the threads were about new releases of amd cards. Users who neither reference amd nor nvidia in their posts , are considered neutral .The graph is better viewed when zoomed in.

<img src="/home/yawda/Desktop/insomnia_scraper/output/user_preference.png " width="500" height="700" />

