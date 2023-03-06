import pandas as pd
from bs4 import BeautifulSoup
from google_play_scraper import reviews_all
from app_store_scraper import AppStore
import numpy as np
from deep_translator import GoogleTranslator

minecraft = AppStore(country='au', app_name='emergency-plus', app_id=691814685)
minecraft.review(how_many=20)

print(minecraft.reviews)