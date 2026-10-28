from django.urls import path, include
from .views import login1, svikvizovi, logout1, register1, prikaziKviz, sviTimoviKviza, top_kvizovi

urlpatterns = [
    path('', login1, name='login1'),
    path('kurcina/', svikvizovi, name="svikvizovi"),

    path('kurcina1/', logout1, name='logout1'),

    path('kurcina2/', register1, name='register1'),

    path('kurcina3/<int:kvizId>/', prikaziKviz, name='prikaziKviz'),

    path('kurcina4/<int:kvizId>/', sviTimoviKviza, name='sviTimoviKviza'),

    path('kurcina5/', top_kvizovi, name='top'),
]
