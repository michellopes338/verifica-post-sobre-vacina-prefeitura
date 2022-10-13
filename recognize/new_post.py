from email import message
import json
from socket import timeout
import requests
import nltk
import re
from plyer import notification


def check_if_is_vaccine_post(post):
    subtitles = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
    only_letters = re.sub('[^a-zA-Z]', ' ', subtitles)
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    wordstoken = nltk.tokenize.word_tokenize(only_letters, language='portuguese')
    filtered_words = []
    keywords = ['vacin']

    for word in wordstoken:
        if word not in stopwords:
            filtered_words.append(ps.stem(word))
    
    for keyword in keywords:
        if keyword in filtered_words:
            return True
    
    return False

ps = nltk.stem.RSLPStemmer()
DATA = requests.get('https://www.instagram.com/prefeituradeparauapebas/?__a=1').json()
POST = DATA['graphql']['user']['edge_owner_to_timeline_media']['edges']
search_scope = len(POST)

with open('post.json', 'r') as file:
    content = file.read()
    if content == '':
        last_post = ['']
    else:
        last_post = json.loads(content)

for post_index in range(search_scope + 1):
    is_vaccine_post = check_if_is_vaccine_post(POST[post_index])

    if is_vaccine_post == True:
        current_post = POST[post_index]
        break

if last_post != current_post:
    notification.notify(
        title = 'Novo post sobre vacina',
        message = f'{current_post["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]} https://www.instagram.com/p/{current_post["node"]["shortcode"]}/',
        timeout = 60
    )
    with open('post.json', 'w') as file:
        file.write(json.dumps(current_post))
    
