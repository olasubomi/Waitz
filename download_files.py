import boto3
import botocore
import json

# access data from Amazon
BUCKET_NAME = 'waitz-spring-interview-dataset'
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)


# store data objects in local directory for extracting and processing 

biomed_list = []
geisel_list = []

for key in bucket.objects.all():
	KEY = key.key

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
for file in geisel_list:
	data = json.load(open(file))
	pprint(data)
	break


