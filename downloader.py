import streamlit as st
import yt_dlp
import os
import tempfile
import shutil
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="NEON-TUBE // Medya Konsolu",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- STUDIO CONSOLE DESIGN SYSTEM ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg: #16140f;
        --panel: #1d1a13;
        --panel-2: #221f17;
        --border: #3a362c;
        --border-soft: #2b2820;
        --text: #f2ede1;
        --text-muted: #9c9686;
        --text-dim: #6b665a;
        --amber: #e8a33d;
        --amber-dim: #6b5228;
        --sage: #7a9a7e;
        --sage-dim: #38452f;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: var(--bg);
        color: var(--text);
    }

    /* ---- Top brand header ---- */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 20px;
        border-bottom: 1px solid var(--border-soft);
        margin-bottom: 28px;
    }
    .brand-row { display: flex; align-items: center; gap: 12px; }
    .brand-mark {
        width: 36px; height: 36px;
        background: var(--panel-2);
        border: 1px solid var(--border);
        border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px;
    }
    .brand-name {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 17px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--text);
    }
    .brand-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10.5px;
        color: var(--text-dim);
        letter-spacing: 1.5px;
        margin-left: 48px;
        margin-top: 2px;
        text-transform: uppercase;
    }
    .status-chip-ok, .status-chip-warn {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        padding: 6px 12px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        gap: 7px;
        white-space: nowrap;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .status-chip-ok {
        color: var(--sage);
        border: 1px solid var(--sage-dim);
        background: rgba(122,154,126,0.06);
    }
    .status-chip-warn {
        color: var(--amber);
        border: 1px solid var(--amber-dim);
        background: rgba(232,163,61,0.06);
    }
    .dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; display: inline-block; }

    /* ---- Panels (containers) ---- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--panel) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 22px !important;
        box-shadow: none !important;
        margin-bottom: 20px !important;
    }
    div[data-testid="column"] div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 20px !important;
        border-radius: 10px !important;
        background: var(--panel) !important;
    }

    /* ---- Section labels ---- */
    .panel-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-dim);
        margin-bottom: 14px;
    }
    .channel-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: var(--text-dim);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        display: block;
        margin-bottom: 6px;
    }
    .channel-title {
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 4px;
        color: var(--text);
    }
    .channel-desc {
        font-size: 12.5px;
        color: var(--text-muted);
        margin-bottom: 4px;
    }
    .channel-video .channel-num, .channel-video .channel-title { color: var(--amber); }
    .channel-audio .channel-num, .channel-audio .channel-title { color: var(--sage); }

    /* ---- Search / link slot ---- */
    div[data-testid="stTextInput"] input {
        background-color: var(--panel-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        padding: 12px 14px !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stTextInput"] input::placeholder { color: var(--text-dim) !important; }

    div[data-testid="stSelectbox"] > div {
        background-color: var(--panel-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--text) !important;
    }

    /* ---- Buttons ---- */
    .stButton button {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11.5px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid var(--border) !important;
        background: var(--panel-2) !important;
        color: var(--text) !important;
        padding: 0.6rem 1rem !important;
    }
    .stButton button:hover {
        border-color: var(--amber) !important;
        color: var(--amber) !important;
    }

    /* ---- Meta row / timecode text ---- */
    .meta-row {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        color: var(--text-muted);
        display: flex;
        gap: 18px;
        flex-wrap: wrap;
        margin-top: 6px;
    }
    .meta-row .dim { color: var(--text-dim); margin-right: 4px; }

    .video-grid-card {
        background: var(--panel-2);
        border: 1px solid var(--border-soft);
        border-radius: 10px;
        padding: 1rem;
        height: 100%;
    }
    .video-grid-title {
        font-weight: 600;
        font-size: 0.92rem;
        color: var(--text);
        margin-top: 0.7rem;
        margin-bottom: 0.4rem;
        line-height: 1.35;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .video-grid-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--text-dim);
    }

    /* ---- Progress bar restyle (VU-meter feel) ---- */
    div[data-testid="stProgress"] > div > div {
        background-color: var(--border-soft) !important;
        height: 8px !important;
        border-radius: 2px !important;
    }
    div[data-testid="stProgress"] > div > div > div {
        background-color: var(--amber) !important;
        border-radius: 2px !important;
    }

    /* ---- Divider ---- */
    hr { border-color: var(--border-soft) !important; }
</style>
""", unsafe_allow_html=True)

def get_ffmpeg_dir():
    # 1. Check if already in system PATH
    sys_ffmpeg = shutil.which('ffmpeg') or shutil.which('ffmpeg.exe')
    if sys_ffmpeg:
        return os.path.dirname(sys_ffmpeg)
        
    # 2. Check fallback extraction paths on Windows
    fallback_paths = [
        r"C:\ffmpeg\bin",
        r"C:\ffmpeg",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
        os.path.join(os.path.expanduser("~"), "ffmpeg", "bin"),
        os.path.join(os.path.expanduser("~"), "ffmpeg"),
    ]
    
    for path in fallback_paths:
        if os.path.exists(path):
            ffmpeg_exe = os.path.join(path, "ffmpeg.exe")
            if os.path.exists(ffmpeg_exe):
                return path
    return None


ffmpeg_dir = get_ffmpeg_dir()
ffmpeg_installed = ffmpeg_dir is not None

if ffmpeg_dir:
    os.environ["PATH"] += os.pathsep + ffmpeg_dir


def get_common_ydl_opts():
    opts = {
        'nocheckcertificate': True,
        'geo_bypass': True,
        'quiet': True,
        'no_warnings': True,
        'cachedir': False,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'mweb'],
            }
        },
        'source_address': '0.0.0.0',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    
    # Explicitly pass ffmpeg directory to yt-dlp to prevent PATH resolution issues
    if ffmpeg_dir:
        opts['ffmpeg_location'] = ffmpeg_dir
        
    try:
        from yt_dlp.networking.impersonate import ImpersonateTarget
        opts['impersonate'] = ImpersonateTarget.from_str('chrome')
    except Exception:
        pass
        
    return opts


def execute_download(ydl_opts, url, status_text):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return True
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg or "Forbidden" in error_msg:
            status_text.warning("Hızlı sunucu kanalı engellendi. Alternatif kanal deneniyor...")
            ydl_opts['format'] = 'best'
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    return True
            except Exception as e2:
                status_text.error(f"Hata oluştu: {str(e2)}")
                return False
        else:
            status_text.error(f"Hata oluştu: {error_msg}")
            return False


# ---- Header ----
st.markdown("""
<div class="header-container">
    <div>
        <div class="brand-row">
            <div class="brand-mark">⚡</div>
            <div class="brand-name">Neon–Tube</div>
        </div>
        <div class="brand-tag">medya i̇ndirme konsolu</div>
    </div>
</div>
""", unsafe_allow_html=True)

if ffmpeg_installed:
    st.markdown('<span class="status-chip-ok"><span class="dot"></span>FFMPEG HAZIR — MP3 VE 1080P AKTİF</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="status-chip-warn"><span class="dot"></span>FFMPEG YOK — ORİJİNAL FORMAT KULLANILACAK</span>', unsafe_allow_html=True)

st.write("")

# Initialize Session States
if "active_url" not in st.session_state:
    st.session_state.active_url = ""
if "active_video_info" not in st.session_state:
    st.session_state.active_video_info = None
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# Navigation Tabs
tab_search, tab_direct = st.tabs(["Ara ve Oynat", "Doğrudan Link"])

# --- TAB 1: SEARCH & PLAY ---
with tab_search:
    with st.container(border=True):
        st.markdown('<div class="panel-header">Youtube Araması</div>', unsafe_allow_html=True)

        col_search_input, col_search_btn = st.columns([4, 1])
        with col_search_input:
            search_query = st.text_input("Aramak istediğiniz video, sanatçı veya YouTube linki", placeholder="Örn: Tarkan - Yolla", label_visibility="collapsed")
        with col_search_btn:
            if st.button("Getir", use_container_width=True):
                if search_query:
                    st.session_state.search_query = search_query
                    st.session_state.search_results = []

        if st.session_state.search_query:
            if not st.session_state.search_results:
                with st.spinner("Youtube taranıyor..."):
                    ydl_opts_search = get_common_ydl_opts()
                    ydl_opts_search.update({
                        'default_search': 'ytsearch',
                        'extract_flat': True,
                    })
                    with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                        try:
                            if "youtube.com/" in st.session_state.search_query or "youtu.be/" in st.session_state.search_query:
                                st.session_state.active_url = st.session_state.search_query
                                st.session_state.active_video_info = None
                            else:
                                res = ydl.extract_info(f"ytsearch6:{st.session_state.search_query}", download=False)
                                st.session_state.search_results = res.get('entries', [])
                        except Exception as e:
                            st.error(f"Arama sırasında hata: {str(e)}")

            if st.session_state.search_results:
                st.write("")
                st.markdown('<div class="panel-header">Sonuçlar</div>', unsafe_allow_html=True)

                grid_cols = st.columns(3)
                for idx, entry in enumerate(st.session_state.search_results):
                    col = grid_cols[idx % 3]
                    video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
                    thumb = f"https://img.youtube.com/vi/{entry.get('id')}/mqdefault.jpg"

                    duration = entry.get('duration', 0)
                    if duration:
                        mins, secs = divmod(int(duration), 60)
                        dur_str = f"{mins}:{secs:02d}"
                    else:
                        dur_str = "Bilinmiyor"

                    with col:
                        st.markdown(f"""
                        <div class="video-grid-card">
                            <img src="{thumb}" style="width:100%; border-radius:6px; border:1px solid var(--border-soft);">
                            <div class="video-grid-title">{entry.get('title')}</div>
                            <div class="video-grid-meta">{entry.get('uploader')} · {dur_str}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("Seç ve Yükle", key=f"sel_{entry.get('id')}", use_container_width=True):
                            st.session_state.active_url = video_url
                            st.session_state.active_video_info = None

# --- TAB 2: DIRECT LINK ---
with tab_direct:
    with st.container(border=True):
        st.markdown('<div class="panel-header">Video Linki</div>', unsafe_allow_html=True)

        pasted_url = st.text_input("YouTube video adresi", value=st.session_state.active_url, placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
        if pasted_url != st.session_state.active_url:
            st.session_state.active_url = pasted_url
            st.session_state.active_video_info = None

# --- ACTIVE DOWNLOAD & PREVIEW PANEL ---
if st.session_state.active_url:
    with st.container(border=True):
        st.markdown('<div class="panel-header">Aktif Kayıt</div>', unsafe_allow_html=True)

        if st.session_state.active_video_info is None:
            try:
                with st.spinner("Video bilgileri yükleniyor..."):
                    ydl_opts = get_common_ydl_opts()
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(st.session_state.active_url, download=False)
                        st.session_state.active_video_info = {
                            'url': st.session_state.active_url,
                            'title': info.get('title', 'Bilinmeyen Başlık'),
                            'thumbnail': info.get('thumbnail', ''),
                            'duration': info.get('duration', 0),
                            'channel': info.get('uploader', 'Bilinmeyen Kanal'),
                            'views': info.get('view_count', 0),
                            'likes': info.get('like_count', 0),
                            'upload_date': info.get('upload_date', '')
                        }
            except Exception as e:
                st.error(f"Hata: Link analiz edilemedi. {str(e)}")
                st.session_state.active_video_info = None

        info = st.session_state.active_video_info
        if info:
            preview_col, details_col = st.columns([1.1, 0.9])

            with preview_col:
                st.video(info['url'])

            with details_col:
                mins, secs = divmod(info['duration'], 60)
                duration_str = f"{mins}:{secs:02d}"
                views_str = f"{info['views']:,}" if info['views'] else "Bilinmiyor"

                st.markdown(f"""
                <div style="font-size: 1.05rem; font-weight: 600; margin-bottom: 6px; color: var(--text);">{info['title']}</div>
                <div class="meta-row">
                    <span><span class="dim">Kanal</span>{info['channel']}</span>
                    <span><span class="dim">Süre</span>{duration_str}</span>
                    <span><span class="dim">İzlenme</span>{views_str}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<hr style='margin: 1.8rem 0;'>", unsafe_allow_html=True)

            video_dl_col, audio_dl_col = st.columns(2, gap="large")

            # --- VIDEO DOWNLOAD CARD ---
            with video_dl_col:
                with st.container(border=True):
                    st.markdown("""
                    <div class="channel-video">
                        <span class="channel-num">CH.01</span>
                        <div class="channel-title">Video</div>
                        <div class="channel-desc">Görüntü ve ses birleşik dosya.</div>
                    </div>
                    """, unsafe_allow_html=True)

                    video_quality = st.selectbox(
                        "Video Çözünürlük Sınırı",
                        ["1080p (Full HD)", "720p (HD)", "480p (Orta Kalite)", "360p (Düşük Kalite)", "4K / En Yüksek"],
                        key="v_res",
                        label_visibility="collapsed"
                    )

                    st.write("")
                    if st.button("İndir — Video", use_container_width=True, key="btn_dl_video"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        temp_dir = tempfile.mkdtemp()

                        def video_hook(d):
                            if d['status'] == 'downloading':
                                percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
                                try:
                                    percent = float(percent_str) / 100.0
                                    progress_bar.progress(percent)
                                    status_text.text(f"İndiriliyor: {d.get('_percent_str', '0%')} | Hız: {d.get('_speed_str', 'N/A')}")
                                except ValueError:
                                    pass
                            elif d['status'] == 'finished':
                                progress_bar.progress(1.0)
                                status_text.text("Görüntü ve ses birleştiriliyor...")

                        res_map = {
                            "1080p (Full HD)": "1080",
                            "720p (HD)": "720",
                            "480p (Orta Kalite)": "480",
                            "360p (Düşük Kalite)": "360",
                            "4K / En Yüksek": "4320",
                        }
                        res_val = res_map.get(video_quality, "1080")

                        ydl_opts_video = get_common_ydl_opts()
                        ydl_opts_video.update({
                            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                            'progress_hooks': [video_hook],
                        })

                        if ffmpeg_installed:
                            ydl_opts_video['format'] = f'bestvideo[height<={res_val}]+bestaudio/bestvideo[height<={res_val}][ext=mp4]+bestaudio[ext=m4a]/best[height<={res_val}]/best'
                        else:
                            ydl_opts_video['format'] = f'best[height<={res_val}]/best'

                        try:
                            success = execute_download(ydl_opts_video, info['url'], status_text)
                            if success:
                                downloaded_files = os.listdir(temp_dir)
                                if downloaded_files:
                                    filename = downloaded_files[0]
                                    file_path = os.path.join(temp_dir, filename)
                                    with open(file_path, "rb") as f:
                                        file_bytes = f.read()

                                    status_text.success("Video hazır. Aşağıdan kaydet:")
                                    st.download_button(
                                        label=f"Kaydet — {filename}",
                                        data=file_bytes,
                                        file_name=filename,
                                        mime="video/mp4",
                                        use_container_width=True
                                    )
                                else:
                                    status_text.error("Hata: Video dosyası oluşturulamadı.")
                        finally:
                            shutil.rmtree(temp_dir, ignore_errors=True)

            # --- AUDIO/MP3 DOWNLOAD CARD ---
            with audio_dl_col:
                with st.container(border=True):
                    st.markdown("""
                    <div class="channel-audio">
                        <span class="channel-num">CH.02</span>
                        <div class="channel-title">Ses (MP3)</div>
                        <div class="channel-desc">Yalnızca ses dosyasını indirir.</div>
                    </div>
                    """, unsafe_allow_html=True)

                    audio_format = st.selectbox(
                        "Ses Formatı ve Kalitesi",
                        ["MP3 (320 kbps - Ultra Kalite)", "MP3 (192 kbps - Standart)", "M4A (Orijinal Ses - Dönüştürmesiz)"],
                        key="a_fmt",
                        label_visibility="collapsed"
                    )

                    st.write("")
                    if st.button("İndir — Ses", use_container_width=True, key="btn_dl_audio"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        temp_dir = tempfile.mkdtemp()

                        def audio_hook(d):
                            if d['status'] == 'downloading':
                                percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
                                try:
                                    percent = float(percent_str) / 100.0
                                    progress_bar.progress(percent)
                                    status_text.text(f"Ses indiriliyor: {d.get('_percent_str', '0%')}")
                                except ValueError:
                                    pass
                            elif d['status'] == 'finished':
                                progress_bar.progress(1.0)
                                status_text.text("Ses dosyası işleniyor...")

                        ydl_opts_audio = get_common_ydl_opts()
                        ydl_opts_audio.update({
                            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                            'progress_hooks': [audio_hook],
                        })

                        if "MP3" in audio_format:
                            bitrate = "320" if "320" in audio_format else "192"
                            if ffmpeg_installed:
                                ydl_opts_audio.update({
                                    'format': 'bestaudio/best',
                                    'postprocessors': [{
                                        'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3',
                                        'preferredquality': bitrate,
                                    }],
                                })
                            else:
                                ydl_opts_audio.update({'format': 'bestaudio[ext=m4a]/bestaudio/best'})
                                st.warning("FFmpeg kurulu olmadığı için orijinal ses (M4A) formatında indiriliyor.")
                        else:
                            ydl_opts_audio.update({'format': 'bestaudio[ext=m4a]/bestaudio/best'})

                        try:
                            success = execute_download(ydl_opts_audio, info['url'], status_text)
                            if success:
                                downloaded_files = [f for f in os.listdir(temp_dir) if not f.endswith(('.part', '.ytdl'))]
                                if downloaded_files:
                                    filename = downloaded_files[0]
                                    file_path = os.path.join(temp_dir, filename)
                                    with open(file_path, "rb") as f:
                                        file_bytes = f.read()

                                    status_text.success("Ses dosyası hazır. Aşağıdan kaydet:")

                                    mime_type = "audio/mp3" if ".mp3" in filename else "audio/mp4"
                                    st.download_button(
                                        label=f"Kaydet — {filename}",
                                        data=file_bytes,
                                        file_name=filename,
                                        mime=mime_type,
                                        use_container_width=True
                                    )
                                else:
                                    status_text.error("Hata: Ses dosyası oluşturulamadı.")
                        finally:
                            shutil.rmtree(temp_dir, ignore_errors=True)