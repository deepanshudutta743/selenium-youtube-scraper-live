import smtplib
import os
import json
#import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D'


def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver
  
def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  driver.get(YOUTUBE_TRENDING_URL)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos
def parse_video(video):
  title_tag=video.find_element(By.ID,'video-title')
  title=title_tag.text
  url=title_tag.get_attribute('href')

  thumbnail_tag=video.find_element(By.TAG_NAME,'img')
  thumbnail_url=thumbnail_tag.get_attribute('src')

  channel_div=video.find_element(By.CLASS_NAME,'ytd-channel-name')
  channel_name=channel_div.text
  views=video.find_element(By.CLASS_NAME,'ytd-video-meta-block').text
  
  description=video.find_element(By.ID,'description-text').text
  return{
    'title':title,
    'url':url,
    'thumbnail_url':thumbnail_url,
    'channel_name':channel_name,
    'views_days':views,
    'description':description
  }
def send_email(body):

  try:
    server_ssl = smtplib.SMTP('smtp.gmail.com', 587)
    server_ssl.starttls()
    SENDER_EMAIL='dichuda998800@gmail.com'
    RECEIVER_EMAIL='dichuda998800@gmail.com'
    my_secret = os.environ['app_password']
    subject = 'Youtube trending videos'
    
    my_secret = os.environ['python']
    
    email_text = f"""
    From: {SENDER_EMAIL}
    To: {RECEIVER_EMAIL}
    Subject: {subject}
    
    {body}
    """
    
    server_ssl.login(SENDER_EMAIL, my_secret)
    server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_text)
    
    
  except:
    print('Something went wrong...')
    
if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()

  print('Fetching trending videos')
  videos = get_videos(driver)
  print(f'Found {len(videos)} videos')
    
  print('Get the video divs')
  print('page title',driver.title)

  print('parsing top 10 videos')
  # title,thumnnail_url,channel,views,uploaded,description
  video_data=[parse_video(video) for video in videos[:10]]
  #print(video_data)
  print("save the data to csv")
  video_df=pd.DataFrame(video_data)
  video_df.to_csv('trending_video.csv',index=None)
  print(video_df)

  print('Send a Email with the results')
  body=json.dumps(video_data,indent=2)
  send_email(body)
   
  
  
  

  
  # print('All video divs count',len(video_divs.text))