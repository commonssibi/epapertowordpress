#!/usr/bin/env python

'''
Author: Prasanna Venkadesh, Sibi Kanakaraj
License: GNU GPL
'''

import os
import urllib
import datetime
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs

class Theekathir_Parser:
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.published_date = None
        self.data = {}

    def parse(self, news_id):
        
        full_url = self.base_url + str(news_id)
        
        # Hit the URL and fetch the HTML content
        print("Hitting the Url...")
        response = urllib.urlopen(full_url)
        
        if response.code == 200:
        
            # Find sections using BeautifulSoup
            soup = BeautifulSoup(response)
            title = soup.find("span", {"class": "Title"}).text.encode('utf8')
            sub_title = soup.find("span", {"class": "SubTitle"}).text.encode('utf8')
            news_content = soup.find("span", {"class": "News"}).text.encode('utf8')
        
            # getting published date from the queryparams
            href_text = soup.find("fb:like").get("href")
            query_params = parse_qs(urlparse(href_text).query)
            day = int(query_params.get('day')[0])
            month = int(query_params.get('month')[0])
            year = int(query_params.get('year')[0])
        
            self.published_date = datetime.date(year, month, day)
        
            # update result dictionary
            self.data['news_id'] = news_id
            self.data['title'] = title
            self.data['sub_title'] = sub_title
            self.data['news_content'] = news_content
            self.data['published_date'] = str(self.published_date)
            self.data['url'] = full_url
            
            return self.data
            
        else:
            return None
        

if __name__ == "__main__":

    # setup the parser configs
    theekathir_url = "http://epaper.theekkathir.org/news.aspx?NewsID="
    theekathir_parser = Theekathir_Parser(theekathir_url)
    
    # Destination to save the output of the parser
    output_folder = os.getenv('PWD') + "/theekathir_data/"
    
    # Check if the folder already exists. If not create one.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    news_id_start = int(raw_input("Enter a News ID to start with: "))
    no_of_news = int(raw_input("How many news to parse? "))
    
    try:
        with open(output_folder + 'output.txt', 'w') as outfile:
            for news_id in range(news_id_start, news_id_start + no_of_news):
                json_data = theekathir_parser.parse(news_id)
                if json_data is not None:
                    outfile.write( json_data.get('url') + '\n' + json_data.get('published_date') + '\n' + json_data.get('title') + '\n' +
                                    json_data.get('sub_title') + '\n' +
                                    json_data.get('news_content') )
		    outfile.write("\n" + ("-" * 20) + "\n")
                else:
                    print ("Unable to parse, Skipping News ID: %d" % news_id)
    except BaseException, be:
        print ("Exception Occured, Message: s", be)
        pass
        
    finally:
        print ("Finished. Output files are saved in %s" % output_folder)
