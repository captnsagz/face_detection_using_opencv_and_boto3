import cv2
import sys
import creds_aws as cred
import boto3


access_key_id = cred.Access_key_ID
secret_access_key = cred.Secret_access_key
collection_id = " "


client = boto3.client('rekognition',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key,
                      region_name='us-east-2')

if len(sys.argv) > 1:
	if sys.argv[1] == "-p":
		name = input("Enter the name of individual u want to add:")
		if len(sys.argv) > 2:
			photo = sys.argv[2]
			response = client.index_faces(CollectionId=collection_id,
    			Image={'Bytes': source_bytes},
    			ExternalImageId=name)
			print(response['FaceRecords'][0]['Face']['ExternalImageId'])
		else:
			print("[!] Name of photo missing!")
	elif sys.argv[1] == "-l":
		response = client.list_faces(
    		CollectionId=collection_id,MaxResults=123)
		length = len(response['Faces'])
		for i in range(length):
			print(response['Faces'][i]['ExternalImageId'])
	else:
		print("[!] Invalid argument!")
else :
	print("[!] Program requires an addittional arguments!")
	sys.exit(0)




