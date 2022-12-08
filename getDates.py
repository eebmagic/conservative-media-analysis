import urllib.request as ur
from bs4 import BeautifulSoup
import re
import json
import os
from tqdm import tqdm

def getDate(vidID):
    # Build url
    url = "http://www.youtube.com/watch?v=" + vidID

    # Get html from url
    html = ur.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    # Get variable from script
    scripts = soup.findAll('script', {})
    target = 'var ytInitialData = '
    p = re.compile('var ytInitialData = .*?;')
    texts = [str(s) for s in scripts]
    match = [t for t in texts if target in t][0]
    result = p.search(match).string

    # Get date from variable
    start = result.index('"publishDate":{"simpleText":"')+29
    back = result[start:]
    final = back[:back.index('"')]

    return final
    

if __name__ == '__main__':
    # video_id = 'aEH7BueK_sU'
    # date = getDate(video_id)
    # print(video_id, date)

    files = os.listdir('channel-results')
    print(f'Building dates for files:\n\t{files}')

    for file in files:
        if file.endswith('.json'):
            channel = file.split('.')[0]
            with open(f'channel-results/{file}') as file:
                videos = json.load(file)
                ids = [v['id']['videoId'] for v in videos]
            print(f'Getting dates for channel {channel} ({len(ids)} total videos)')

            targetPath = f'video-dates/{channel}.json'
            if not os.path.exists(targetPath):
                with open(targetPath, 'w') as file:
                    file.write('{}')

            with open(targetPath, 'r') as file:
                allDates = json.load(file)

            added = 0
            for vidId in tqdm(ids):
                if vidId not in allDates:
                    added += 1
                    date = getDate(vidId)
                    allDates[vidId] = date

            if added > 0:
                with open(targetPath, 'w') as file:
                    json.dump(allDates, file)
                    print(f'Wrote {added} new items to file')

