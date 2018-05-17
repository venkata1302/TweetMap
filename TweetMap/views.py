from django.shortcuts import render
import tweepy
import pandas as pd 
import gmplot
import os

consumer_key="upTlpctgIVW0AB3D6L43Fy08S"
consumer_secret="pI07xmzRPKEN3cdGjn17yfj8umEbJSkgIerEFYvmDNVyQOlrIy"
access_key="994291815217065984-B0KgQEDgO13Rc0DnwlzEfcOorIDqHEy"
access_secret="iDEZw6rVbhuN6UX9Q1OCDteiJTsGTOegvB8HBElB9tq3a"

def home(request):
    if request.method == 'POST':
        count_num = request.POST.get('number')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        alltweets = api.user_timeline(screen_name = 'MaplecroftRisk', count = count_num, include_entities = True, tweet_mode = 'extended')
        request.session['all_tweets'] = [x._json for x in alltweets]
        return render(request,'tweet.html',{'alltweets':alltweets})
    return render(request,'home.html')

def map(request):
    all_tweet = request.session['all_tweets']
    df = pd.read_csv('countries.csv',skiprows=[0],index_col = 0,names=['name','abbr','long','lat'])
    df.drop(df.columns[0],axis =1, inplace=True)
    my_dict = df.to_dict('index')
    latitude = []
    longitude = []
    text = []
    gmap = gmplot.GoogleMapPlotter(30,0,3)
    for j in all_tweet:
        for i in my_dict.keys():
            if i in j['full_text']:
                latitude.append(float(my_dict[i]['lat']))
                longitude.append(float(my_dict[i]['long']))
    gmap.scatter(latitude,longitude,'r',marker = False,size = 100000)
    gmap.draw((os.path.join(os.getcwd(),'templates/'))+"python_heatmap.html")
    return render(request,'python_heatmap.html')

