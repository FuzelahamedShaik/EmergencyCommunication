import pandas as pd
from bs4 import BeautifulSoup
from google_play_scraper import reviews_all
from app_store_scraper import AppStore
import numpy as np
from deep_translator import GoogleTranslator
import os
import warnings
warnings.filterwarnings('ignore')

def PrepareDataForTranslation(reviews_dataframe):
  global valueToFillForEmptyReviews
  valueToFillForEmptyReviews = "No review Comment"
  reviews_dataframe['Review'] = reviews_dataframe['Review'].fillna(valueToFillForEmptyReviews)
  reviews_dataframe['Review'].str.replace('|', '')

  splittedArray =[]
  characterLength =0
  arrayChunk =[]
  for i in range(len( reviews_dataframe['Review'])):
    characterLength = characterLength + len(reviews_dataframe['Review'][i])
                                            
    if characterLength > 3000 :
        splittedArray.append(arrayChunk)
        arrayChunk =[]
        characterLength= len(reviews_dataframe['Review'][i])
        arrayChunk.append(reviews_dataframe['Review'][i])
                             
    else:
      arrayChunk.append(reviews_dataframe['Review'][i])

    if i == len(reviews_dataframe['Review'])-1 :
       splittedArray.append(arrayChunk)
   
  return splittedArray


def TranslateReviewContent(splittedReviewList):
  translatedReviews =[]
  concatednatedReviewString=""
  for i in range(len(splittedReviewList)):
     concatednatedReviewString = "|".join(splittedReviewList[i])
     translatedValue = translator.translate(concatednatedReviewString, dest='en')
     splittedTranslatedContent= translatedValue.split("|")
     translatedReviews = translatedReviews + splittedTranslatedContent
  return translatedReviews

def ExtractAndTranslateGoogleReviews(app):
  googleReviewResult = reviews_all( app['googleId'], 
                       lang= app['googleLanguage'], 
                       country=app['googleCountry'], 
                       )
  googleAppReviewsdf = pd.DataFrame(googleReviewResult)
  googleAppReviewsdf.rename(columns = {'reviewId':'Review Id','userName':'User Name', 'content':'Review', 'score':'Rating', 'at':'Date of Review','reviewCreatedVersion':'reviewCreatedVersion'}, inplace = True)
  splittedReviewList = PrepareDataForTranslation(googleAppReviewsdf)
  new_list = []
  for l in splittedReviewList:
    for r in l:
      new_list.append(r)
  #googleAppReviewsdf['Review'] = pd.Series(TranslateReviewContent(splittedReviewList))
  googleAppReviewsdf['Review'] = pd.Series(new_list)
  googleAppReviewsdf['Review'].replace([valueToFillForEmptyReviews], '')
  return googleAppReviewsdf

def ExtractAndTranslateAppleReviews(app):
  appleApp = AppStore(app_name=app['appStoreName'], app_id = app['appleAppId'], country=app['appleCountry'])
  appleApp.review(how_many=2000)
  appleAppReviewsdf = pd.DataFrame(appleApp.reviews)
  appleAppReviewsdf.dropna(how='all')
  appleAppReviewsdf.rename(columns = {'userName':'User Name', 'review':'Review', 'rating':'Rating', 'date':'Date of Review'}, inplace = True)
  splittedAppleReviewList = PrepareDataForTranslation(appleAppReviewsdf)
  #print(splittedAppleReviewList)
  new_list = []
  for l in splittedAppleReviewList:
    for r in l:
      new_list.append(r)
  #appleAppReviewsdf['Review'] = pd.Series(TranslateReviewContent(splittedAppleReviewList))
  appleAppReviewsdf['Review'] = pd.Series(new_list)
  appleAppReviewsdf['Review'].replace([valueToFillForEmptyReviews], '')
  return appleAppReviewsdf

emergencyApps = [{'appName': 'Emergency Plus','googleId': 'com.threesixtyentertainment.nesn', 'googleLanguage': 'en', 'googleCountry': 'fi', 
                                    'appStoreName':'emergency-plus','appleAppId' : '691814685', 'appleCountry': 'au'},
                {'appName': '112 Suomi','googleId': 'fi.digia.suomi112', 'googleLanguage': 'en', 'googleCountry': 'fi', 
                                    'appStoreName':'112-suomi','appleAppId' : '998281396', 'appleCountry': 'fi'},
                {'appName': 'SOS Alarm','googleId': 'se.sos.soslive', 'googleLanguage': 'en', 'googleCountry': 'se', 
                                    'appStoreName':'sos-alarm','appleAppId' : '1458725539', 'appleCountry': 'se'},
                {'appName': 'Hjelp 113','googleId': 'com.favouritesystems.android.emergencyapp.nla113', 'googleLanguage': 'en', 'googleCountry': 'no', 
                                    'appStoreName':'hjelp-113','appleAppId' : '363739748', 'appleCountry': 'no'},
                {'appName': 'Nødnummer','googleId': 'no.deepmind.SjomannskirkenBeredskap', 'googleLanguage': 'en', 'googleCountry': 'no', 
                                    'appStoreName':'nødnummer','appleAppId' : '688801563', 'appleCountry': 'no'},
                {'appName': '112 App','googleId': 'nl.maxbytes.app112', 'googleLanguage': 'en', 'googleCountry': 'dk', 
                                    'appStoreName':'112-app','appleAppId' : '1208094333', 'appleCountry': 'dk'},
                {'appName': 'Krisinformation.se','googleId': 'se.msb.krisinformation', 'googleLanguage': 'en', 'googleCountry': 'se', 
                                    'appStoreName':'krisinformation-se','appleAppId' : '514531751', 'appleCountry': 'se'}                                                          
]

headers = ["Review Id", "User Name" ,"Review","Rating", "Date of Review", "reviewCreatedVersion"] 

#headers = ["User Name" ,"Review","Rating", "Date of Review"] 
translator = GoogleTranslator(source='auto', target='en')

for app in emergencyApps: 

  googleAppReviewsdf = ExtractAndTranslateGoogleReviews(app)
  appleAppReviewsdf = ExtractAndTranslateAppleReviews(app)
  appleAppReviewsdf['Date of Review'] = appleAppReviewsdf['Date of Review'].dt.date
  combinedReviewsdf = pd.concat([googleAppReviewsdf, appleAppReviewsdf])
  file_name = app['appName']+'.csv'
  combinedReviewsdf = combinedReviewsdf[headers]
  parent_dir = "C:\\Users\\Fuzel Shaik\\Documents\\Master Thesis\\Data_extraction\\Dump"
  path = os.path.join(parent_dir,app['googleCountry'])
  if not os.path.exists(path):
    os.makedirs(path)
  file_path = os.path.join(path,file_name)
  combinedReviewsdf.to_csv(file_path, index=None, header=True)

  print('--------------------'+app['appName']+".csv file with "+ str(combinedReviewsdf.shape[0]) +" rows is created sucessfully. Check the files folder in left side bar. If you can't see yet refresh the folder.------------------------")