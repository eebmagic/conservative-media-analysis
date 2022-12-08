# Conservative Media Analysis

## Data Collection Methodology
1. List all desired channels to collect from.
2. Get all video ids for each channel (this can be 50-4,000 videos)
    - Dump video ids to a file with channel id as name.
    - Also collect published dates.
3. Download captions for all video ids in each file. (Also track date for videos)
    - *NOTE:* This might be the point where a local database could make sense. Depending on how much text this comes out to.
        - Most texts might be small as a result of YouTube shorts.


## Data Processing
- Maybe split videos by year and build word-embeddings for each year.
    - Then could compare words near specific tops over time.
