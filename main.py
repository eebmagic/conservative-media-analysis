from getUrls import getAllVids
from dataProcessing import mergeVideos

# # Daily Wire (52 videos)
# author = 'UCroKPvbmaQKGK5tjtQsvaDw'

# # Ben Shapiro (3547 videos)
# author = 'UCnQC_G5Xsjhp9fEJKuIcrSw'

# Daily Wire Plus (807 videos)
# author = 'UCaeO5vkdj5xOQHp4UmIN6dw'

# Matt Walsh (2504 videos)
author = 'UCO01ytfzgXYy4glnPJm4PPQ'

# # Michael Knowls (3406 videos)
# author = 'UCr4kgAUTFkGIwlWSodg43QA'

# # Candace Owens (129 videos)
# author = 'UCkY4fdKOFk3Kiq7g5LLKYLw'

newvids = getAllVids(author)
print(f'Got a total of {len(newvids)} videos')

mergeVideos(author, newvids)
print(f'FINISHED DOWNLOADING & MERGING VIDEOS FOR CHANNEL {author}')
