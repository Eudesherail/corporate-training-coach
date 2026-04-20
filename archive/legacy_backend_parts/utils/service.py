import requests
import json
import os
import datetime
import psycopg2
from psycopg2 import sql
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import random
from fastapi import HTTPException, Header
from dotenv import load_dotenv
from fastapi import HTTPException, Header
from functools import wraps
from utils.logger import setup_logger


logger = setup_logger(__name__)
# Error handling decorator
def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request Error in {func.__name__}: {e}")
            raise HTTPException(status_code=500, detail=f"Error in {func.__name__}: {e}")
        except Exception as e:
            logger.error(f"Unexpected Error in {func.__name__}: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error in {func.__name__}")
    return wrapper

load_dotenv("../.env")
# URL of the backend.
BASE_URL = "http://localhost:8080/api"
#BASE_URL = os.getenv('SPRING_URL', 'http://localhost:8080/api')


OPENAI_KEY = os.getenv('OPENAI_KEY')

# Postgres db url for the chat history.
#DB = "postgresql://postgres:postgres@localhost:5432/postgres" 
DB = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')

load_dotenv()

connection_string = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

#Der Filepath muss für den Server angepasst werden
def getDocument(document_name: str):
    aktuelles_verzeichnis = os.getcwd()
    übergeordneter_ordner = os.path.abspath(os.path.join(aktuelles_verzeichnis, "..\\"))
    folder_path = os.path.abspath(os.path.join(übergeordneter_ordner, "backend\\src\\main\\java\\com\\stubu\\studybuddy\\api\\Admin\\documents\\"))
    try:
        file_path = os.path.join(folder_path, document_name)
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
#insert the ducuments zu the database
def create_vectorstore_pickle(docname: str):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100, )
        documents = text_splitter.split_documents(getDocument(docname))
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


# Extract the token from the Authorization header.
@error_handler
def get_token(authorization: str = Header(default="")):
    # if "bearer" not in authorization.lower():
    #     raise HTTPException(status_code=403, 
    #     detail="Unauthorized: Bearer token not found")
    return authorization.split(" ")[1]

# Create headers with Authorization Token.
def create_headers(token: str):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

# Fetch the user goal from the backend.
@error_handler
def get_goal(token: str, user_id: int):
    headers = create_headers(token)
    request_url = f"{BASE_URL}/users/{user_id}/goals"
    response = requests.get(request_url, headers=headers)
    data = json.loads(response.text)
    goal = data[0] if data else "none"
    return goal

# Set or update a user goal.
@error_handler
def set_goal(token: str, user_id: int, goal: str, enddate: str):
    headers = create_headers(token)
    oldGoal = get_goal(token, user_id)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    goalData = {
        "goal": goal,
        "startDate": current_date,
        "endDate": enddate,
    }
    if oldGoal == "none":
        request_url = f"{BASE_URL}/users/{user_id}/goals"
        response = requests.post(request_url, headers=headers, data=json.dumps(goalData))
    else:
        goalId = oldGoal["id"]
        request_url = f"{BASE_URL}/users/{user_id}/goals/{goalId}"
        response = requests.put(request_url, headers=headers, data=json.dumps(goalData))
    return response

# Fetch the user state from the backend.
@error_handler
def get_state(token: str, user_id: int, bot_id: int):
    header = create_headers(token)

    response = requests.get(
        f"{BASE_URL}/states?userId={user_id}&botId={bot_id}",
        headers=header
    )

    if response.status_code == 200:
        return response.json().get("currentState")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Set the user state in the backend.
@error_handler
def set_state(token: str, user_id: int, bot_id: int, state_value: int):
    headers = create_headers(token)
    request_url = f"{BASE_URL}/states?userId={user_id}&botId={bot_id}"
    payload = {
        "currentState": state_value
    }
    response = requests.put(request_url, headers=headers, data=json.dumps(payload))
    return response.json()

# Fetch the user agent from the backend.
@error_handler
def get_bot(token: str, user_id: int):
    headers = create_headers(token)
    requests_url = f"{BASE_URL}/user/{user_id}/bot"
    response = requests.get(requests_url, headers=headers)
    return response.json()

# Set the user agent in the backend.
@error_handler
def set_bot(token: str, user_id: int, bot_id: int):
    headers = create_headers(token)
    requests_url = f"{BASE_URL}/user/{user_id}/bot/{bot_id}"
    response = requests.put(requests_url, headers=headers)
    return response.json()

# get all questions from one topic
@error_handler
def get_questions_by_topic(token: str, topicId: int):
    headers = create_headers(token)
    requests_url = f"{BASE_URL}/questions/topic/{topicId}"
    response = requests.get(requests_url, headers=headers)
    response = response.json()
    qa = response[random.randint(0, len(response)-1)]
    return qa

# get quiz state
@error_handler
def get_current_status(token: str, userId: int):
    headers = create_headers(token)
    requests_url = f"{BASE_URL}/current_status?userId={userId}"
    response = requests.get(requests_url, headers=headers)
    response = response.json()
    return response

# set quiz state
@error_handler
def set_current_status(token: str, userId:int, topicId:int, questionId:int):
    headers = create_headers(token)
    request_url = f"{BASE_URL}/current_status"
    payload = {
        "userId": userId,
        "topicId": topicId,
        "questionId": questionId
    }
    response = requests.post(request_url, headers=headers, data=json.dumps(payload))
    return response.json()

# get question/answer by id
@error_handler
def get_question_by_id(token: str, questionId):
    headers = create_headers(token)
    requests_url = f"{BASE_URL}/questions/{questionId}"
    response = requests.get(requests_url, headers=headers)
    return response.json()

# get all topics
@error_handler
def get_topics(token:str):
    headers = create_headers(token)
    requests_url = f"{BASE_URL}/topics"
    response = requests.get(requests_url, headers=headers)
    return response.json()

# Delete the MessageHistory of a user
def delete_session(user_id):
    # Verbindung herstellen
    conn = psycopg2.connect(DB)

    # Cursor erstellen
    cur = conn.cursor()

    # SQL-Abfragen vorbereiten
    delete_messages_query = "DELETE FROM message_store WHERE session_id = %s;"
    reset_bot_id_query = "UPDATE app_user SET bot_id = 0 WHERE id = %s;"
    reset_state_query = "UPDATE state SET current_state = 0 WHERE user_id = %s;"

    try:
        # SQL-Abfragen ausführen
        cur.execute(delete_messages_query, (user_id,))
        cur.execute(reset_bot_id_query, (user_id,))
        cur.execute(reset_state_query, (user_id,))

        # Änderungen in der Datenbank übernehmen
        conn.commit()

    except psycopg2.Error as e:
        # Fehlerausgabe, falls etwas schiefgeht
        logger.error(f"Ein Fehler ist aufgetreten: {e}")
        conn.rollback()

    finally:
        # Cursor und Verbindung schließen
        cur.close()
        conn.close()
        return True
