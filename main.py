#!/usr/bin/env python

import os
import requests
import pandas as pd
import time
from tqdm import tqdm
from helper import *

# Specify folder for downloading
# if none in mind, create downloads, otherwise specify
#folder = create_relative_path_if_not_exist('downloads')
folder = '/Users/Bryce/Documents/learning/texts/'

# Location of table for all books
table_url = 'https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4'
table = 'table_' + table_url.split('/')[-1] + '.xlsx'
table_path = os.path.join(folder, table)

# Get table of books
if not os.path.exists(table_path):
    books = pd.read_excel(table_url)
    # Save table
    books.to_excel(table_path)
else:
    books = pd.read_excel(table_path, index_col=0, header=0)

# Loop over and download all books
print()
for url, title, author, edition, isbn, category in tqdm(books[['OpenURL', 'Book Title', 'Author', 'Edition', 'Electronic ISBN', 'English Package Name']].values):

    # Get only specific categories of books
    # Test first with a small category of 'Economics and Finance'
    # Change categories in list for whatever you want to download
    if category in ['Computer Science', 'Economics and Finance', 'Mathematics and Statistics', 'Physics and Astronomy']:
        new_folder = create_relative_path_if_not_exist(os.path.join(folder, category))
    
        bookname = compose_bookname(title, author, edition, isbn)
        output_file = os.path.join(new_folder, bookname + '.pdf')
    
        # If book already downloaded, skip it
        if os.path.exists(output_file):
            continue
    
        try:
            r = requests.get(url)
            new_url = r.url.replace('%2F','/').replace('/book/','/content/pdf/') + '.pdf'
            download_book(new_url, output_file)
    
            # Download EPUB version too if exists
            # Uncomment if you want this version
            #new_url = r.url.replace('%2F','/').replace('/book/','/download/epub/') + '.epub'
            #output_file = os.path.join(new_folder, bookname + '.epub')
            #request = requests.get(new_url, stream = True)
            #if request.status_code == 200:
            #    download_book(new_url, output_file)
            
        except:
            print('\nProblem downloading: ' + title)
            time.sleep(30)
            continue

print('\nFinished downloading.')
