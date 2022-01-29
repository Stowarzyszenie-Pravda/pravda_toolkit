from wordcloud import WordCloud
from PIL import Image

import numpy as np

def wordcloud(text, mask_path = None, width = 1500, height = 1000):
    ''' 
    Takes Series text object and generates wordcloud (optionally with mask) to output folder.
    '''
    
    # If mask path not given then don't use one
    if mask_path is not None:
        mask = np.array(Image.open(mask_path))
        wordcloud = WordCloud(width = width, height = height, random_state=1, background_color='white', colormap='winter',
        collocations=False, mask=mask).generate(text.to_string())
    else:
        wordcloud = WordCloud(width = width, height = height, random_state=1, background_color='white', colormap='winter',
        collocations=False).generate(text.to_string())
    return wordcloud