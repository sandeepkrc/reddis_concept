from django.shortcuts import render
from .models import Fruit
from django.core.cache import cache
from django.http import JsonResponse

# Create your views here.
def home(request):



    data=[]
    db=None
    if cache.get('fruits'):
        data= cache.get('fruits')    
        db ="reddis"
    else:
        objs=Fruit.objects.all()
        for obj in objs:
            data.append(obj.name)
            db="SQLLITE"
        cache.set('fruits',data)  
    return JsonResponse({"status":200,"db":db,"data":data})