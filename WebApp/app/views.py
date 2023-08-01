import re
from django.shortcuts import render
from django.conf import settings
import os
import io
import base64
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.http import HttpResponse
from PIL import Image
from django.http import JsonResponse
import io
import base64
import matplotlib.pyplot as plt
import cv2 as cv
from PIL import UnidentifiedImageError  

model= load_model('Transfer_learningmodel_loss_0_0466_accuracy_0_9854_RMSprop_E18.h5')#load our model for the use of prediction

def front(request):
    context = {}
    if request.method == 'POST':#if the request from front side is 'POST'
        ext = str(request.FILES.get('imagee')).split('.')[-1]
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        imagee=request.FILES.get('imagee') #get the file path becouse we need the path for prediction
        file_extension = imagee.name[imagee.name.rfind('.'):].lower()
        imagee = imagee.file
        if file_extension in image_extensions:
            imagee = load_img(imagee, target_size=(224,224))#change the size of the image loaded to (224,224) becouse our model need that size of image
            img = np.array(imagee)#change our image to array using numpy(whice is as imported as np)
            img = img / 255.0 #divide it to 255 to reduce number result to range of [1,0] 1 for white and 0 for black
            img = img.reshape(1,224,224,3)#
            label = model.predict(img)#predict if there is tumor or not using our model loaded at line 22 
            #our result we look like this [[*,*,*,*]] like list of array in array ,so we will have result for each class of tumor
            #class while training =>>> [Glioma:0,Meningioma:1,No Tumor:2,Pituitary:3]
            l=max(label[0])#we will take maximum value from the result
            if l==label[0,0]:#if max value is at index 0 
              text="Glioma Tumor"#result output will be Glioma
              label_per=round(label[0,0]*100,2)#round value to decimal place  of 2
            elif l==label[0,1]:
              text="Meningioma Tumor"
              label_per=round(label[0,1]*100,2)
            elif l==label[0,2]:
              text="No Tumor"
              label_per=round(label[0,2]*100,2)
            else:
              text="Pituitary Tumor"
              label_per=round(label[0,3]*100,2)
            if l!=label[0,2]:
              tumor="Tumor Detected" #if there is tumor we will diplay "Tumor Detected" massages
            else:
              tumor=""
            print(label)
            file = request.FILES['imagee'] #'imagee' is the name of the file upload field in our form for user input
            size = (250,250)#size of output(one we display) image check line 75
            image = Image.open(file)#we are opening file from line 52
            image= np.array(image)#we change image to array to apply cv2 features 
            # Convert the image to grayscale
            if l!=label[0,2]:
               gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            # Apply a Gaussian blur to reduce noise
               blur = cv.GaussianBlur(gray, (5, 5), 0)
            # Apply a threshold to create a binary image
               _, threshold = cv.threshold(blur, 100, 255, cv.THRESH_BINARY)
            # Find contours in the binary image
               contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            # Iterate over the contours
               for contour in contours:
                  # Calculate the area of the contour
                  area = cv.contourArea(contour)
                  # Set a threshold for the minimum area of the tumor
                  min_area = 1000
                  if area > min_area:
                      # Draw a bounding rectangle around the contour
                      x, y, w, h = cv.boundingRect(contour)
                      cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            image = Image.fromarray(image)#change our array result at line 55 (becouse we are done using cv2) to file
            image.thumbnail(size) #resize image by (250,250)
            image_data = io.BytesIO() #create an in-memory binary stream
            image.save(image_data, format=ext) #save it as jpeg file
            image_data.seek(0) #absolute file positioning for our current saved file 
            data_url = base64.b64encode(image_data.read()).decode()#decode image file using base64 to use it as source file
            context.update({'l':str(l),"text":text,'data_url': data_url,"label_per":label_per,"tumor":tumor})#pass every result to display it on front part
            #for example we pass text from line 39 or 42 as 'text' on front side
        else:
            context.update({'error': 'Wrong file uploaded.'})

    return render(request,'app/front.html',context)

        
      

def index(request):
  return render(request,'app/index.html')#when we are at '/index' url we will render index.html file
def about(request):
  return render(request,'app/about.html')#when we are at '/about' url we will render about.html file
  
@csrf_exempt
def brain_api(request):
    context = {}
    if request.method == 'POST':#all the same on ,but it return JSON format(line 118) of our result for using it on moblie app side
      try:
        imagee=request.FILES.get('imagee').file
        ext = str(request.FILES.get('imagee')).split('.')[-1]
        imagee = load_img(imagee, target_size=(224,224))
        img = np.array(imagee)
        img = img / 255.0
        img = img.reshape(1,224,224,3)
        label = model.predict(img)
        l=max(label[0])
        if l==label[0,0]:
          text="Glioma_tumor"
          label_per=round(label[0,0]*100,2)
        elif l==label[0,1]:
          text="Meningioma_tumor"
          label_per=round(label[0,1]*100,2)
        elif l==label[0,2]:
          text="No tumor"
          label_per=round(label[0,2]*100,2)
        else:
          text="Pituitary_tumor"
          label_per=round(label[0,3]*100,2)
        if l!=label[0,2]:
          tumor="Tumor Detected"
        else:
          tumor=""
        file = request.FILES['imagee'] #'imagee' is the name of the file upload field in our form for user input
        image = Image.open(file)#we are opening file from line 52
        size = (300,300)#size of output(one we display) image check line 75
        image= np.array(image)#we change image to array to apply cv2 features 
        # Convert the image to grayscale
       
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # Apply a Gaussian blur to reduce noise
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        # Apply a threshold to create a binary image
        _, threshold = cv.threshold(blur, 100, 255, cv.THRESH_BINARY)
        # Find contours in the binary image
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # Iterate over the contours
        for contour in contours:
          # Calculate the area of the contour
          area = cv.contourArea(contour)
          # Set a threshold for the minimum area of the tumor
          min_area = 1000
          if area > min_area:
              # Draw a bounding rectangle around the contour
              x, y, w, h = cv.boundingRect(contour)
              cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
              
        
        image = Image.fromarray(image)
        image.thumbnail(size) #resize image by (250,250)
        image_data = io.BytesIO() #create an in-memory binary stream
        image.save(image_data, format="jpeg") #save it as file
        image_data.seek(0)
        data_url = base64.b64encode(image_data.read()).decode()#decode image file using base64 to use it as source file
        context={'l':str(l),"text":text,"label_per":label_per,"tumor":tumor,"data_url":data_url}
        return JsonResponse(context)
      except UnidentifiedImageError:
         return JsonResponse({'error': 'Invalid File Uploaded'})
    return JsonResponse({"error": "Method not suported"}, status=200)

      