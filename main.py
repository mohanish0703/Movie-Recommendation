import streamlit as st
import pickle
import pandas as pd
import requests
import random

st.set_page_config(
    page_title="CineMatch · Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');

:root {
    --bg:      #060609;
    --surface: #0f0f17;
    --card:    #14141f;
    --card2:   #1a1a28;
    --border:  #222235;
    --red:     #e63946;
    --red-dim: #7a1c24;
    --gold:    #ffc857;
    --text:    #f0f0f8;
    --muted:   #6b6b8a;
    --sub:     #9090b0;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"],[data-testid="stToolbar"],footer { display:none !important; }
[data-testid="stMainBlockContainer"] { padding-top:0 !important; }

::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:99px; }

[data-testid="stSidebar"] { background:var(--surface) !important; border-right:1px solid var(--border); }
[data-testid="stSidebar"] * { color:var(--text) !important; }

/* HERO */
.hero-wrap { position:relative; width:100%; min-height:300px; display:flex; align-items:center; padding:3rem 4rem; overflow:hidden; box-sizing:border-box; }
.hero-bg { position:absolute; inset:0; background:linear-gradient(135deg,#0d0005 0%,#120010 40%,#060609 100%); z-index:0; }
.hero-bg::after { content:''; position:absolute; inset:0; background:radial-gradient(ellipse 55% 70% at 85% 50%,rgba(230,57,70,.18) 0%,transparent 65%),radial-gradient(ellipse 35% 50% at 10% 20%,rgba(255,200,87,.06) 0%,transparent 60%); }
.hero-content { position:relative; z-index:2; max-width:620px; }
.hero-eyebrow { font-size:.68rem; font-weight:600; letter-spacing:.22em; color:var(--red); text-transform:uppercase; margin-bottom:.8rem; display:flex; align-items:center; gap:.5rem; }
.hero-eyebrow::before { content:''; display:inline-block; width:24px; height:2px; background:var(--red); }
.hero-title { font-family:'Bebas Neue',sans-serif; font-size:clamp(3.5rem,7vw,5.5rem); line-height:.95; letter-spacing:.02em; color:var(--text); margin:0 0 1rem; }
.hero-title em { font-style:normal; -webkit-text-stroke:2px var(--red); color:transparent; }
.hero-sub { color:var(--sub); font-size:.95rem; line-height:1.65; max-width:440px; }
.hero-deco { position:absolute; right:3rem; top:50%; transform:translateY(-50%); z-index:2; opacity:.06; font-family:'Bebas Neue',sans-serif; font-size:13rem; line-height:1; color:var(--red); pointer-events:none; user-select:none; }

/* SELECT & BUTTON */
div[data-baseweb="select"] > div { background:var(--card2) !important; border:1px solid var(--border) !important; border-radius:12px !important; color:var(--text) !important; font-family:'Inter',sans-serif !important; transition:border-color .2s; }
div[data-baseweb="select"] > div:hover,div[data-baseweb="select"] > div:focus-within { border-color:var(--red) !important; }
div[data-baseweb="select"] * { color:var(--text) !important; }
div[data-baseweb="popover"] { background:var(--card2) !important; border:1px solid var(--border) !important; border-radius:12px !important; }
div[data-baseweb="popover"] li { background:var(--card2) !important; color:var(--text) !important; }
div[data-baseweb="popover"] li:hover { background:var(--border) !important; }
.stButton > button { background:var(--red) !important; color:#fff !important; font-family:'Inter',sans-serif !important; font-weight:600 !important; font-size:.88rem !important; border:none !important; border-radius:12px !important; padding:.7rem 1.2rem !important; letter-spacing:.03em; transition:filter .2s,transform .15s !important; white-space:nowrap; }
.stButton > button:hover { filter:brightness(1.15) !important; transform:translateY(-2px) !important; }

/* SECTION LABEL */
.sec-label { display:flex; align-items:center; gap:.75rem; font-size:.68rem; font-weight:600; letter-spacing:.2em; text-transform:uppercase; color:var(--muted); margin:2rem 0 1rem; }
.sec-label::after { content:''; flex:1; height:1px; background:var(--border); }
.sec-label span { color:var(--red); }

/* SELECTED BANNER */
.sel-banner { display:flex; gap:1.8rem; align-items:flex-start; background:linear-gradient(135deg,var(--card2),var(--surface)); border:1px solid var(--border); border-left:4px solid var(--red); border-radius:16px; padding:1.5rem 2rem; margin-bottom:.5rem; }
.sel-poster { width:85px; border-radius:10px; flex-shrink:0; box-shadow:0 8px 24px rgba(0,0,0,.5); }
.badge-gold { display:inline-flex; align-items:center; gap:.2rem; background:var(--gold); color:#0a0a0f; font-weight:700; font-size:.72rem; padding:.18rem .5rem; border-radius:6px; }
.badge-genre { background:var(--card); color:var(--sub); border:1px solid var(--border); font-size:.7rem; font-weight:500; padding:.18rem .5rem; border-radius:6px; }

/* MOVIE CARD — image + overlay only */
.card-outer { position:relative; border-radius:14px; overflow:hidden; background:var(--card); border:1px solid var(--border); transition:transform .28s cubic-bezier(.22,1,.36,1),box-shadow .28s; }
.card-outer:hover { transform:translateY(-8px) scale(1.02); box-shadow:0 24px 48px rgba(0,0,0,.7); }
.card-outer img { width:100%; display:block; aspect-ratio:2/3; object-fit:cover; }
.card-overlay { position:absolute; inset:0; background:linear-gradient(to top,rgba(6,6,9,.97) 0%,rgba(6,6,9,.5) 45%,transparent 70%); opacity:0; transition:opacity .28s; display:flex; flex-direction:column; justify-content:flex-end; padding:1rem; }
.card-outer:hover .card-overlay { opacity:1; }
.card-rat { position:absolute; top:.55rem; right:.55rem; background:rgba(6,6,9,.85); color:var(--gold); font-size:.7rem; font-weight:700; padding:.2rem .48rem; border-radius:6px; backdrop-filter:blur(6px); }
.trend-num { font-family:'Bebas Neue',sans-serif; font-size:3.5rem; line-height:1; color:var(--border); position:absolute; bottom:-.2rem; left:.5rem; pointer-events:none; user-select:none; transition:color .28s; }
.card-outer:hover .trend-num { color:var(--red-dim); }
.overlay-title { font-family:'Playfair Display',serif; font-size:.95rem; font-weight:700; color:var(--text); margin-bottom:.3rem; }
.overlay-desc { font-size:.72rem; color:var(--sub); line-height:1.55; }

/* CARD TEXT BELOW IMAGE — rendered via st.markdown separately */
.ctext-wrap { padding:.6rem .2rem .9rem; }
.ctext-score { font-size:.68rem; color:var(--red); font-weight:700; margin-bottom:.15rem; }
.ctext-title { font-size:.88rem; font-weight:600; color:var(--text); line-height:1.3; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:.12rem; }
.ctext-meta { font-size:.72rem; color:var(--muted); }

/* WATCHLIST */
.wl-row { display:flex; align-items:center; justify-content:space-between; padding:.38rem 0; border-bottom:1px solid var(--border); gap:.5rem; }
.wl-title { font-size:.8rem; color:var(--text); flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

/* MATCH BAR */
.match-row { margin-bottom:.45rem; }
.match-header { display:flex; justify-content:space-between; font-size:.73rem; color:var(--sub); margin-bottom:.12rem; }
.match-title-t { white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:145px; }
.match-pct { color:var(--red); font-weight:700; }
.match-bar-bg { height:3px; background:var(--border); border-radius:99px; }
.match-bar-fill { height:3px; background:linear-gradient(90deg,var(--red-dim),var(--red)); border-radius:99px; }

/* EMPTY */
.empty-state { text-align:center; padding:4rem 2rem; }
.empty-icon { font-size:3.5rem; margin-bottom:1rem; filter:grayscale(1) opacity(.25); }
.empty-title { font-family:'Bebas Neue',sans-serif; font-size:2rem; color:var(--border); letter-spacing:.05em; margin-bottom:.5rem; }
.empty-sub { font-size:.85rem; color:var(--muted); line-height:1.7; }

/* FOOTER */
.app-footer { margin-top:4rem; padding:1.5rem 4rem; border-top:1px solid var(--border); display:flex; justify-content:space-between; font-size:.72rem; color:var(--muted); }
</style>
""", unsafe_allow_html=True)

# ── TMDB API ──────────────────────────────────────────────────────────────────
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
POSTER_BASE  = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER  = "https://via.placeholder.com/500x750/14141f/e63946?text=No+Poster"

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id: int) -> dict:
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        d   = requests.get(url, timeout=5).json()
        poster   = POSTER_BASE + d["poster_path"] if d.get("poster_path") else PLACEHOLDER
        rating   = round(d.get("vote_average", 0), 1)
        year     = d.get("release_date", "")[:4]
        overview = d.get("overview", "")
        overview = overview[:200] + "…" if len(overview) > 200 else overview
        genres   = [g["name"] for g in d.get("genres", [])[:3]]
        runtime  = d.get("runtime", 0)
        return {"poster": poster, "rating": rating, "year": year,
                "overview": overview, "genres": genres, "runtime": runtime}
    except Exception:
        return {"poster": PLACEHOLDER, "rating": 0, "year": "",
                "overview": "", "genres": [], "runtime": 0}

@st.cache_resource(show_spinner=False)
def load_data():
    movies     = pickle.load(open("movie_list.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity

def recommend(movie, movies, similarity, n=8):
    idx       = movies[movies["title"] == movie].index[0]
    distances = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)[1:n+1]
    results   = []
    for i, score in distances:
        row = movies.iloc[i]
        det = fetch_movie_details(int(row.movie_id))
        results.append({"title": row.title, "movie_id": int(row.movie_id),
                        "score": round(score * 100, 1), **det})
    return results

def get_trending(movies, n=6):
    popular = ["The Dark Knight","Inception","Interstellar","The Avengers",
               "Pulp Fiction","The Shawshank Redemption","The Godfather",
               "Fight Club","Forrest Gump","The Matrix"]
    found = []
    for t in popular:
        m = movies[movies["title"] == t]
        if not m.empty:
            found.append({"title": t, "movie_id": int(m.iloc[0].movie_id)})
        if len(found) == n: break
    if len(found) < n:
        for _, row in movies.sample(n - len(found), random_state=42).iterrows():
            found.append({"title": row.title, "movie_id": int(row.movie_id)})
    return found

# ── Card renderers ─────────────────────────────────────────────────────────────
# Split into TWO st.markdown calls per card:
#   1. Image block (card-outer) — hover overlay, rating badge, trend number
#   2. Text block (ctext-wrap)  — title, year, score
# This avoids Streamlit stripping nested div classes inside a single markdown.

def render_card_image(rec, number=None):
    rat = f'<span style="position:absolute;top:.55rem;right:.55rem;background:rgba(6,6,9,.85);color:#ffc857;font-size:.7rem;font-weight:700;padding:.2rem .48rem;border-radius:6px;">{rec["rating"]} ⭐</span>' if rec.get("rating") else ""
    num = f'<span style="font-family:Bebas Neue,sans-serif;font-size:3.5rem;line-height:1;color:#222235;position:absolute;bottom:-.2rem;left:.5rem;pointer-events:none;user-select:none;">{number:02d}</span>' if number is not None else ""
    ov  = rec.get("overview","")[:90] + "…" if len(rec.get("overview","")) > 90 else rec.get("overview","")
    st.markdown(f"""
<div class="card-outer">
  <img src="{rec['poster']}" alt="{rec['title']}" loading="lazy">
  {rat}{num}
  <div class="card-overlay">
    <p class="overlay-title">{rec['title']}</p>
    <p class="overlay-desc">{ov}</p>
  </div>
</div>""", unsafe_allow_html=True)

def render_card_text(rec, show_score=False):
    score_html = f'<p class="ctext-score">▲ {rec["score"]}% match</p>' if show_score and rec.get("score") else ""
    genre = ", ".join(rec.get("genres", [])[:2])
    meta  = " · ".join(filter(None, [rec.get("year",""), genre]))
    title = rec['title'][:26] + "…" if len(rec['title']) > 26 else rec['title']
    st.markdown(f"""
<div class="ctext-wrap">
  {score_html}
  <p class="ctext-title" title="{rec['title']}">{title}</p>
  <p class="ctext-meta">{meta}</p>
</div>""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("watchlist",[]),("last_recs",[]),("last_selected",None),("sel_details",{})]:
    if k not in st.session_state: st.session_state[k] = v

# ── Load ──────────────────────────────────────────────────────────────────────
with st.spinner("Loading…"):
    movies, similarity = load_data()
movie_list = movies["title"].values

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div class="hero-eyebrow">AI-Powered Movie Discovery</div>
    <div class="hero-title">CINE<br><em>MATCH</em></div>
    <p class="hero-sub">Tell us one movie you love — our engine finds eight more you'll obsess over.</p>
  </div>
  <div class="hero-deco">🎬</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SEARCH BAR
# ══════════════════════════════════════════════════════════════════════════════
c1, c2, c3 = st.columns([5, 1.1, 1], gap="small")
with c1:
    selected = st.selectbox(" ", movie_list, label_visibility="collapsed",
                            placeholder="🔍  Search 5,000+ movies…")
with c2:
    go = st.button("✦  Recommend", use_container_width=True)
with c3:
    lucky = st.button("🎲 Random", use_container_width=True)

if lucky:
    selected = str(random.choice(movie_list))
    go = True

# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
main_col, side_col = st.columns([3.2, 1], gap="large")

with main_col:
    # ── Trigger recommendation ────────────────────────────────────────────
    if go and selected:
        with st.spinner("Matching your taste…"):
            recs    = recommend(selected, movies, similarity)
            sel_det = fetch_movie_details(int(movies[movies["title"]==selected].iloc[0].movie_id))
        st.session_state.last_recs     = recs
        st.session_state.last_selected = selected
        st.session_state.sel_details   = sel_det

    # ── Results ───────────────────────────────────────────────────────────
    if st.session_state.last_recs:
        sel     = st.session_state.last_selected
        sel_det = st.session_state.sel_details
        recs    = st.session_state.last_recs

        # Selected movie banner
        genres_html = " ".join([f'<span class="badge-genre">{g}</span>' for g in sel_det.get("genres",[])])
        rt = f'{sel_det["runtime"]} min · ' if sel_det.get("runtime") else ""
        st.markdown(f"""
<div class="sel-banner">
  <img class="sel-poster" src="{sel_det.get('poster', PLACEHOLDER)}" alt="{sel}">
  <div>
    <p style="font-size:.65rem;font-weight:600;letter-spacing:.2em;color:#e63946;text-transform:uppercase;margin:0 0 .4rem">YOU SELECTED</p>
    <p style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:#f0f0f8;margin:0 0 .35rem">{sel}</p>
    <p style="font-size:.8rem;color:#9090b0;margin:0 0 .55rem">
      {sel_det.get('year','')} · {rt}{genres_html}
      {'<span class="badge-gold">⭐ ' + str(sel_det.get('rating','')) + '</span>' if sel_det.get('rating') else ''}
    </p>
    <p style="font-size:.85rem;color:#6b6b8a;line-height:1.65;margin:0">{sel_det.get('overview','')}</p>
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-label"><span>▶</span> BECAUSE YOU LIKED IT</div>', unsafe_allow_html=True)

        # Row 1
        row1 = st.columns(4, gap="small")
        for i, rec in enumerate(recs[:4]):
            with row1[i]:
                render_card_image(rec)
                render_card_text(rec, show_score=True)
                if st.button("＋ Watchlist", key=f"wl1_{i}"):
                    if rec["title"] not in st.session_state.watchlist:
                        st.session_state.watchlist.append(rec["title"])
                        st.toast(f"Added **{rec['title']}**!", icon="✅")

        # Row 2
        row2 = st.columns(4, gap="small")
        for i, rec in enumerate(recs[4:8]):
            with row2[i]:
                render_card_image(rec)
                render_card_text(rec, show_score=True)
                if st.button("＋ Watchlist", key=f"wl2_{i}"):
                    if rec["title"] not in st.session_state.watchlist:
                        st.session_state.watchlist.append(rec["title"])
                        st.toast(f"Added **{rec['title']}**!", icon="✅")

    else:
        # ── Trending ──────────────────────────────────────────────────────
        st.markdown('<div class="sec-label"><span>🔥</span> TRENDING NOW</div>', unsafe_allow_html=True)
        with st.spinner("Loading trending…"):
            trending      = get_trending(movies, 6)
            trend_details = [fetch_movie_details(t["movie_id"]) for t in trending]
        trend_data = [{**t, **d} for t, d in zip(trending, trend_details)]

        t_cols = st.columns(6, gap="small")
        for i, t in enumerate(trend_data):
            with t_cols[i]:
                render_card_image(t, number=i+1)
                render_card_text(t)

        st.markdown("""
<div class="empty-state">
  <div class="empty-icon">🎬</div>
  <p class="empty-title">FIND YOUR NEXT FAVOURITE</p>
  <p class="empty-sub">Search above and hit <b style="color:#e63946">✦ Recommend</b><br>
  or try <b style="color:#ffc857">🎲 Random</b> to let us surprise you.</p>
</div>""", unsafe_allow_html=True)

# ── Right panel: watchlist ─────────────────────────────────────────────────
with side_col:
    st.markdown('<div class="sec-label" style="margin-top:.3rem"><span>📌</span> MY WATCHLIST</div>', unsafe_allow_html=True)
    if st.session_state.watchlist:
        for i, title in enumerate(st.session_state.watchlist):
            ca, cb = st.columns([5, 1])
            with ca:
                st.markdown(f'<div class="wl-row"><span class="wl-title">{title}</span></div>', unsafe_allow_html=True)
            with cb:
                if st.button("✕", key=f"rm_{i}"):
                    st.session_state.watchlist.remove(title)
                    st.rerun()
        st.markdown("<div style='margin-top:.6rem'></div>", unsafe_allow_html=True)
        if st.button("🗑 Clear all", use_container_width=True):
            st.session_state.watchlist = []
            st.rerun()
    else:
        st.markdown("<p style='font-size:.8rem;color:#6b6b8a;line-height:1.7'>Hit <b>＋ Watchlist</b> on any card to save movies here.</p>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
<div style="padding:.5rem 0 1.2rem">
  <p style="font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:.06em;color:#f0f0f8;margin:0">
    CINE<span style="color:#e63946">MATCH</span>
  </p>
  <p style="font-size:.73rem;color:#6b6b8a;margin:.15rem 0 0">AI Movie Recommender</p>
</div>""", unsafe_allow_html=True)

    st.markdown("**📊 Dataset**")
    col1, col2 = st.columns(2)
    with col1: st.metric("Movies", f"{len(movies):,}")
    with col2: st.metric("Pairs",  f"{len(movies)**2//1_000_000}M+")

    st.divider()
    st.markdown("**⚙️ How it works**")
    st.markdown("""
<p style="font-size:.8rem;color:#6b6b8a;line-height:1.9;margin:0">
  <b style="color:#e63946">1. Vectorise</b> — Genres, cast, keywords & crew combined into a text corpus per movie<br>
  <b style="color:#e63946">2. BoW</b> — CountVectorizer builds a Bag-of-Words matrix<br>
  <b style="color:#e63946">3. Similarity</b> — Cosine similarity scored across all pairs<br>
  <b style="color:#e63946">4. Rank</b> — Top-8 nearest neighbours returned instantly
</p>""", unsafe_allow_html=True)

    if st.session_state.last_recs:
        st.divider()
        st.markdown("**📈 Match Scores**")
        for rec in st.session_state.last_recs:
            st.markdown(f"""
<div class="match-row">
  <div class="match-header">
    <span class="match-title-t">{rec['title']}</span>
    <span class="match-pct">{rec.get('score',0)}%</span>
  </div>
  <div class="match-bar-bg">
    <div class="match-bar-fill" style="width:{rec.get('score',0)}%"></div>
  </div>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.caption("")

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown(""")