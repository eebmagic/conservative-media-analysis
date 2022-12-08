from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import TranscriptsDisabled
from youtube_transcript_api._errors import NoTranscriptFound
import os
import json
from tqdm import tqdm

def getText(video_id):
    try:
        result = YouTubeTranscriptApi.get_transcript(video_id)
    except TranscriptsDisabled:
        print(f'Transcript disbabled for {video_id}')
        return None
    except NoTranscriptFound:
        print(f'No transcript found for {video_id}')
        return None

    # except Exception as e:
        # print(f'Got error for video {video_id}:\n\t{e}')
        # print(f'Got exception: {e}')
        # print(f'Exception type: {type(e)}')
        # raise e
    texts = ' '.join([r['text'] for r in result])

    return texts

if __name__ == '__main__':
    # video_id = 'aEH7BueK_sU'
    # video_id = 's3MRx4-k2O8'

    # getText(video_id)

    files = os.listdir('channel-results')
    print(f'Building captions for files:\n\t{files}')

    for file in files:
        if file.endswith('.json'):
            channel = file.split('.')[0]
            with open(f'channel-results/{file}') as file:
                videos = json.load(file)
                ids = [v['id']['videoId'] for v in videos]
            
            print(f'Getting captions for channel {channel} ({len(ids)} total videos)')

            targetPath = f'video-captions/{channel}.json'
            if not os.path.exists(targetPath):
                with open(targetPath, 'w') as file:
                    file.write('{}')

            with open(targetPath, 'r') as file:
                allCaptions = json.load(file)

            added = 0
            for vidId in tqdm(ids):
                if vidId not in allCaptions:
                    added += 1
                    text = getText(vidId)
                    if text:
                        allCaptions[vidId] = text

            if added > 0:
                with open(targetPath, 'w') as file:
                    json.dump(allCaptions, file)
                    print(f'Wrote {added} new items to file')

