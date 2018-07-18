from flask import Flask,render_template,request,redirect
#import folium
import dill
import pandas as pd
import datetime
#import holidays
#import glob
import os
import json
import requests
#from bs4 import BeautifulSoup
import re
import numpy as np
#from scipy.stats import poisson

def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
        # Geoff Boeing
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

def getNumberFromOneTag_td(inTag):
    tempOutString = re.findall('(?<=\<td\>).*(?=.*\</td\>)',str(inTag))[0]
    tempOutString = ''.join([x for x in tempOutString if x in '0123456789.-'])
    if (not(tempOutString)):
        return 0.0
    else:
        return float(tempOutString)
    
app = Flask(__name__)
app.vars={}
app.vars['firstTime']=True

@app.route('/index_abc',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        if (app.vars['firstTime']):
            app.vars['window']=15
        try:
            #"""
            oDF = pd.read_csv('restAreas.csv')
            sendGJ = df_to_geojson(oDF,['name','spacesTotal','availability'],lat='latitude',lon='longitude')
            return render_template('withMap.html',num=app.vars['window'],gjFC_StationData=sendGJ) 
            #"""
        except:    
            #print('fail')
            oDF = pd.read_csv('restAreas.csv')
            sendGJ = df_to_geojson(oDF,['name','spacesTotal','availability'],lat='latitude',lon='longitude')
            return render_template('withoutMap.html',num=app.vars['window'],
                                   gjFC_StationData=sendGJ)
    else:
        #request was a POST
        tempInput = request.form['myWindow']
        app.vars['firstTime']=False
        try:
            app.vars['window'] = min([abs(int(float(tempInput))),60]) # limit one hour
        except:
            app.vars['window'] = 15 # default to 15 minutes, if input cannot be converted to numeric
        return redirect('/')


if __name__ == "__main__":
    app.run()