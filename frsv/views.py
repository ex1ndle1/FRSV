from django.shortcuts import render, redirect
from .forms import RegisterForm
import cv2
from insightface.app import FaceAnalysis
from .models import PeopleEmb


def make_emb(image):
        
    app = FaceAnalysis()
    app.prepare(ctx_id=-1)  
    img = cv2.imread(image)  
    faces = app.get(img)
    face = faces[0]
    embedding = face.embedding 
    emb_bytes = embedding.tobytes()
    
    return emb_bytes


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES) 
        if form.is_valid():

            person = form.save(commit=False)  
            print(person.image.path)
    else:
        form = RegisterForm()

    return render(request, 'frsv/register.html', {'form': form})




def users_info(request):
    datas = PeopleEmb.objects.all()
    
    return render(request , 'frsv/info.html', {"datas":datas}) 
