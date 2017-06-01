import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine
import apiai
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

API_TOKEN = '249725860:AAERnYX5uniAFdV9cd7yKd4Y_tfJ5tqSX8g'
WEBHOOK_URL = 'https://ikmchatbot.com:8443/telegram_try/'
context = ('ssl/fullchain.crt', 'ssl/private.key')

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
##client = apiai.ApiAI("b7de777391ec48329e192fe579d23e1")
machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2',
        'state3',
        'state4',
        'state5',
        'state6',
        'state7',
        'state8',
        'state9',
        'state10'

    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state3',
            'conditions': 'is_going_to_state3'
        },
        {
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state4',
            'conditions': 'is_going_to_state4'
        },
        {
            'trigger': 'advance',
            'source': 'state4',
            'dest': 'state5',
            'conditions': 'is_going_to_state5'
        },
        {
            'trigger': 'advance',
            'source': 'state5',
            'dest': 'state6',
            'conditions': 'is_going_to_state6'
        },
        {
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'state7',
            'conditions': 'is_going_to_state7'
        },
        {
            'trigger': 'advance',
            'source': 'state7',
            'dest': 'state8',
            'conditions': 'is_going_to_state8'
        },
         {
            'trigger': 'advance',
            'source': 'state3',
            'dest': 'state9',
            'conditions': 'is_going_to_state9'
        },
         {
            'trigger': 'advance',
            'source': 'state9',
            'dest': 'state10',
            'conditions': 'is_going_to_state10'
        },
        {
            'trigger': 'go_back',
            'source': [
                'state6',
                'state8',
                'state10'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)
def intent_parser(input):
    # Initialize API.AI client
    # global client
    client = apiai.ApiAI("b7de777391ec48329e192fe579d23e1c")

    # Create new request

    request = client.text_request()
    request.query = input

    # Receive response and convert it to JSON

    response = request.getresponse()
    t1= response.read()
    t2 = json.loads(t1)
    return (t2["result"]["metadata"]["intentName"],t2["result"]["fulfillment"]["speech"])

def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
#update = telegram.Update.de_json(request.get_json(force=True), bot)
@app.route('/telegram_try/', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
   
    if update.message.text == "/start":
        update.message.reply_text("Find album?\nNeed recommendation?\nFind artist's top track?\nEnd the task by enter '/end' ")
    
    elif update.message.text == "/end":
        machine.go_back(update)
    
    elif update.message.text == "/check_state":
        update.message.reply_text(machine.state)      
   
    else:
        
        save_text=update.message.text
        current_intent,try_output=intent_parser(update.message.text)
        update.message.text=current_intent
        #print (current_intent)
        machine.advance(update)
        action(try_output,current_intent,update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

def action(save_text,api_return,update):
    if api_return=="find_album_by_enter_singer" and machine.state=="state9":
        artist = get_artist(save_text)
        show_top_track(artist,update)
        
    elif api_return=="find_album_by_enter_singer":
        artist = get_artist(save_text)
        show_artist_albums(artist,update)
    
    elif api_return=="list_song_by_album_name":
        show_album_tracks(save_text,update)
    
    elif api_return=="recommend_by_singer":
        artist = get_artist(save_text)
        show_recommendations_for_artist(artist,update)

    
# get the json file from spotify database
def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None
#decode the json file get the artist id and find artist's album
def show_artist_albums(artist,update):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set() # to avoid dups
    final = " "
    albums.sort(key=lambda album:album['name'].lower())
    for album in albums:
        name = album['name']
        final = final + "\n"+ name
        if name not in seen:
            seen.add(name)

    update.message.reply_text(final)

def show_recommendations_for_artist(artist,update):
    albums = []
    results = sp.recommendations(seed_artists = [artist['id']])
    final=" "
    for track in results['tracks']:
        final= final + "\n" + track['name'] + ' - ' + track['artists'][0]['name']  
        #print track['name'], '-', track['artists'][0]['name']    
    #update.message.reply_text("check recommend")
    update.message.reply_text(final)
    update.message.reply_text("Do you want to play the list ?")

                

#show all the tracks by album name
def show_album_tracks(album,update):
    results = sp.search(q = "album:" + album, type = "album")
    final = " "
    # get the first album uri
    album_id = results['albums']['items'][0]['uri']

    # get album tracks
    tracks = sp.album_tracks(album_id)
    for track in tracks['items']:
        #print(track['name'])
        final = final + "\n"+ track['name']

    update.message.reply_text(final)
    update.message.reply_text("Do you want to play the album ?")

def show_top_track(artist,update):
    response = sp.artist_top_tracks(artist['id'])
    final = " "
    for track in response['tracks']:
        #print(track['name'])
        final = final + "\n"+ track['name']

    update.message.reply_text(final)
    update.message.reply_text("Do you want to play these tracks ?")

if __name__ == "__main__":
    client_credentials_manager = SpotifyClientCredentials("8c43edb614f441928b56383ac1b5fc88","4fe1a416dc0545879558cc1e8aa010bc")
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=False
    _set_webhook()
    app.run(host='0.0.0.0', port=8443, debug=False, ssl_context=context)


