import json
import os
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

STOPS = set(stopwords.words('english'))
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

def cleanTexts(texts):
    def cleanText(text):
        words = text.strip().split(' ')
        return [lemmatizer.lemmatize(w.lower()).lower() for w in words if (w not in STOPS and '[' not in w)]

    return [cleanText(text) for text in texts]

def getTextsInDateRange(channels, start, stop, cleaned=True):
    texts = []
    for channel in channels:
        # Load videos
        with open(f'channel-results/{channel}.json') as file:
            videos = json.load(file)

        # Load video captions
        with open(f'video-captions/{channel}.json') as file:
            captions = json.load(file)
        
        # Load video dates
        with open(f'video-dates/{channel}.json') as file:
            dates = json.load(file)


        # Check valid videos and add captions to texts
        for vid in videos:
            vidId = vid['id']['videoId']
            if vidId in captions and vidId in dates:
                date = dates[vidId]
                year = int(date.split(' ')[-1])
                if year >= start and year <= stop:
                    texts.append(captions[vidId])

    if cleaned:
        return cleanTexts(texts)
    else:
        return texts

def getPairs(texts, window=2):
    '''
    texts: list of list of strings.
        Each list should be a viddeo caption, each string should be a word in a caption.
    window: the distance distance between words to consider a pair (min is 2).
    '''
    pairs = []
    for words in tqdm(texts):
        for i in range(len(words)):
            for j in range(1, window+1):
                if i+j < len(words):
                    pairs.append((words[i], words[i+j]))
                if i-j >= 0:
                    pairs.append((words[i], words[i-j]))
    return pairs

def getFullWordset(texts):
    words = set()
    # files = os.listdir('video-captions')
    # for file in files:
    #     if file.endswith('.json'):
    #         with open(f'video-captions/{file}') as file:
    #             data = json.load(file)
    #             for vidId in data:
    #                 words.update(data[vidId].split(' '))
    for text in texts:
        words.update(text)
            
    return words

def buildTokenizer(wordset):
    word2idx = {w: i for i, w in enumerate(wordset)}
    idx2word = {i: w for i, w in enumerate(wordset)}
    return word2idx, idx2word

def mergeVideos(channelId, newVideos):
    filepath = f'channel-results/{channelId}.json'
    # check that filepath exists
    if os.path.exists(filepath):
        with open(f'channel-results/{channelId}.json') as file:
            videos = json.load(file)
            oldIds = set([v['id']['videoId'] for v in videos])
    else:
        videos = []
        oldIds = []

    added = 0
    for vid in newVideos:
        if vid['id']['videoId'] not in oldIds:
            videos.append(vid)
            added += 1
    
    if added > 0:
        print(f'Found {added} new videos for channel {channelId}')
        with open(f'channel-results/{channelId}.json', 'w') as file:
            json.dump(videos, file)
    else:
        print(f'NO UPDATES MADE. No new videos for channel {channelId}')
        


if __name__ == '__main__':
    channel = 'UCnQC_G5Xsjhp9fEJKuIcrSw'
    start = 2010
    stop = 2023

    texts = getTextsInDateRange(channel, start, stop)
    print(texts)
    print([len(t.split(' ')) for t in texts])
    print(len(texts))
