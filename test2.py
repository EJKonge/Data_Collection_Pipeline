import boto3
import os

path ='C:/AiCore/Data_Collection_Pipeline/raw_data/images'
os.chdir(path)
for names in os.listdir():
    s3= boto3.client('s3')
    s3.upload_file(names, 'anime-cloud', 'Images/' + str(names) )