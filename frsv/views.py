
from django.shortcuts import render, redirect
from .forms import RegisterForm
import cv2
from insightface.app import FaceAnalysis
from .models import PeopleEmb
import numpy as np
from django.db.models import Max



def make_emb(image):
    app = FaceAnalysis()
    app.prepare(ctx_id=-1)  
    data = np.fromfile(image, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)

    faces = app.get(img)

    embedding = faces[0].embedding 
    emb_bytes = embedding.tobytes()
    
    return emb_bytes



def register(request):
    id =  PeopleEmb.objects.aggregate(Max('id'))
    
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES) 

        if form.is_valid():

            person = form.save(commit=False)  
            
            try:
                person.save()
                
            except TypeError:
                try:
                 print(person.image.path)
                 
                 person.vector = make_emb(person.image.path)
                 person.id = id['id__max'] + 1
                 person.save()

                except Exception:
                    print('error')
                
                
    else:
        form = RegisterForm()

    return render(request, 'frsv/register.html', {'form': form})




def users_info(request):
    datas = PeopleEmb.objects.all()
    
    return render(request , 'frsv/info.html', {"datas":datas}) 
