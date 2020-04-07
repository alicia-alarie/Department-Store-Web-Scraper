# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:05:51 2020

@author: alici
"""

import numpy as np
import pandas as pd

def add_categorygenderplus(db):
    #Add columns to the database for clothing type- jeans, shirt, blazer, jewelry, etc.
    accessories=((db.description.str.contains('bag ')) | (db.description.str.contains('hat '))|
                 (db.description.str.contains('purse '))|(db.description.str.contains('hair '))|
                 (db.name.str.contains('Belt ')))
    jeans=(db.description.str.contains('these jeans '))
    
    pants=(db.description.str.contains('these pants '))
    
    shirts=((db.description.str.contains('this shirt ')) | (db.description.str.contains('this blouse '))|
            (db.description.str.contains('this top '))|(db.description.str.contains('this tee')))
    
    blazer=(db.description.str.contains('this blazer ')) 
    
    jacket=(db.description.str.contains('this jacket '))|(db.description.str.contains('this coat '))
    
    sweater=((db.description.str.contains('this sweater'))| (db.description.str.contains('this sweatshirt '))|
             (db.description.str.contains('this knit')))
    
    jewelry=((db.description.str.contains('this bracelet')) | (db.description.str.contains('this necklace'))|
                (db.description.str.contains('these earring'))|(db.description.str.contains('this chain'))|
                (db.description.str.contains('this ring'))|(db.name.str.contains('Chain')))
                
    
    swimwear=(db.description.str.contains('swim')) | (db.description.str.contains('bathing'))
    
    dresses=(((db.description.str.contains('this dress')) | (db.description.str.contains('this gown'))|
              (db.name.str.contains('Gown'))) & (db.Womens==1))
    
    skirt=(db.description.str.contains('this skirt features')) & (db.Womens==1)
    
    suit=((db.description.str.contains('this suit '))|(db.description.str.contains('this skirt suit '))|
          (db.description.str.contains('this Tuxedo'))|(db.description.str.contains('this 2-piece tuxedo ')))
    
    jumpsuit=(db.description.str.contains('this jumpsuit '))
    
    robe=(db.description.str.contains('this robe '))
    
    shorts=(db.description.str.contains('these shorts '))
    
    plus=((db.description.str.contains('plus'))| (db.name.str.contains('Plus'))|(db.name.str.contains('Big'))|
          (db.description.str.contains('Big & Tall')))
    petite=(db.description.str.contains('petite'))| (db.name.str.contains('Petite'))
    
    #Add the item categories to the database
    db['category']='miscellaneous'
    db.category[accessories]='accesories'
    db.category[jewelry]='jewelry'
    db.category[shirts]='shirt'
    db.category[sweater]='sweater'
    db.category[blazer]='blazer'
    db.category[jacket]='jacket'
    db.category[pants]='pants'
    db.category[jeans]='jeans'
    db.category[swimwear]='swimwear'
    db.category[dresses]='dresses'
    db.category[skirt]='skirt'
    db.category[suit]='suit'
    db.category[robe]='robe'
    db.category[shorts]='shorts'
    db.category[jumpsuit]='jumpsuit'
    db=db[db.category!='miscellaneous']
    
    #Add the plus/pertite/regular data to the database
    db['pluspetite']='regular'
    db.pluspetite[plus]='plus'
    db.pluspetite[petite]='petite'
    
    #Add gender information to the database
    db['gender']=''
    db.gender[db.Mens==1]='Mens'
    db.gender[db.Womens==1]='Womens'
    
    #Add pricerange
    db['pricerange']=np.around(db.price,decimals=-1)
    
    return db