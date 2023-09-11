head = """
<html>
<head>
<style>
    body {
        background-color: darkgrey;
    }
    .header {
        display: in-line;
    }
    
    td {
        border-top: solid grey 1px;
        border-left: solid grey 1px;
        text-align: center;
    }
</style>
<body>
<div class="header">
    <div><a href="/search">Normal Search</a> || <a href="/playlist">Playlist Search</a> || <a href="/channel">Channel Search</a> || <a href="/video">Video/Playlist Bulk Download</a> || <a href="/queue">Download Queue</a></div>
</div>
"""
footer = """
</table>
<script>
const queueDownload = async (download, ele) => {
        const response = await fetch('http://127.0.0.1:8000/download?video=' + download,
            {headers: {
            'Access-Control-Allow-Origin':'*',
            }});
        const myJson = await response.json(); //extract JSON from the http response
        ele.setAttribute("disabled", true);
        await console.log(myJson)
    }
</script>
</body>
</html>
"""
def channel_search_bar(channel_id, filter):
    return f"""
    <form method="GET" action="/channel">
    <h3>Type a youtube channel_id (named id's DO NOT WORK, view the page source on the channel page and search for 'channel_id' if it's not in the url. It'll look something like "UCijULR2sXLutCRBtW3_WEfA"</h3>
    <label>If the channel has a shitload of videos, this <b>WILL</b> take a long ass time, be patient.</label><br>
    
    <input name="channel_id" type="text" size="100" value="{channel_id}"/>
    <br>
    <label>Filter text:</label><br>
    <input name="filter" size=100 value="{filter}"/>
    <br>
    <input type="submit">
    </form>
    <table>
    """
    
def video_download_bar():
    return f"""
    <form method="GET" action="/download">
    <h3>You can use this to download single videos as well as entire playlists. Playlists will be added as a single file to the queue but will still download all files contained within it.</h3>
    <h4><b><i>BE WARNED THAT THE ONLY WAY TO STOP DOWNLOADING LARGE PLAYLISTS IS TO STOP THE SERVER, WORKING ON A WAY AROUND THAT IN A FUTURE RELEASE.</i></b></h4>
    <br>
    <label>If the playlist has a shitload of videos, this <b>WILL</b> take a long ass time, be patient.</label>
    <br>
    <input name="video" type="text" size="100"/>
    <br>
    <input type="submit">
    </form>
    """
    
def video_download_queue(paused):
    return f"""
    <h2>Download Queue - {paused}</h2>
    <a href="/pause">Pause</a>||<a href="/unpause">Unpause</a>
    <table>
    """
    
def video_search_bar(query):
    return f"""
    <form method="GET" action="./search">
    <h3>This is a standard Youtube search that will return the first 100 videos of your query. If you can't find the video you want, try being a little more descriptive.</h3>
    <br>
    <input name="query" type="text" size="100" value="{query}"/>
    <br>
    <input type="submit">
    </form>
    <table>
    """
    
def playlist_search_bar(query):
    return f"""
    <form method="GET" action="./playlist">
    <h3>This shows all videos in a playlist that you can download. Keep in mind this <b>will</b> take a long time if the playlist is huge.</h3>
    <br>
    <input name="query" type="text" size="100" value="{query}"/>
    <br>
    <input type="submit">
    </form>
    <table>
    """