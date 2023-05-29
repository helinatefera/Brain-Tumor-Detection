from django.shortcuts import render
from django.conf import settings
import os
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
import cv2
from skimage import morphology
model= load_model('model.h5')

def front(request):
    if request.method == 'POST':
        imagee=request.FILES.get('imagee').file
        imagee = load_img(imagee, target_size=(200,200))
        img = np.array(imagee)
        img = img / 255.0
        img = img.reshape(1,200,200,3)
        label = model.predict(img)
        l=label[0][0]
        if l>0.5:
          text='Tumor Detected'
        else:
          text='No Tumor'
        file = request.FILES['imagee'] # assumes 'image' is the name of the file upload field in your form
        size = (250,250)
        image = Image.open(file)
        
        image.thumbnail(size)
        image_data = io.BytesIO()
        image.save(image_data, format='JPEG')
        image_data.seek(0)
        data_url = base64.b64encode(image_data.read()).decode()
        # image = plt.imshow(image,cmap='gray')
        # image= image.astype(np.uint8)
        # filtered_image = cv2.medianBlur(image, ksize=3)
        # thresholded_image = cv2.threshold(filtered_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # cleaned_image = morphology.remove_small_objects(thresholded_image.astype(bool), min_size=150)
        # # Find contours in the binary image
        # contours, _ = cv2.findContours(cleaned_image.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # # Find the contour with the maximum area (likely to be the tumor)
        # max_area = 0
        # max_contour = None
        # for contour in contours:
        #     contour_area = cv2.contourArea(contour)
        #     if contour_area > max_area:
        #         max_area = contour_area
        #         max_contour = contour
        a=plt.imshow(image)
      
        context={'l':l,'text':text,'ima':imagee,'data_url': data_url,'a':a}
        return render(request,'app/front.html',context)
    return render(request,'app/front.html')
def localization(request):
  if request.method == 'POST':
    file = request.FILES['imagee']
    # Load the MRI image
    context={'a':a}
    return render(request,'app/front.html',context)
  return render(request,'app/front.html')
def index(request):
  return render(request,'app/index.html')
def about(request):
  return render(request,'app/about.html')

  
@csrf_exempt
def brain_api(request):
    """
    List all code snippets, or create a new snippet.
    """
    # data = {
    #     "name": "Vaibhav",
    #     "age": 20,
    #     "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"]
    #          }

    # return JsonResponse(data)
    if request.method == 'POST':
      print(request.POST, request.FILES)
      imagee=request.FILES.get('imagee').file
      # imagee.flush()
      # print(imagee)
      # ima = request.POST['imagee']
      imagee = load_img(imagee, target_size=(200,200))
      img = np.array(imagee)
      img = img / 255.0
      img = img.reshape(1,200,200,3)
      label = model.predict(img)
      l=label[0][0]
      if l>0.5:
        text='Tumor Detected'
      else:
        text='No Tumor'
      context={'l':str(l),'text':text}
      return JsonResponse(context)
    return JsonResponse({"error": "Method not suported"}, status=200)

      