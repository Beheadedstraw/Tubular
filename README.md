#### Main Branch: ![main](https://github.com/Beheadedstraw/Tubular/actions/workflows/docker-publish.yml/badge.svg?branch=main) Dev Branch:![image](https://github.com/Beheadedstraw/Tubular/actions/workflows/docker-publish.yml/badge.svg?branch=dev)
# Tubular - A YouTube Video uh... *"Collecting"* Suite
![image](https://github.com/Beheadedstraw/Tubular/assets/5951719/bdf8e9be-38b6-4679-9da1-214f25099fd8)

## What This Does
This helps with collecting YouTube videos for offline viewing in an easy'ish to use and not so fancy web UI.

Ways of collecting are:
- Searching manually within Tubular.
- Searching by Channel
- Searching from a Playlist
- Bulk collecting via playlist.
- Tracks Downloaded Items via sqlite DB. 

## How This Does It
Currently thanks to scrapetube and youtube_dl libraries with my own added special sauce. This serves everything through a lightweight FastAPI instance and keeps track of collecting by storing the queue and completed downloads in an sqlite database.

## How To Run It
### No Container
1. clone this repo
2. `pip install -r requirements.txt`
3. Change the variable `download_location` in the tubular.py to the location you want to collect your files.
4. Run `python tubular.py`
5. Navigate to `http://{your ip}:8000`

## Docker
> :warning: Change the source mount to wherever you want to store your files.

`sudo docker run -p 8000:8000 --mount type=bind,source="/Videos",target=/videos ghcr.io/beheadedstraw/tubular:main`


### Docker Compose
```yaml
version: '3'
services:
  app:
    image: ghcr.io/beheadedstraw/tubular:dev
    container_name: tubular
    restart: always
    ports:
      - 8000:8000
    environment:
      - HOST=0.0.0.0         # internal ip, leave as is.
      - PORT=8000            # internal port
      - CONFIG_DIR=/data     # internal config path
      - DOWNLOAD_DIR=/videos # internal download path
    volumes:
      - /tublular/config:/data   #data folder for app src
      - /tublular/videos:/videos #folder to store videos ***CHANGE THIS TO WHERE YOU WANT TO STORE VIDS***
```

## FAQ
### What version of python does this run on?
- Python 3.x (tested on Python 3.8)

### How do I change the destination directory?
- you can change the `download_location` variable in the main.py

### Do You Have Any Docker Images?
- You can find them under the packages section to the right or read above.

### Why Not Make Something Like *arr programs?
- Because I hate C#.

### Will this ever get as feature rich as the *arr programs?
- Probably not. This was made in a couple of nights on a few beers and a prayer. If someone wants to help with PR's, it's more than welcome.

### Why does your Python code look like sh*t?
- Read above. 
