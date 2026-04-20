from urllib import request
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import concurrent.futures
from .models import AdminDocuments
import os

@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_documents(request):
    try:
        if request.method == 'POST':
            institution = request.POST.get('institution')
            modul = request.POST.get('modul')
            description = request.POST.get('description')
            userName = request.POST.get('userName')

            if 'document' in request.FILES:
                file = request.FILES['document']
                aktuelles_verzeichnis = os.getcwd()
                folder_path = os.path.abspath(os.path.join(aktuelles_verzeichnis, "adminBereich\\documents\\"))
                file_path = os.path.join(folder_path, file.name)
                print(file_path)
                if os.path.exists(file_path):
                    return HttpResponse('Die Datei existiert bereits.', status=400)
                else:

                    print("UserID:", userName, modul, description, institution)
                    admin_document = AdminDocuments.objects.create(
                        name=file.name,
                        institution=institution,
                        modul=modul,
                        filePath=file_path,
                        description=description,
                        userName=userName
                    )
                    with open(file_path, 'wb') as destination_file:
                        for chunk in file.chunks():
                            destination_file.write(chunk)
                    
                    print("before name")
                    if admin_document is not None:
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            executor.submit(create_vectorstore, file_path)
                        print("after")
                return HttpResponse('Das Dokument wurde erfolgreich Hochgeladen :')
            else:
                return HttpResponse({'error': 'Es wurde keine Datei bereitgestellt.'}, status=400)
        else:
            return HttpResponse({'error': 'Nur POST-Anfragen sind erlaubt.'}, status=405)
    except Exception as e:
        return HttpResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def edit_documents(request):
    try:

        admin_document = AdminDocuments.objects.get(pk=request.POST.get('id'))
        admin_document.institution = request.POST.get('institution')
        admin_document.modul = request.POST.get('modul')
        admin_document.description = request.POST.get('description')

        
        
        admin_document.save()
        return HttpResponse('Erfolgreich aktualisiert!')
    except AdminDocuments.DoesNotExist:
        return "Dokument mit ID {} nicht gefunden.".format(id)
    

@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])   
def load_documents(request, username):
    try:
        
        documents = AdminDocuments.objects.filter(userName=username).values()
        
       
        return JsonResponse({'documents': list(documents)})

    except Exception as e:
       
        return HttpResponse({'error': str(e)}, status=500)
    

@csrf_exempt
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])   
def delete_document(request, id):
    try:
        document = AdminDocuments.objects.get(pk=id)
        file_path = document.filePath
        if os.path.exists(file_path):
            os.remove(file_path)
        
        document.delete()
        
        return HttpResponse('Das Dokument wurde erfolgreich gelöscht')
    
    except AdminDocuments.DoesNotExist:
        return HttpResponse({'error': 'Das Dokument wurde nicht in der Datenbank gefunden.'}, status=404)
    
    except Exception as e:
        return HttpResponse({'error': 'Es ist ein Fehler beim Löschen des Dokuments aufgetreten: {}'.format(str(e))}, status=500)
    


def create_vectorstore(file_path: str):
    try:
        print(f"Erstelle Vectorstore für Datei: {file_path}")
        print(create_vectorstore_pickle(file_path))
        return {"message": "Vectorstore erfolgreich erstellt."}
    except Exception as e:
        return {"message": f"Fehler beim Erstellen des Vectorstores: {str(e)}"}   
    

load_dotenv("../.env")

OPENAI_KEY = os.getenv('OPENAI_KEY')

#DB = "postgresql://postgres:postgres@localhost:5432/postgres" 
DB = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')
connection_string = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

#Der Filepath muss für den Server angepasst werden
def getDocument(file_path:str):
    try:
        print(file_path)
        # Überprüfe, ob die Datei existiert/ Muss auch Serverseitig erfolgen
        if os.path.exists(file_path):
            loader = PyPDFLoader(file_path, extract_images=True)
            pdf_pages = loader.load_and_split()
            print("there was something")
            return pdf_pages
        else:
            print("there was nothing")
            return None
    except Exception as error:
        print("Fehler beim Lesen des Dokuments:", error)
        return None
    

def create_vectorstore_pickle(file_path: str):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100, )
        documents = text_splitter.split_documents(getDocument(file_path))
        print("Das Dokument wurde gesplittet")
        #Hier der Collectionname zu einer existierende anpassen! Siehe Init
        store = PGVector(
        collection_name= "meinedokumenten",
        connection_string=connection_string,
        embedding_function=embeddings,
        )
        addedVectore = store.add_documents(documents)
        if (addedVectore is None) :
            return "Das Dokument wurde nicht geadded"
        else :
            return "Dokument erfolgreich hochgeladen"
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)