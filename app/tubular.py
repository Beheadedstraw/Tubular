#!/usr/bin/python
import urllib.request
import scrapetube
import requests
from bs4 import BeautifulSoup
import uvicorn
import re
import youtube_dl
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
import urllib.parse
from threading import Thread
import time
from static import *
from db import DB
from config import PORT, HOST, DOWNLOAD_DIR

############ Change These ####################

#change this to set the download location for videos
download_location = DOWNLOAD_DIR      

##############################################

app = FastAPI()
origins = ['*']
download_queue = []
db = DB()

global DL_PAUSED 
DL_PAUSED = "Downloading"

@app.get("/")
async def root():
    return RedirectResponse("/search")

@app.get("/pause")
async def pause():
    global DL_PAUSED 
    DL_PAUSED = "Paused"
    return RedirectResponse("/queue")

@app.get("/unpause")
async def pause():
    global DL_PAUSED 
    DL_PAUSED = "Downloading"
    return RedirectResponse("/queue")

@app.get("/download")
async def download(video: str):
    download_queue.append(video)
    db.queue_insert(video)
    return RedirectResponse("/video")

@app.get("/clear_queue")
async def clear_queue():
    db.queue_clear()
    return {"message":"Queue Cleared. Current downloading item will still continue."}

@app.get("/video")
async def download():
    page = head + video_download_bar() + footer
    return HTMLResponse(page)

@app.get("/queue")
async def queue():
    d_list = db.dl_get_queue()
    content = ""
    for d in d_list:
        content += f'<tr><td>{d[0]}</td></tr>'
    page = head + video_download_queue(DL_PAUSED) + content + footer
    return HTMLResponse(page)

@app.get("/search")
async def download(query: str =""):    
    if query != "":
        try:
            videos = get_all_video_in_search(query)
        except Exception as e:
            content = f"<p>something is borked: {e}</p>"
            page = head + video_search_bar(query) + content + footer
            return HTMLResponse(page)
        
        content = ""
        for v in videos:
            check = db.dl_check_history(v["url"])
            
            if check == True:
                disabled = "disabled"
                button = "In Library"
            else:
                disabled = ""
                button = "Download"
            content += f'<tr><td><img src="{v["thumbnail"]}"></td><td>{v["title"]}</td><td>{v["upload_date"]}</td><td><a href="{v["url"]}">{v["url"]}</a></td><td><input type="button" onclick=queueDownload("{v["url"]}",this) value="{button}" {disabled}><input type="button" onclick=queueDownload("{v["url"]}",this) value="Force Download"></td></tr>'
    else:
        content = ""
    
    page = head + video_search_bar(query) + content + footer
    return HTMLResponse(page)

@app.get("/playlist")
async def playlist(query: str =""):    
    if query != "":
        try:
            videos = get_all_video_in_playlist(query)
        except Exception as e:
            content = f"<p>something is borked: {e}</p>"
            page = head + playlist_search_bar(query) + content + footer
            return HTMLResponse(page)
        
        content = ""
        for v in videos:
            check = db.dl_check_history(v["url"])
            
            if check == True:
                disabled = "disabled"
                button = "In Library"
            else:
                disabled = ""
                button = "Download"
            content += f'<tr><td><img src="{v["thumbnail"]}"></td><td>{v["title"]}</td><td>{v["upload_date"]}</td><td><a href="{v["url"]}">{v["url"]}</a></td><td><input type="button" onclick=queueDownload("{v["url"]}",this) value="{button}" {disabled}><input type="button" onclick=queueDownload("{v["url"]}",this) value="Force Download"></td></tr>'
    else:
        content = ""
    
    page = head + playlist_search_bar(query) + content + footer
    return HTMLResponse(page)

@app.get("/channel")
async def channel(channel_id: str="", filter: str=""):
    try:
        videos = get_all_video_in_channel(channel_id)
    except Exception as e:
        content = f"<p>something is borked: {e}</p>"
        page = head + channel_search_bar(channel_id, filter) + content + footer
        return HTMLResponse(page)
        
    if channel_id != "":
        content = ""
        for v in videos:
            check = db.dl_check_history(v["url"])
            
            if check == True:
                disabled = "disabled"
                button = "In Library"
            else:
                disabled = ""
                button = "Download"
            if filter != "":
                if re.search(filter,v["title"],re.IGNORECASE):
                    content += f'<tr><td><img src="{v["thumbnail"]}"></td><td>{v["title"]}</td><td>{v["upload_date"]}</td><td><a href="{v["url"]}">{v["url"]}</a></td><td><input type="button" onclick=queueDownload("{v["url"]}",this) value="{button}" {disabled}><input type="button" onclick=queueDownload("{v["url"]}",this) value="Force Download"></td></tr>'
            else:
                content += f'<tr><td><img src="{v["thumbnail"]}"></td><td>{v["title"]}</td><td>{v["upload_date"]}</td><td><a href="{v["url"]}">{v["url"]}</a></td><td><input type="button" onclick=queueDownload("{v["url"]}",this) value="{button}" {disabled}><input type="button" onclick=queueDownload("{v["url"]}",this) value="Force Download"></td></tr>'
    else:
        content = ""
    
    page = head + channel_search_bar(channel_id, filter) + content + footer
    return HTMLResponse(page)

def get_all_video_in_channel(channel_id):
    videos = scrapetube.get_channel(channel_id, sleep=0.1, sort_by="newest")
    v_list = []
    for video in videos:
        video_url = "https://www.youtube.com/watch?v="+str(video['videoId'])
        print(video_url)
        v_list.append({"title": video['title']['runs'][0]['text'], "url": video_url, "thumbnail": urllib.parse.unquote(video['thumbnail']['thumbnails'][0]['url']), "upload_date": "TBD"})
    return v_list

def get_all_video_in_search(query):
    videos = scrapetube.get_search(query, sleep=0.1, limit=100, sort_by="upload_date")
    v_list = []
    for video in videos:
        video_url = "https://www.youtube.com/watch?v="+str(video['videoId'])
        print(video_url)
        v_list.append({"title": video['title']['runs'][0]['text'], "url": video_url, "thumbnail": urllib.parse.unquote(video['thumbnail']['thumbnails'][0]['url']), "upload_date": "TBD"})
    return v_list

def get_all_video_in_playlist(query):
    videos = scrapetube.get_playlist(query, sleep=0.1)
    v_list = []
    for video in videos:
        video_url = "https://www.youtube.com/watch?v="+str(video['videoId'])
        print(video_url)
        v_list.append({"title": video['title']['runs'][0]['text'], "url": video_url, "thumbnail": urllib.parse.unquote(video['thumbnail']['thumbnails'][0]['url']), "upload_date": "TBD"})
    return v_list
        

def get_video_title(video_url):
    r = requests.get(video_url)
    soup = BeautifulSoup(r.text)

    link = soup.find_all(name="title")[0]
    title = str(link.text)

    return title
    
def downloader_thread():
    dbt = DB()
    while True:
        try:
            global DL_PAUSED
            if DL_PAUSED != "Paused":
                video = dbt.queue_pull()
                if video:
                    ydl_opts = {
                        'outtmpl': download_location + '/%(uploader)s/%(title)s.%(ext)s',
                        'ignoreerrors': True
                        }
                    
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        try:
                            d = ydl.download([video])
                            dbt.queue_delete(video)
                            dbt.dl_complete(video)
                        except Exception as e:
                            pass
        except Exception as e:
            print(e)
        time.sleep(2)
            

downloader = Thread(target=(downloader_thread), args=())
downloader.start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_level=20)