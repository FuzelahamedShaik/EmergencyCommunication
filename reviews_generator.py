import pandas as pd
from bs4 import BeautifulSoup
from google_play_scraper import reviews_all
from app_store_scraper import AppStore
import numpy as np
from deep_translator import GoogleTranslator

emergencyApps = [{'appName': 'Emergency Plus','googleId': 'com.threesixtyentertainment.nesn', 'googleLanguage': 'en', 'googleCountry': 'se'},
                  {'appName': 'Panic Button | Emergency SOS','googleId': 'com.solvaday.panic_alarm', 'googleLanguage': 'en', 'googleCountry': 'se'}]

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
  googleAppReviewsdf.rename(columns = {'reviewId':'Review Id','userName':'User Name', 'content':'Review', 'score':'Rating', 'at':'Date of Review'}, inplace = True)
  splittedReviewList = PrepareDataForTranslation(googleAppReviewsdf)
  googleAppReviewsdf['Review'] = TranslateReviewContent(splittedReviewList);
  googleAppReviewsdf['Review'].replace([valueToFillForEmptyReviews], '')
  return googleAppReviewsdf

headers = ["Review Id", "User Name" ,"Review","Rating", "Date of Review", "reviewCreatedVersion"] 
translator = GoogleTranslator(source='auto', target='en')

for app in emergencyApps: 
  
  googleAppReviewsdf = ExtractAndTranslateGoogleReviews(app)
  #appleAppReviewsdf = ExtractAndTranslateAppleReviews(app)

  #combinedReviewsdf = pd.concat([googleAppReviewsdf, appleAppReviewsdf])
  googleAppReviewsdf['Date of Review'] = googleAppReviewsdf['Date of Review'].dt.date
  googleAppReviewsdf.to_csv(app['appName'].replace('|','')+' play store '+'se'+'.csv', index=None, columns = headers, header=True)

  print(app['appName']+".csv file is created sucessfully. Check the files folder in left side bar. If you can't see yet refresh the folder.")