import boto3
import botocore
import os.path
import json
import matplotlib.pyplot as plt
import matplotlib 
import numpy as np
import pandas as pd
from datetime import datetime

# access data from Amazon
BUCKET_NAME = 'waitz-spring-interview-dataset'
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

biomed_list = []
geisel_list = []

# store data objects in local directory for extracting and processing 
for key in bucket.objects.all():
	KEY = key.key
# efficiency check if files have previosuly been downloaded,
# then skip this step when compiling and running
	if ((os.path.exists('./waitz_midterm_season_data/Biomed/'+KEY)) or
	(os.path.exists('./waitz_midterm_season_data/Geisel/'+KEY))):
# add files from dir to lists for processing
		biomed_list = os.listdir('./waitz_midterm_season_data/Biomed/')
		geisel_list = os.listdir('./waitz_midterm_season_data/Geisel/')
		break
# this algorithm assumes the mentined directories are already declared
# for data objects to be downloaded to
		try:
			if KEY.find("Biomed") != -1:
				biomed_list.append(KEY)
				s3.Bucket(BUCKET_NAME).download_file(KEY, 'waitz_midterm_season_data/Biomed/'+KEY )
			if KEY.find("Geisel")!=-1:
				geisel_list.append(KEY)
				s3.Bucket(BUCKET_NAME).download_file(KEY, 'waitz_midterm_season_data/Geisel/'+KEY )
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == "404":
				print("The object does not exist.")
			else:
				raise

#----------------------------------------------------------------------------------
# access data for visualization
biomed_list = sorted(biomed_list)
geisel_list = sorted(geisel_list)

file_count =0
for file in biomed_list:
	with open('waitz_midterm_season_data/Biomed/'+file) as json_file:
		data = json.load(json_file)
		dates=[]
		n_ppl =[]
		for date_str in data.keys():
			a_date = datetime.strptime(date_str, '%m/%d/%Y %H:%M')                     
			dates.append(a_date)
			n_ppl.append(data.get(date_str))
		plt.plot(dates, n_ppl)
		file_count+=1
		if file_count == 2:
			plt.suptitle('Biomed '+datetime.strftime(a_date, '%m/%d/%Y'))
			plt.show()
			file_count = 0



#-----------------------------------------------------------------------------------
count =0
for file in geisel_list:
	if file.find("a_Floor") != -1:
		count += 1
	with open('waitz_midterm_season_data/Geisel/'+file) as json_file:
		data = json.load(json_file)
		data_size = len(data)
		dates = []
		n_ppl = []
		#dates.append(date_str)
		#first_day_time = (dates[1])
		#last_day_time = (dates[-1])
		#drange = pd.date_range(start=first_day_time, end=last_day_time, freq='10M' )
		#print(drange)
		# vanilla coding to reduce clustering in visualization
		freq_count = 0;
		for date_str in data.keys():
			if freq_count == 0:
				a_date = datetime.strptime(date_str, '%m/%d/%Y %H:%M')					
				if(a_date.weekday() != 0):
					break
				just_time = datetime.strftime(a_date,'%H:%M')
				fmt_time = datetime.strptime(just_time, '%H:%M')
				print(fmt_time)
				dates.append(a_date)
				n_ppl.append(data.get(date_str))
	  		
			freq_count += 1
			if freq_count == 10:
		  		freq_count = 0

			#fmt_date = datetime.strftime(fmt_date,'%H:%M')
			#print(fmt_date)
			#dates = matplotlib.dates.date2num(dates)
			#plt.plot(dates, n_ppl)

#dates = pd.to_datetime(data.keys(), format='%m/%d/%Y %H:%M')
#print(type(dates[0]))

#s = pd.Series(n_people, index = dates)
#s.resample('10Min')
#print(s)

# convert dataframe from dictionary object
#print(df)
#plt.plot(data.keys(), data.values())
#plt.show()
#x_length = len(data)
#x = range(0, x_length)
#_, ax = plt.subplots()
#plt.scatter(data.keys(), data.values(), s = 1)
#ax.show()
#break
#plt.show()
