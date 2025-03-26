from flask import Flask, Response, render_template
import requests
from urllib.parse import urljoin
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Simpan URL .m3u8 di backend
IPTV_URLS = {
    "cnbc": "https://live.cnbcindonesia.com/livecnbc/smil:cnbctv.smil/master.m3u8",
    "moji": "http://op-group1-swiftservehd-1.dens.tv/h/h207/02.m3u8",
    "trans7": "https://video.detik.com/trans7/smil:trans7.smil/index.m3u8",
    "transTV": "https://video.detik.com/transtv/smil:transtv.smil/index.m3u8",
    "indosiar": "http://op-group1-swiftservehd-1.dens.tv/h/h235/02.m3u8",
    "sportstars": "https://cempedak-live-cdn.mncnow.id/live/eds/SPOTV2-HD/sa_dash_vmx/SPOTV2-HD.mpd",
}


@app.route("/")
def index():
    # template_folder = os.path.join(os.path.dirname(os.getcwd()), "templates")
    return render_template("index.html")


# Proxy untuk file .m3u8
@app.route("/proxy/<key>/master.m3u8")
def proxy_m3u8(key):
    # Ambil URL .m3u8 berdasarkan key
    m3u8_url = IPTV_URLS.get(key)
    if not m3u8_url:
        return f"Key '{key}' not found in IPTV_URLS", 404

    try:
        # Ambil konten dari URL .m3u8
        response = requests.get(m3u8_url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}", 500

    # Kembalikan konten ke frontend dengan header CORS
    flask_response = Response(
        response.content, content_type=response.headers["Content-Type"]
    )
    flask_response.headers.add("Access-Control-Allow-Origin", "*")
    return flask_response


# Proxy untuk file segment .m3u8 dan .ts
@app.route("/proxy/<key>/<path:subpath>")
def proxy_segment(key, subpath):
    # Ambil URL .m3u8 berdasarkan key
    m3u8_url = IPTV_URLS.get(key)
    if not m3u8_url:
        return f"Key '{key}' not found in IPTV_URLS", 404

    # Bangun base_url dari URL .m3u8 utama
    base_url = m3u8_url.rsplit("/", 1)[0] + "/"

    # Bangun URL asli dari base_url dan subpath
    original_url = urljoin(base_url, subpath)

    try:
        # Ambil konten dari URL asli
        response = requests.get(original_url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching the segment: {e}", 500

    # Tentukan content type berdasarkan ekstensi file
    if subpath.endswith(".m3u8"):
        content_type = "application/vnd.apple.mpegurl"
    elif subpath.endswith(".ts"):
        content_type = "video/MP2T"
    else:
        content_type = response.headers.get("Content-Type", "application/octet-stream")

    # Kembalikan konten ke frontend dengan header CORS
    flask_response = Response(response.content, content_type=content_type)
    flask_response.headers.add("Access-Control-Allow-Origin", "*")
    return flask_response


# Proxy untuk file segment .m3u8 dan .ts
@app.route("/proxy/mpd/<key>/master.mpd")
def proxy_mpd(key):
    # Ambil URL .m3u8 berdasarkan key
    mpd_url = IPTV_URLS.get(key)

    if not mpd_url:
        return f"Key '{key}' not found in IPTV_URLS", 404

    try:
        # Ambil konten dari URL .m3u8
        response = requests.get(dash, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}", 500

    # Kembalikan konten ke frontend dengan header CORS
    flask_response = Response(
        response.content, content_type=response.headers["Content-Type"]
    )
    flask_response.headers.add("Access-Control-Allow-Origin", "*")
    return flask_response


# Proxy untuk file segment .m3u8 dan .ts
@app.route("/proxy/mpd/<key>/<path:subpath>")
def proxy_segment_mpd(key, subpath):
    # Ambil URL .m3u8 berdasarkan key
    mpd_url = IPTV_URLS.get(key)

    if not mpd_url:
        return f"Key '{key}' not found in IPTV_URLS", 404

    # Bangun base_url dari URL .m3u8 utama
    base_url = dash.rsplit("/", 1)[0] + "/"

    # Bangun URL asli dari base_url dan subpath
    original_url = urljoin(base_url, subpath)

    try:
        # Ambil konten dari URL asli
        response = requests.get(original_url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching the segment: {e}", 500

    # Tentukan content type berdasarkan ekstensi file
    if subpath.endswith(".m3u8"):
        content_type = "application/vnd.apple.mpegurl"
    elif subpath.endswith(".ts"):
        content_type = "video/MP2T"
    else:
        content_type = response.headers.get("Content-Type", "application/octet-stream")

    # Kembalikan konten ke frontend dengan header CORS
    flask_response = Response(response.content, content_type=content_type)
    flask_response.headers.add("Access-Control-Allow-Origin", "*")
    return flask_response
