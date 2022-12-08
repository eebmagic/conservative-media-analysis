import urllib
import json
import urllib.request as ur

with open('yt-key.txt') as file:
    key = file.read().strip()


GLOBAL_USAGE = 0
# THRESH = 3
THRESH = 720

def getUrlResponse(url):
    '''
    "Speed limited" wrapper for API calls
    '''
    global GLOBAL_USAGE, THRESH
    assert GLOBAL_USAGE < THRESH, f"Cannot get data at URL, because have run func {GLOBAL_USAGE} times"

    try:
        result = json.load(ur.urlopen(url))
    # except urllib.error.HTTPError as err:
    except:
        print(f'Got errror for url:\n\t{url}')
        # raise err
        return {}
    GLOBAL_USAGE += 1

    print(f'Got {len(result["items"])} items {GLOBAL_USAGE}/{THRESH}')

    return result


def getAllVids(channelId):
    '''
    For a given channel, get all videos listed.
    '''
    url = f"https://www.googleapis.com/youtube/v3/search?key={key}&channelId={channelId}&maxResults=50"
    try:
        jres = getUrlResponse(url)
        nextToken = jres['nextPageToken']
        print(json.dumps(jres, indent=2))
        # print(nextToken)
    except:
        return []

    allItems = []
    for item in jres['items']:
        val = item['id']
        if val['kind'] == 'youtube#video':
            allItems.append(item)

    while 'nextPageToken' in jres:
        url = f"https://www.googleapis.com/youtube/v3/search?key={key}&channelId={channelId}&pageToken={nextToken}&maxResults=50"
        # jres = json.load(ur.urlopen(url))
        try:
            jres = getUrlResponse(url)
        except:
            print(f'breaking for assertion on counter of {THRESH}')
            return allItems

        items = jres['items']
        for item in items:
            val = item['id']
            if val['kind'] == 'youtube#video':
                allItems.append(item)

        if 'nextPageToken' in jres:
            nextToken = jres['nextPageToken']
        else:
            break

        print(f'Currently have {len(allItems)} items')

    return allItems


if __name__ == '__main__':

    # Daily Wire (52 videos)
    author = 'UCroKPvbmaQKGK5tjtQsvaDw'

    # Ben Shapiro (3547 videos)
    # author = 'UCnQC_G5Xsjhp9fEJKuIcrSw'

    vids = getAllVids(author)
    print(vids)
    print(len(vids))


    with open(f'channel-results/{author}.json', 'w') as file:
        json.dump(vids, file)
        print(f'WROTE TO FILE')
