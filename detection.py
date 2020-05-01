import cv2
import sys
import creds_aws as cred
import boto3
import gmail_creds as creds
import smtplib

EMAIL_ADDRESS = creds.EMAIL_ADDRESS
EMAIL_PASSWORD = creds.EMAIL_PASSWORD
RECEIVER_EMAIL = " "
collection_id = " "
def send_mail():
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

            subject = "SECURITY BREACH!"
            body = "Potential security breach"
            msg = f'subject: {subject}\n\n{body}'
            try:
            	smtp.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL,msg)
            	print("[+] Email sent")
            except ConnectionError:
                print("[!] Your smtp port is filtered or closed!")
		



def send_to_aws(bytes_raw):
    detect_faces = client.detect_faces(
    Image={
        'Bytes': source_bytes},)
    if(detect_faces['FaceDetails'] == []):
        print('[!]No Faces Detected!')
    else:
        #print("Confidence Level : ",detect_faces['FaceDetails'][0]['Confidence'])
        search_faces = client.search_faces_by_image(
        CollectionId=collection_id,
        Image={'Bytes': bytes_raw},
        MaxFaces=1,
        FaceMatchThreshold=98)
        try:
            print("[+] Image id :"+search_faces['FaceMatches'][0]['Face']['ExternalImageId'])
        except IndexError:
            print("[+] An unregistered user has been detected sending an email to the admin now!")
            #send_mail()

access_key_id = cred.Access_key_ID
secret_access_key = cred.Secret_access_key
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
i = 1
source_bytes = ""
client = boto3.client('rekognition',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key,
                      region_name='us-east-2')
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.imwrite('img'+str(i)+'.jpg',frame)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        source_image = open("img"+str(i)+".jpg","rb")
        source_bytes = source_image.read()
        send_to_aws(source_bytes)
    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
