import os
import pickle
from flask import Flask, jsonify, render_template
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# --- CONFIGURAÇÃO ---
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = 'client_secrets.json'

# --- NOVAS VARIÁVEIS GLOBAIS PARA GERENCIAR A FILA E HISTÓRICO ---
app = Flask(__name__, template_folder='.')
processed_subscribers = []  # Lista com todos os inscritos já processados, em ordem cronológica
current_display_index = -1  # O índice do inscrito que está sendo exibido atualmente
channel_stats = {"subscriberCount": "0"}

# --- FUNÇÕES DA API DO YOUTUBE (sem grandes mudanças) ---
def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def initialize_data():
    """Busca os dados iniciais e prepara o histórico."""
    global processed_subscribers, current_display_index, channel_stats
    youtube = get_authenticated_service()

    # Busca estatísticas do canal
    channel_request = youtube.channels().list(part='statistics', mine=True).execute()
    channel_stats = channel_request['items'][0]['statistics']

    # Busca inscritos recentes
    subs_response = youtube.subscriptions().list(part='snippet,subscriberSnippet', myRecentSubscribers=True, maxResults=50).execute()
    
    # Inverte a lista para que fique em ordem cronológica (do mais antigo para o mais novo)
    initial_list = list(reversed(subs_response.get('items', [])))
    processed_subscribers = initial_list
    
    # Começa apontando para o inscrito mais recente da lista inicial
    if processed_subscribers:
        current_display_index = len(processed_subscribers) - 1
    
    print(f"Inicialização completa. {len(processed_subscribers)} inscritos carregados no histórico.")

# --- ROTAS DO SERVIDOR (LÓGICA COMPLETAMENTE REFEITA) ---
@app.route('/')
def index():
    return render_template('controller.html')

@app.route('/display')
def display_page():
    return render_template('display.html')

@app.route('/next_subscriber')
def next_subscriber():
    """Avança para o próximo inscrito, buscando novos se necessário."""
    global current_display_index, processed_subscribers

    # Se já estamos no final da lista, precisamos checar por novos inscritos
    if current_display_index == len(processed_subscribers) - 1:
        print("Verificando se há novos inscritos...")
        youtube = get_authenticated_service()
        subs_response = youtube.subscriptions().list(part='snippet,subscriberSnippet', myRecentSubscribers=True, maxResults=50).execute()
        latest_from_api = list(reversed(subs_response.get('items', [])))

        last_known_id = processed_subscribers[-1]['subscriberSnippet']['channelId'] if processed_subscribers else None

        # Encontra o índice do último inscrito que já conhecemos
        last_known_index_in_new_list = -1
        for i, sub in enumerate(latest_from_api):
            if sub['subscriberSnippet']['channelId'] == last_known_id:
                last_known_index_in_new_list = i
                break

        # Se encontramos o último conhecido, adicionamos todos que vieram depois dele
        if last_known_index_in_new_list != -1:
            new_subs = latest_from_api[last_known_index_in_new_list + 1:]
            if new_subs:
                print(f"Encontrados {len(new_subs)} novos inscritos!")
                processed_subscribers.extend(new_subs)
            else:
                print("Nenhum inscrito novo.")

    # Avança o índice, sem deixar passar do final da lista
    if current_display_index < len(processed_subscribers) - 1:
        current_display_index += 1
    
    # Baixa a foto do inscrito atual (se houver um)
    download_current_subscriber_picture()
    return get_current_data()

@app.route('/previous_subscriber')
def previous_subscriber():
    """Volta para o inscrito anterior no histórico."""
    global current_display_index
    # Volta o índice, sem deixar ser menor que 0
    if current_display_index > 0:
        current_display_index -= 1
    
    download_current_subscriber_picture()
    return get_current_data()

@app.route('/current_data')
def get_current_data():
    """Retorna os dados do inscrito atualmente em exibição."""
    global channel_stats # Precisamos buscar as estatísticas mais recentes também
    youtube = get_authenticated_service()
    channel_request = youtube.channels().list(part='statistics', mine=True).execute()
    channel_stats = channel_request['items'][0]['statistics']
    
    if current_display_index == -1 or not processed_subscribers:
        return jsonify({
            "subscriberCount": channel_stats.get('subscriberCount', '0'),
            "currentSubscriberName": "Pronto para começar!",
            "currentSubscriberPicture": ""
        })

    subscriber_info = processed_subscribers[current_display_index]['subscriberSnippet']
    return jsonify({
        "subscriberCount": channel_stats.get('subscriberCount', '0'),
        "currentSubscriberName": subscriber_info['title'],
        "currentSubscriberPicture": subscriber_info['thumbnails']['high']['url']
    })

def download_current_subscriber_picture():
    """Função auxiliar para baixar a foto do inscrito no índice atual."""
    if current_display_index != -1 and processed_subscribers:
        try:
            subscriber_info = processed_subscribers[current_display_index]['subscriberSnippet']
            subscriber_name = subscriber_info['title']
            image_url = subscriber_info['thumbnails']['high']['url']
            
            response = requests.get(image_url)
            if response.status_code == 200:
                if not os.path.exists('fotos_inscritos'): os.makedirs('fotos_inscritos')
                
                file_path = os.path.join('fotos_inscritos', "ultimoinscrito.png")
                with open(file_path, 'wb') as f: f.write(response.content)
                print(f"Exibindo e baixando foto de: '{subscriber_name}'")
        except Exception as e:
            print(f"Erro ao baixar a foto: {e}")

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    initialize_data()
    print("Servidor pronto! Acesse http://127.0.0.1:5000 no seu navegador para o controle.")
    app.run(port=5000)