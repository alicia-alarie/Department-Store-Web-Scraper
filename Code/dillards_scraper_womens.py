# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:42:45 2020

@author: alici
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 14:17:45 2020

@author: alici
"""
import re
import requests
import requests_ftp
import requests_cache
import lxml
from bs4 import BeautifulSoup
from collections import Counter
from matplotlib import pyplot as plt
plt.style.use('ggplot')
import pandas as pd
plt.style.use('ggplot')
requests_cache.install_cache('coll_cache')
import sqlalchemy as sqla
import numpy as np


## Create database engine
sqlite_file = 'final project\Data\Dillardswomen.sqlite'
dillards = sqla.create_engine('sqlite:///' + sqlite_file)
dillards.execute('CREATE TABLE "clothing" ('
                                           'name VARCHAR, '
                                           'brand VARCHAR,'
                                           'Womens INT,'
                                           'Mens INT,'
                                           'price FLOAT,'
                                           'description VARCHAR)')

#Dillards website for scraping
urlbase = "https://www.dillards.com/c/women"

for p in range(1,144):
    print('page:', p)
    #request data and store in beautiful soup object
    dataparams = {"pageNumber":p, "forceFlatResults":"forceFlatResults"}
    womensclothingreq = requests.get(urlbase,params=dataparams)
    womensclothingreq.url
    womensclothinghtml = womensclothingreq.text
    womensclothing = BeautifulSoup(womensclothinghtml,'lxml')
    

    collset_content = womensclothing.find_all(name='div',attrs={'class' : 'result-tile-below' })
    
    for collset in collset_content:
        #go to page referenced in tile and request it's information
        collset_a = collset.find(name='a')
        url ='https://www.dillards.com'+collset_a['href']
        req = requests.get(url)
        html = req.text
        
        #store in Beutiful Soup object
        wom = BeautifulSoup(html,'lxml')
        
        #parse price
        price = wom.find(name='span',attrs={'class' : 'price'}).text
        price=price.replace('$','')
        price=price.split('-')
        price=float(price[len(price)-1])
        print(price)
        
        #parse description
        descr = wom.find(name='div',attrs={'class' : 'col-sm-12 product-description'})
        if descr is None:
            descr=''
        else:
            descr=descr.text
        print(descr)
        
        #parse name
        name= wom.find(name='span',attrs={'class' : 'product__title--desc m-b-10'}).text
        print(name)
        
        #parse brand
        brand= wom.find(name='span',attrs={'class' : 'product__title--brand m-b-10'}).text
        print(brand)
        
        #set gender flags
        Womens=1
        Mens=0
        
        #add entry to sql database file
        sql = ''' INSERT INTO clothing("name","brand",Womens,Mens,price,"description")
                  VALUES("{name}","{brand}",{Womens},{Mens},{price},"{descr}") '''.format(name= name.replace('"',''),brand=brand.replace('"',''),Womens=Womens, Mens=Mens,price=price, descr=descr.replace('"',''),  if_exists='replace')
    
        dillards.execute(sql)#
        
    pd.read_sql_query("select count(*) from clothing", dillards)
    
    
