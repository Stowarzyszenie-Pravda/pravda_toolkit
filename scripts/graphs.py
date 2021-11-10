import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 

from wordcloud import WordCloud
from PIL import Image

def wordcloud(text, output_path = "/", mask_path = None, width = 1500, height = 1000):
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

    wordcloud.to_file("wordcloud.png")

if __name__ == '__main__':
    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sed nisi erat. Maecenas iaculis consequat nisi, vel rhoncus ex dictum at. Phasellus facilisis imperdiet congue. In eu pulvinar diam, eu molestie magna. Proin erat tortor, ultrices at elit et, elementum tempus neque."
    
    # Creates dataframe based on lorem ipsum
    lorem_ipsum_dataframe = pd.DataFrame(lorem_ipsum.split(' '), columns = ['text'])

    # Generates wordcloud for lorem_ipsum_dataframe
    wordcloud(lorem_ipsum_dataframe['text'])

