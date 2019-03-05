from chatmiddleware.models import Lawyer
from chatmiddleware.serializers import LawyerSerializer, AOLSerializer, LanguageSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from chatmiddleware.relevance import relevance_generator
from google.cloud import translate
from .lawnet import search


client = translate.Client()


class LawyerList(generics.ListCreateAPIView):
    queryset = Lawyer.objects.all()
    serializer_class = LawyerSerializer


class LawyerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lawyer.objects.all()
    serializer_class = LawyerSerializer


@api_view(['POST'])
def queryAOL(request):
    if request.method == 'POST':
        dataRes = JSONParser().parse(request)
        sz = AOLSerializer(data=dataRes)
        if sz.is_valid():
            root = search(dataRes['intent_keywords'])
            citations = []
            for el in root.iter():
                if el.tag == 'Citation':
                    citations.append(el.text)
            if len(citations) > 0:
                lawyers = Lawyer.objects.filter(cases__icontains=citations[0])
                if len(citations) >  1:
                    for i in range(1, len(citations)):
                        if citations[i]:
                            lawyers = (lawyers | Lawyer.objects.filter(cases__icontains=citations[i]))
                relevant_lawyers = relevance_generator(lawyers, dataRes['aol_keywords'])
                lsz = LawyerSerializer(relevant_lawyers, many=True)
                return Response(lsz.data)
            else:
                root = search(dataRes['aol_keywords'])
                citations = []
                for el in root.iter():
                    if el.tag == 'Citation':
                        citations.append(el.text)
                lawyers = Lawyer.objects.filter(cases__icontains=citations[0])
                if len(citations) >  1:
                    for i in range(1, len(citations)):
                        if citations[i]:
                            lawyers = (lawyers | Lawyer.objects.filter(cases__icontains=citations[i]))
                relevant_lawyers = relevance_generator(lawyers, dataRes['aol_keywords'])
                lsz = LawyerSerializer(relevant_lawyers, many=True)
                return Response(lsz.data)
        return Response(sz.errors, status=400)


@api_view(['POST'])
def translate(request):
    if request.method == 'POST':
        dataRes = JSONParser().parse(request)
        sz = LanguageSerializer(data=dataRes)
        if sz.is_valid():
            translation = client.translate(sz.data['text'], target_language='en')
            return Response(translation['translatedText'])
        return Response(sz.errors, status=400)
