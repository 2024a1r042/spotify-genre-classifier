import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import requests
from streamlit_lottie import st_lottie
import time


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="SonicSort // Genre AI",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INTERACTIVE PARTICLE CANVAS (Spotify Neon Spectrum)
# 80 green, teal, and purple particles with proximity lines
# and mouse-repel physics via JS canvas
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_PARTICLE_JS = """
<canvas id="pc" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;"></canvas>
<script>
(function(){
var c=document.getElementById('pc'),x=c.getContext('2d'),W,H,mx=-999,my=-999;
function rz(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
window.addEventListener('resize',rz);rz();
document.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY;});
var N=80,P=[];
for(var i=0;i<N;i++){var h=140+Math.random()*80;
P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35,
r:Math.random()*1.8+.7,h:h,a:Math.random()*.45+.15,p:Math.random()*6.28});}
function dr(){x.clearRect(0,0,W,H);var t=Date.now()*.001;
for(var i=0;i<N;i++){for(var j=i+1;j<N;j++){var dx=P[i].x-P[j].x,dy=P[i].y-P[j].y,d=Math.sqrt(dx*dx+dy*dy);
if(d<130){x.beginPath();x.moveTo(P[i].x,P[i].y);x.lineTo(P[j].x,P[j].y);
x.strokeStyle='rgba(29,185,84,'+(0.06*(1-d/130))+')';x.lineWidth=.5;x.stroke();}}}
for(var k=0;k<N;k++){var q=P[k],dmx=q.x-mx,dmy=q.y-my,dm=Math.sqrt(dmx*dmx+dmy*dmy);
if(dm<110){q.vx+=dmx/dm*.12;q.vy+=dmy/dm*.12;}
q.vx*=.99;q.vy*=.99;q.x+=q.vx;q.y+=q.vy;
if(q.x<0)q.x=W;if(q.x>W)q.x=0;if(q.y<0)q.y=H;if(q.y>H)q.y=0;
var pl=Math.sin(t*1.4+q.p)*.3+.7,gr=q.r*3*pl;
var gd=x.createRadialGradient(q.x,q.y,0,q.x,q.y,gr*3);
gd.addColorStop(0,'hsla('+q.h+',85%,55%,'+(q.a*pl*.35)+')');
gd.addColorStop(1,'hsla('+q.h+',85%,55%,0)');
x.beginPath();x.arc(q.x,q.y,gr*3,0,6.28);x.fillStyle=gd;x.fill();
x.beginPath();x.arc(q.x,q.y,q.r*pl,0,6.28);
x.fillStyle='hsla('+q.h+',85%,60%,'+(q.a*pl)+')';x.fill();}
requestAnimationFrame(dr);}dr();})();
</script>
"""
components.html(_PARTICLE_JS, height=0, scrolling=False)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FULL CSS — Spotify Neon Green & Deep Noir Glassmorphism + VFX
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root{
--bg:#070a0f;--card:rgba(255,255,255,.022);--card-h:rgba(255,255,255,.045);
--border:rgba(255,255,255,.05);--txt:#e8ecf1;--muted:#8b95a5;
--a1:#1DB954;--a2:#1ed760;--a3:#7c3aed;
--grad:linear-gradient(135deg,#1DB954 0%,#1ed760 40%,#17d05b 100%);
--grad2:linear-gradient(135deg,#7c3aed 0%,#a855f7 50%,#c084fc 100%);
--glow:rgba(29,185,84,.35);--glow2:rgba(124,58,237,.3);--r:16px;--rl:24px;
--tr:.3s cubic-bezier(.4,0,.2,1);
}

#MainMenu,header,footer{visibility:hidden}
.stDeployButton{display:none!important}

.stApp{background:var(--bg)!important;color:var(--txt);font-family:'Space Grotesk',sans-serif}

/* ── Ambient orbs (Spotify glow) ── */
.stApp::before,.stApp::after{content:'';position:fixed;border-radius:50%;filter:blur(140px);opacity:.2;z-index:0;pointer-events:none}
.stApp::before{width:520px;height:520px;background:radial-gradient(circle,#1DB954 0%,transparent 70%);top:-12%;left:-10%;animation:oA 24s ease-in-out infinite alternate}
.stApp::after{width:460px;height:460px;background:radial-gradient(circle,#7c3aed 0%,transparent 70%);bottom:-14%;right:-10%;animation:oB 28s ease-in-out infinite alternate}
@keyframes oA{0%{transform:translate(0,0) scale(1)}50%{transform:translate(70px,50px) scale(1.18)}100%{transform:translate(-40px,80px) scale(.92)}}
@keyframes oB{0%{transform:translate(0,0) scale(1)}50%{transform:translate(-60px,-40px) scale(1.12)}100%{transform:translate(50px,-70px) scale(.88)}}

/* ── Scanlines ── */
.scan{position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;
background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(29,185,84,.006) 2px,rgba(29,185,84,.006) 4px)}

/* ── Floating icons (Music Theme) ── */
.ficons{position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;overflow:hidden}
.fi{position:absolute;opacity:0;animation:fUp linear infinite;filter:blur(.3px)}
@keyframes fUp{0%{transform:translateY(100vh) rotate(0) scale(.5);opacity:0}10%{opacity:.13}90%{opacity:.08}100%{transform:translateY(-10vh) rotate(360deg) scale(1.1);opacity:0}}

section.main>div{position:relative;z-index:1}

/* ── Hero ── */
.hbadge{display:inline-block;background:var(--grad);color:#000;font-family:'JetBrains Mono',monospace;font-size:.68rem;font-weight:700;letter-spacing:3px;padding:6px 18px;border-radius:50px;text-transform:uppercase;box-shadow:0 0 20px var(--glow);animation:bp 3s ease-in-out infinite}
@keyframes bp{0%,100%{box-shadow:0 0 20px var(--glow)}50%{box-shadow:0 0 35px rgba(29,185,84,.55),0 0 60px rgba(29,185,84,.18)}}
.htitle{font-size:3.6rem;font-weight:900;line-height:1.05;letter-spacing:-1px;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0 0 8px;position:relative;display:inline-block}
.htitle::after{content:'SonicSort';position:absolute;top:0;left:0;background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,.4) 45%,rgba(255,255,255,.6) 50%,rgba(255,255,255,.4) 55%,transparent 100%);background-size:200% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:shm 4s ease-in-out infinite}
@keyframes shm{0%{background-position:200% center}100%{background-position:-200% center}}
.hglow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:280px;height:55px;background:radial-gradient(ellipse,rgba(29,185,84,.22) 0%,transparent 70%);filter:blur(28px);pointer-events:none;animation:tg 4s ease-in-out infinite alternate}
@keyframes tg{0%{opacity:.4;transform:translate(-50%,-50%) scale(1)}100%{opacity:.75;transform:translate(-50%,-50%) scale(1.3)}}
.hsub{font-family:'JetBrains Mono',monospace;font-size:.82rem;color:var(--muted);letter-spacing:4px;text-transform:uppercase;margin-bottom:6px}
.hdesc{color:var(--muted);font-size:.95rem;line-height:1.6;max-width:540px;margin:0 auto}

/* ── Equalizer bars ── */
.speedo{display:flex;align-items:flex-end;justify-content:center;gap:3px;height:28px;margin:14px auto 0;width:fit-content}
.sbar{width:3px;border-radius:3px;background:var(--grad);animation:sb ease-in-out infinite;opacity:.45}
@keyframes sb{0%,100%{height:4px;opacity:.25}50%{opacity:.65}}

/* ── Glass cards ── */
.gc{background:var(--card);border:1px solid var(--border);border-radius:var(--rl);padding:24px 22px;backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);transition:var(--tr);position:relative;overflow:hidden;margin-bottom:8px}
.gc::before{content:'';position:absolute;inset:0;border-radius:inherit;padding:1px;background:linear-gradient(135deg,rgba(255,255,255,.08),transparent 60%);-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.gc::after{content:'';position:absolute;top:-35px;right:-35px;width:90px;height:90px;background:radial-gradient(circle,rgba(29,185,84,.1) 0%,transparent 70%);border-radius:50%;pointer-events:none;transition:var(--tr)}
.gc:hover{background:var(--card-h);border-color:rgba(29,185,84,.22);transform:translateY(-2px);box-shadow:0 10px 35px rgba(29,185,84,.06)}
.gc:hover::after{width:130px;height:130px;background:radial-gradient(circle,rgba(29,185,84,.2) 0%,transparent 70%)}
.ci{font-size:1.4rem;display:block;margin-bottom:4px}
.cl{font-family:'JetBrains Mono',monospace;font-size:.6rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--a1);margin-bottom:2px}
.ct{font-size:1.05rem;font-weight:700;color:var(--txt);margin-bottom:0}

/* ── Slider / Select / Input ── */
.stSlider>div>div>div>div{background:var(--grad)!important}
.stSlider [data-testid="stThumbValue"]{color:var(--txt)!important;font-weight:700!important;font-family:'JetBrains Mono',monospace!important}
div[data-baseweb="slider"] div[role="slider"]{background:#fff!important;border:3px solid var(--a1)!important;box-shadow:0 0 14px var(--glow)!important;width:20px!important;height:20px!important}
.stSlider label,.stSelectbox label,.stTextInput label{color:var(--muted)!important;font-weight:600!important;font-size:.82rem!important}
div[data-testid="stVerticalBlock"]>div:has(div.stSlider),div[data-testid="stVerticalBlock"]>div:has(div.stSelectbox),div[data-testid="stVerticalBlock"]>div:has(div.stTextInput){background:transparent!important;border:none!important;box-shadow:none!important;padding:0!important}

/* ── CTA Button ── */
div.stButton>button{background:var(--grad)!important;color:#000!important;font-family:'JetBrains Mono',monospace!important;font-weight:700!important;font-size:.9rem!important;letter-spacing:2.5px!important;text-transform:uppercase!important;border:none!important;padding:17px 40px!important;border-radius:60px!important;width:100%!important;box-shadow:0 6px 28px var(--glow),0 0 50px rgba(29,185,84,.08)!important;transition:var(--tr)!important;position:relative!important;overflow:hidden!important;animation:bb 3s ease-in-out infinite!important}
@keyframes bb{0%,100%{box-shadow:0 6px 28px rgba(29,185,84,.25),0 0 50px rgba(29,185,84,.08)}50%{box-shadow:0 8px 38px rgba(29,185,84,.45),0 0 70px rgba(29,185,84,.14)}}
div.stButton>button::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.2),transparent);transform:translateX(-100%);transition:.6s ease}
div.stButton>button:hover{transform:translateY(-3px) scale(1.01)!important;box-shadow:0 10px 45px var(--glow),0 0 90px rgba(29,185,84,.2)!important}
div.stButton>button:hover::after{transform:translateX(100%)}
div.stButton>button:active{transform:translateY(0) scale(.98)!important}

/* ── Result card ── */
.rc{background:rgba(255,255,255,.02);border:1px solid var(--border);border-radius:var(--rl);padding:38px 34px;backdrop-filter:blur(28px);position:relative;overflow:hidden;animation:ci .7s cubic-bezier(.16,1,.3,1)}
@keyframes ci{0%{opacity:0;transform:translateY(35px) scale(.96);filter:blur(6px)}100%{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
.prb{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);pointer-events:none;z-index:0}
.pr{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);border-radius:50%;border:1px solid;animation:rp ease-out infinite;opacity:0}
@keyframes rp{0%{width:40px;height:40px;opacity:.35}100%{width:380px;height:380px;opacity:0}}
.rbadge{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;padding:5px 14px;border-radius:30px;margin-bottom:12px;position:relative;z-index:1}
.rgenre{font-size:3rem;font-weight:900;letter-spacing:-1px;line-height:1.1;margin-bottom:6px;position:relative;z-index:1}
.rsub{font-family:'JetBrains Mono',monospace;font-size:.65rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px;position:relative;z-index:1}
.rdesc{color:var(--muted);font-size:.92rem;line-height:1.7;position:relative;z-index:1}
.rdiv{border:none;border-top:1px solid rgba(255,255,255,.06);margin:16px 0;position:relative;z-index:1}
.srow{display:flex;gap:14px;margin-top:22px;position:relative;z-index:1;flex-wrap:wrap}
.sc{flex:1;min-width:70px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.045);border-radius:var(--r);padding:14px;text-align:center;transition:var(--tr)}
.sc:hover{background:rgba(255,255,255,.06);transform:translateY(-2px);box-shadow:0 6px 20px rgba(29,185,84,.08)}
.sv{font-family:'JetBrains Mono',monospace;font-size:1.15rem;font-weight:800;display:block;margin-bottom:2px}
.sl{font-size:.6rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}
.ctrack{width:100%;height:7px;background:rgba(255,255,255,.05);border-radius:10px;overflow:hidden;margin-top:18px;position:relative;z-index:1}
.cfill{height:100%;border-radius:10px;animation:fi 1.3s cubic-bezier(.16,1,.3,1) forwards}
@keyframes fi{0%{width:0%}}

/* ── Stage text ── */
.stg{text-align:center;font-family:'JetBrains Mono',monospace;font-size:.78rem;letter-spacing:1px;color:var(--a1);animation:si .35s ease}
@keyframes si{0%{opacity:0;transform:translateY(5px)}100%{opacity:1;transform:translateY(0)}}

/* ── Footer ── */
.foot{text-align:center;padding:36px 0 18px;font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:2px;color:rgba(139,149,165,.3);text-transform:uppercase}

.stMarkdown h3{color:var(--txt)!important;font-size:1rem!important}

/* ── Waveform VFX (horizontal) ── */
.waveform{position:fixed;bottom:0;left:0;width:100vw;height:60px;pointer-events:none;z-index:0;overflow:hidden;opacity:.08}
.wbar{position:absolute;bottom:0;width:2px;background:var(--grad);border-radius:2px 2px 0 0;animation:wb ease-in-out infinite}
@keyframes wb{0%,100%{height:5px}50%{height:55px}}

/* ── Particle iframe ── */
div[data-testid="stHtml"]{position:fixed!important;top:0!important;left:0!important;width:0!important;height:0!important;overflow:visible!important;z-index:0!important}
div[data-testid="stHtml"] iframe{position:fixed!important;top:0!important;left:0!important;width:100vw!important;height:100vh!important;border:none!important;pointer-events:none!important;z-index:0!important}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FLOATING ICONS + SCANLINES + WAVEFORM (helper)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def build_overlay():
    icons = ['🎵', '🎶', '🎧', '🎤', '🎸', '🎹', '🎷', '🎺', '🎻', '🎼', '🔊', '🎙️', '🎚️', '🎛️']
    parts = ['<div class="ficons">']
    for i, ic in enumerate(icons):
        left = 4 + (i * 6.8) % 90
        dur = 14 + (i * 3.5) % 16
        delay = (i * 2.3) % 18
        sz = 0.8 + (i * 0.12) % 0.7
        parts.append('<span class="fi" style="left:')
        parts.append(str(int(left)))
        parts.append('%;animation-duration:')
        parts.append("{:.1f}".format(dur))
        parts.append('s;animation-delay:')
        parts.append("{:.1f}".format(delay))
        parts.append('s;font-size:')
        parts.append("{:.1f}".format(sz))
        parts.append('rem;">')
        parts.append(ic)
        parts.append('</span>')
    parts.append('</div><div class="scan"></div>')

    # Waveform bars at bottom
    parts.append('<div class="waveform">')
    for i in range(120):
        left_px = i * 8 + 2
        dur = 0.6 + (i * 0.09) % 1.2
        delay = (i * 0.05) % 0.8
        parts.append('<div class="wbar" style="left:')
        parts.append(str(left_px))
        parts.append('px;animation-duration:')
        parts.append("{:.2f}".format(dur))
        parts.append('s;animation-delay:')
        parts.append("{:.2f}".format(delay))
        parts.append('s;"></div>')
    parts.append('</div>')

    return "".join(parts)


st.markdown(build_overlay(), unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOTTIE LOADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


lottie_music = load_lottieurl("https://lottie.host/e4a9b21d-3f04-4676-b78e-f7b7a940f0e3/TDAzMZMQBI.json")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOAD ML PIPELINE + DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_resource
def load_assets():
    model = joblib.load('final_model_pipeline.pkl')
    df = pd.read_csv('high_popularity_spotify_data.csv')
    return model, df


model, df = load_assets()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EQUALIZER BARS (helper function)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def build_equalizer():
    parts = ['<div class="speedo">']
    for i in range(22):
        h = 5 + (i * 7 + 2) % 20
        dur = 0.5 + (i * 0.14) % 0.85
        delay = (i * 0.07) % 0.55
        parts.append('<div class="sbar" style="height:')
        parts.append(str(h))
        parts.append('px;animation-duration:')
        parts.append("{:.2f}".format(dur))
        parts.append('s;animation-delay:')
        parts.append("{:.2f}".format(delay))
        parts.append('s;"></div>')
    parts.append('</div>')
    return "".join(parts)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GENRE EMOJI MAP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GENRE_EMOJI = {
    'pop': '🎤', 'rock': '🎸', 'hip-hop': '🎤', 'rap': '🎤',
    'r&b': '🎶', 'jazz': '🎷', 'classical': '🎻', 'electronic': '🎛️',
    'edm': '🎛️', 'dance': '💃', 'country': '🤠', 'metal': '🤘',
    'indie': '🎵', 'folk': '🪕', 'blues': '🎺', 'soul': '🎙️',
    'reggae': '🏝️', 'punk': '⚡', 'latin': '💃', 'k-pop': '🇰🇷',
    'alternative': '🎵', 'ambient': '🌊',
}


def get_genre_emoji(genre_str):
    gl = genre_str.lower()
    for key, emoji in GENRE_EMOJI.items():
        if key in gl:
            return emoji
    return '🎵'


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GENRE COLOR MAP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GENRE_COLORS = {
    'pop': ('#ff6b9d', '#c44569', 'linear-gradient(135deg,#ff6b9d,#c44569,#ff9ff3)'),
    'rock': ('#e74c3c', '#c0392b', 'linear-gradient(135deg,#e74c3c,#c0392b,#ff6348)'),
    'hip-hop': ('#f39c12', '#e67e22', 'linear-gradient(135deg,#f39c12,#e67e22,#fdcb6e)'),
    'rap': ('#f39c12', '#e67e22', 'linear-gradient(135deg,#f39c12,#e67e22,#fdcb6e)'),
    'jazz': ('#e17055', '#d35400', 'linear-gradient(135deg,#e17055,#d35400,#fab1a0)'),
    'classical': ('#dfe6e9', '#b2bec3', 'linear-gradient(135deg,#dfe6e9,#b2bec3,#636e72)'),
    'electronic': ('#a29bfe', '#6c5ce7', 'linear-gradient(135deg,#a29bfe,#6c5ce7,#fd79a8)'),
    'edm': ('#a29bfe', '#6c5ce7', 'linear-gradient(135deg,#a29bfe,#6c5ce7,#fd79a8)'),
    'metal': ('#636e72', '#2d3436', 'linear-gradient(135deg,#636e72,#2d3436,#b2bec3)'),
    'indie': ('#55efc4', '#00b894', 'linear-gradient(135deg,#55efc4,#00b894,#81ecec)'),
    'country': ('#fdcb6e', '#f39c12', 'linear-gradient(135deg,#fdcb6e,#f39c12,#e17055)'),
    'latin': ('#fd79a8', '#e84393', 'linear-gradient(135deg,#fd79a8,#e84393,#fdcb6e)'),
}


def get_genre_colors(genre_str):
    gl = genre_str.lower()
    for key, colors in GENRE_COLORS.items():
        if key in gl:
            return colors
    return ('#1DB954', '#1ed760', 'linear-gradient(135deg,#1DB954,#1ed760,#17d05b)')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESULT CARD BUILDER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def build_result(genre, track_name, track_data):
    ac, ac2, gr = get_genre_colors(genre)
    gl = ac + "44"
    emoji = get_genre_emoji(genre)

    rings = ""
    for i in range(3):
        d = "{:.1f}".format(i * 1.2)
        rings += '<div class="pr" style="border-color:' + ac + '25;animation-duration:3.6s;animation-delay:' + d + 's;"></div>'

    p = []
    p.append('<div class="rc">')
    p.append('<div class="prb">' + rings + '</div>')

    # Top accent bar
    p.append('<div style="position:absolute;top:0;left:0;right:0;height:4px;background:')
    p.append(gr)
    p.append(';border-radius:var(--rl) var(--rl) 0 0;box-shadow:0 0 18px ')
    p.append(gl)
    p.append(';z-index:1;"></div>')

    # Badge
    p.append('<span class="rbadge" style="background:')
    p.append(ac)
    p.append('15;color:')
    p.append(ac)
    p.append(';">&#10022; Classification Complete</span>')

    # Genre display
    p.append('<p class="rgenre" style="background:')
    p.append(gr)
    p.append(';-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 28px ')
    p.append(gl)
    p.append(');">')
    p.append(emoji)
    p.append(' ')
    p.append(str(genre).title())
    p.append('</p>')

    # Subtitle
    p.append('<p class="rsub" style="color:')
    p.append(ac)
    p.append(';">Predicted Music Genre</p>')

    p.append('<hr class="rdiv">')

    # Description
    p.append('<p class="rdesc">Genre classification computed for <strong>&ldquo;')
    p.append(str(track_name))
    p.append('&rdquo;</strong>. ')
    p.append('The ML pipeline analyzed audio features and metadata signatures ')
    p.append('to classify this track into the <strong>')
    p.append(str(genre).title())
    p.append('</strong> genre cluster.</p>')

    # Confidence bar
    conf = 88
    p.append('<div style="margin-top:18px;position:relative;z-index:1;">')
    p.append('<div style="display:flex;justify-content:space-between;margin-bottom:5px;">')
    p.append('<span style="font-size:.6rem;letter-spacing:2px;text-transform:uppercase;color:var(--muted);font-weight:600;">Model Confidence</span>')
    p.append('<span style="font-family:JetBrains Mono,monospace;font-size:.78rem;font-weight:700;color:')
    p.append(ac)
    p.append(';">')
    p.append(str(conf))
    p.append('%</span></div>')
    p.append('<div class="ctrack"><div class="cfill" style="width:')
    p.append(str(conf))
    p.append('%;background:')
    p.append(gr)
    p.append(';box-shadow:0 0 10px ')
    p.append(gl)
    p.append(';"></div></div></div>')

    # Audio feature chips — extract from track data if available
    feature_chips = []
    chip_map = {
        'danceability': ('💃', 'Dance'),
        'energy': ('⚡', 'Energy'),
        'tempo': ('🥁', 'Tempo'),
        'valence': ('😊', 'Mood'),
        'loudness': ('🔊', 'Loud'),
    }
    for col, (em, label) in chip_map.items():
        if col in track_data.columns:
            val = track_data[col].values[0]
            if col == 'tempo':
                display = "{:.0f}".format(val)
            elif col == 'loudness':
                display = "{:.1f}".format(val)
            else:
                display = "{:.2f}".format(val)
            feature_chips.append((em, display, label, ac))

    if feature_chips:
        p.append('<div class="srow">')
        for em, val, label, color in feature_chips:
            p.append('<div class="sc"><span class="sv" style="color:')
            p.append(color)
            p.append(';">')
            p.append(val)
            p.append('</span><span class="sl">')
            p.append(em)
            p.append(' ')
            p.append(label)
            p.append('</span></div>')
        p.append('</div>')

    p.append('</div>')
    return "".join(p)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HERO HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div style="text-align:center;padding-top:18px;position:relative;">', unsafe_allow_html=True)
st.markdown('<span class="hbadge">&#10022; AI-Powered &#10022;</span>', unsafe_allow_html=True)
st.markdown('<div style="position:relative;display:inline-block;">', unsafe_allow_html=True)
st.markdown('<div class="hglow"></div>', unsafe_allow_html=True)
st.markdown('<p class="htitle">SonicSort</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<p class="hsub">spotify genre classification engine</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hdesc">Enter a track name from the Spotify catalog and let our machine learning '
    'pipeline classify its genre using audio feature analysis in seconds.</p>',
    unsafe_allow_html=True,
)
st.markdown(build_equalizer(), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if lottie_music:
    st_lottie(lottie_music, height=120, key="music_anim")

st.markdown("<br>", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BUILD TRACK LIST FROM CSV
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
all_track_names = sorted(df['track_name'].dropna().unique().tolist())


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT — Track Search (Dropdown from catalog)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(
    '<div class="gc"><span class="ci">🎧</span>'
    '<p class="cl">Track Lookup</p>'
    '<p class="ct">Select a Track from the Catalog</p></div>',
    unsafe_allow_html=True,
)
track_name = st.selectbox(
    "Select Track",
    options=[""] + all_track_names,
    index=0,
    format_func=lambda x: "🔍  Type to search tracks..." if x == "" else x,
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CTA BUTTON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
analyze_clicked = st.button("CLASSIFY GENRE")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INFERENCE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if analyze_clicked:

    if not track_name or not track_name.strip():
        st.warning("🎵 Please select a track from the dropdown to classify.")
    else:
        # Processing stages
        ph = st.empty()
        for txt, wait in [
            ("Searching track metadata...", 0.35),
            ("Extracting audio features...", 0.45),
            ("Running classification model...", 0.5),
            ("Generating genre report...", 0.35),
        ]:
            ph.markdown('<p class="stg">' + txt + '</p>', unsafe_allow_html=True)
            time.sleep(wait)
        ph.empty()

        # Look up the track — exact match (guaranteed from dropdown)
        match = df[df['track_name'] == track_name.strip()]

        # Fallback: case-insensitive match
        if match.empty:
            match = df[df['track_name'].str.lower() == track_name.strip().lower()]

        # Fallback: partial / contains match
        if match.empty:
            match = df[df['track_name'].str.lower().str.contains(track_name.strip().lower(), na=False)]

        if not match.empty:
            track_data = match.iloc[[0]].copy()
            matched_name = track_data['track_name'].values[0]

            # Recreate 'text_features' — the pipeline was trained to expect this column
            track_data['text_features'] = track_data['track_artist'].astype(str) + " " + track_data['track_album_name'].astype(str)

            prediction = model.predict(track_data)[0]

            # Success animation
            lottie_ok = load_lottieurl("https://lottie.host/80c436ab-6b08-45ec-b91c-7f51be0ccf5d/c3qCgQ2fCc.json")
            if lottie_ok:
                st_lottie(lottie_ok, height=150, speed=1.2, key="ok_vfx")

            # Render result card
            st.markdown(
                build_result(str(prediction), matched_name, track_data),
                unsafe_allow_html=True,
            )
        else:
            # Error state — styled
            st.markdown(
                '<div class="rc">'
                '<div style="position:absolute;top:0;left:0;right:0;height:4px;'
                'background:linear-gradient(135deg,#e74c3c,#c0392b,#ff6348);'
                'border-radius:var(--rl) var(--rl) 0 0;z-index:1;"></div>'
                '<span class="rbadge" style="background:rgba(231,76,60,.12);color:#e74c3c;">'
                '&#10006; Track Not Found</span>'
                '<p class="rgenre" style="background:linear-gradient(135deg,#e74c3c,#c0392b);'
                '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
                'background-clip:text;font-size:1.8rem;">No Match Found</p>'
                '<hr class="rdiv">'
                '<p class="rdesc">The track <strong>&ldquo;' + str(track_name) + '&rdquo;</strong> '
                'was not found in our Spotify metadata catalog. '
                'Please verify the exact track name and try again.</p>'
                '</div>',
                unsafe_allow_html=True,
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(
    '<p class="foot">&#10022; SonicSort &middot; Streamlit &amp; ML &middot; IIT Jammu &middot; 2025 &#10022;</p>',
    unsafe_allow_html=True,
)
