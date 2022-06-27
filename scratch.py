import requests
from bs4 import BeautifulSoup
YOUTUBE_TRENDING_URL='https://www.youtube.com/feed/trending'

# Doesnot execute javascript
response=requests.get(YOUTUBE_TRENDING_URL)
print(response.status_code)
with open('trending.html','w') as f:
  f.write(response.text)
doc=BeautifulSoup(response.text,'html.parser')
print(doc.title.text)
# find all the video divs
div_class='style-scope ytd-video-renderer'
video_divs=doc.find_all('div',{'class':div_class})
print(len(video_divs))