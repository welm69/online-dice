"""
Online Dice - Virtual Dice Simulator
Lancez avec : python app.py
Puis ouvrez : http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify
import random
import string

app = Flask(__name__)

# ── données ──────────────────────────────────────────────────────────────────

STREAMERS_LEFT = [
    {"name": "VIAJERO_NINJA11", "handle": "@viajero_ninja11", "live": True,  "grad": ["#FF6B6B","#C44545"]},
    {"name": "FREXX",           "handle": "@frexx180",        "live": True,  "grad": ["#4FA8E8","#2566a0"]},
    {"name": "AKEFTHEGOAT",     "handle": "@akefrblx",        "live": True,  "grad": ["#9B6BFF","#5d3bb0"]},
    {"name": "AURAZ",           "handle": "@aurazno1",        "live": True,  "grad": ["#FFB23E","#c47e10"]},
    {"name": "VINYYWS",         "handle": "@vinyyws",         "live": True,  "grad": ["#3ECF8E","#1f8a5c"]},
    {"name": "EXAMPLE",         "handle": "@xtypv1",          "live": False, "grad": ["#FF6BD6","#b0398e"]},
    {"name": "LERB",            "handle": "@lerb942",         "live": False, "grad": ["#6BCBFF","#2a7fb0"]},
]

STREAMERS_RIGHT = [
    {"name": "DEETS GAMING",  "handle": "@deets_gaming",     "live": False, "grad": ["#FF6B6B","#C44545"]},
    {"name": "ISLANDZOTT",    "handle": "@islandzott",       "live": False, "grad": ["#4FA8E8","#2566a0"]},
    {"name": "YAGU1N",        "handle": "@yagu1n3",          "live": False, "grad": ["#FFB23E","#c47e10"]},
    {"name": "NANDOX",        "handle": "@nandox.ff1",       "live": False, "grad": ["#FF6BD6","#b0398e"]},
    {"name": "KAZ",           "handle": "@kazuhiko_mayuko",  "live": False, "grad": ["#9B6BFF","#5d3bb0"]},
    {"name": "[KFG] ✦BADboy✧","handle": "@ttvvexz",         "live": False, "grad": ["#3ECF8E","#1f8a5c"]},
    {"name": "WAVY",          "handle": "@its.will1am",      "live": False, "grad": ["#6BCBFF","#2a7fb0"]},
]

COLORS_DEFAULT = [
    {"name": "Rouge",  "hex": "#E24B4A"},
    {"name": "Orange", "hex": "#EF9F27"},
    {"name": "Jaune",  "hex": "#F7D154"},
    {"name": "Vert",   "hex": "#639922"},
    {"name": "Bleu",   "hex": "#378ADD"},
    {"name": "Violet", "hex": "#7F77DD"},
]

COLORS_PASTEL = [
    {"name": "Rouge",  "hex": "#F0997B"},
    {"name": "Orange", "hex": "#FAC775"},
    {"name": "Jaune",  "hex": "#FAEEDA"},
    {"name": "Vert",   "hex": "#C0DD97"},
    {"name": "Bleu",   "hex": "#B5D4F4"},
    {"name": "Violet", "hex": "#CECBF6"},
]

COLORS_NEON = [
    {"name": "Rouge",  "hex": "#FF1744"},
    {"name": "Orange", "hex": "#FF6D00"},
    {"name": "Jaune",  "hex": "#FFEA00"},
    {"name": "Vert",   "hex": "#00E676"},
    {"name": "Bleu",   "hex": "#2979FF"},
    {"name": "Violet", "hex": "#D500F9"},
]

PALETTES = {"default": COLORS_DEFAULT, "pastel": COLORS_PASTEL, "neon": COLORS_NEON}


def rand_id(length=10):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def initials(name):
    parts = name.replace("_", " ").split()
    return "".join(p[0] for p in parts)[:2].upper()


def streamer_html(s):
    g0, g1 = s["grad"]
    ini = initials(s["name"])
    live_badge = '<span class="live">Live</span>' if s["live"] else ""
    return f"""
    <div class="streamer">
      <div class="avatar" style="background:linear-gradient(135deg,{g0},{g1})">
        {ini}{live_badge}
      </div>
      <div>
        <div class="sname">{s["name"]} <span class="badge">✓</span></div>
        <div class="handle">{s["handle"]}</div>
      </div>
    </div>"""


# ── template HTML ─────────────────────────────────────────────────────────────

PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Online Dice - Virtual Dice Simulator</title>
<style>
/* ── reset ── */
*{box-sizing:border-box;margin:0;padding:0;}
html,body{overflow-x:hidden;}

/* ── fond bleu avec motif de dés ── */
body{
  font-family:'Segoe UI',Arial,sans-serif;
  background:#4FA8E8;
  color:#1a1a1a;
  padding-bottom:60px;
  position:relative;
  min-height:100vh;
}
body::before{
  content:'';
  position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='130' height='130'%3E%3Crect x='10' y='10' width='42' height='42' rx='8' fill='none' stroke='rgba(255,255,255,0.22)' stroke-width='2.5'/%3E%3Ccircle cx='21' cy='21' r='3.5' fill='rgba(255,255,255,0.22)'/%3E%3Ccircle cx='41' cy='41' r='3.5' fill='rgba(255,255,255,0.22)'/%3E%3Ccircle cx='41' cy='21' r='3.5' fill='rgba(255,255,255,0.22)'/%3E%3Ccircle cx='21' cy='41' r='3.5' fill='rgba(255,255,255,0.22)'/%3E%3Ccircle cx='31' cy='31' r='3.5' fill='rgba(255,255,255,0.22)'/%3E%3Crect x='78' y='78' width='42' height='42' rx='8' fill='none' stroke='rgba(255,255,255,0.22)' stroke-width='2.5'/%3E%3Ccircle cx='89' cy='89' r='3.5' fill='rgba(255,255,255,0.22)'/%3E%3Ccircle cx='109' cy='89' r='3.5' fill='rgba(255,255,255,0.22)'/%3E%3Ccircle cx='89' cy='109' r='3.5' fill='rgba(255,255,255,0.22)'/%3E%3Ccircle cx='109' cy='109' r='3.5' fill='rgba(255,255,255,0.22)'/%3E%3Crect x='78' y='5' width='32' height='32' rx='6' fill='none' stroke='rgba(255,255,255,0.15)' stroke-width='2'/%3E%3Ccircle cx='94' cy='21' r='3' fill='rgba(255,255,255,0.15)'/%3E%3Crect x='5' y='80' width='32' height='32' rx='6' fill='none' stroke='rgba(255,255,255,0.15)' stroke-width='2'/%3E%3Ccircle cx='21' cy='96' r='3' fill='rgba(255,255,255,0.15)'/%3E%3C/svg%3E");
  background-size:130px 130px;
}
body>*{position:relative;z-index:1;}

/* ── bouton son ── */
.sound-toggle{
  position:fixed;top:10px;right:10px;
  background:white;border:none;border-radius:20px;
  padding:8px 14px;font-size:12px;font-weight:bold;
  cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,0.2);z-index:200;
}

/* ── bannière publicitaire Shine ── */
.shine-ad{
  background:#FCEFA1;border-bottom:2px solid #e0d27a;
  padding:12px 24px;display:flex;align-items:center;gap:16px;
  flex-wrap:wrap;
}
.shine-ad .brand{font-weight:900;font-size:15px;letter-spacing:-0.5px;}
.shine-ad .brand span{font-size:11px;vertical-align:super;margin-right:2px;}
.shine-ad .tagline{font-size:21px;font-style:italic;font-weight:400;}
.shine-ad .tagline b{font-style:normal;font-weight:900;}
.shine-ad .sub{font-size:12px;color:#555;}
.shine-ad .cta-btn{
  margin-left:auto;background:#0d2b24;color:white;
  border:none;padding:10px 20px;border-radius:6px;
  font-weight:bold;font-size:13px;cursor:pointer;white-space:nowrap;
}

/* ── logo ── */
.logo-wrap{text-align:center;padding:18px 10px 6px;}
.logo-wrap h1{
  font-size:68px;font-family:Georgia,'Times New Roman',serif;
  font-weight:900;letter-spacing:3px;
  color:#FFD400;
  -webkit-text-stroke:3px #B8860B;
  text-shadow:0 3px 0 #B8860B,0 6px 10px rgba(0,0,0,0.3);
  line-height:1;
}
.logo-wrap .sub-title{
  color:white;font-weight:700;letter-spacing:4px;font-size:14px;
  text-shadow:2px 2px 0 #2a6fa0;margin-top:2px;
}

/* ── carte Google Maps style ── */
.biz-card{
  max-width:740px;margin:18px auto;background:white;
  border-radius:10px;overflow:hidden;
  box-shadow:0 2px 8px rgba(0,0,0,0.18);
}
.biz-card .bc-top{
  padding:16px 20px 12px;text-align:center;border-bottom:1px solid #eee;
}
.biz-card .bc-pin{
  width:28px;height:28px;border-radius:50%;background:#d93025;color:white;
  display:inline-flex;align-items:center;justify-content:center;
  font-size:13px;margin-bottom:6px;
}
.biz-card .bc-name{font-weight:700;font-size:13.5px;color:#1a1a1a;}
.biz-card .bc-stars{color:#f5a623;font-size:13px;margin-top:4px;}
.biz-card .bc-stars span{color:#777;font-size:12px;}
.biz-card .bc-source{font-size:11px;color:#1a73e8;margin-top:2px;}
.biz-card .bc-body{
  display:flex;align-items:center;gap:14px;
  padding:14px 20px;
}
.biz-card .bc-icon{font-size:28px;flex-shrink:0;}
.biz-card .bc-status{color:#2e9e3e;font-weight:700;font-size:13px;margin-right:6px;}
.biz-card .bc-hours{font-size:13px;color:#333;}
.biz-card .bc-addr{font-size:12px;color:#666;margin-top:3px;}
.biz-card .bc-foot{text-align:center;padding:0 20px 16px;}
.biz-card .bc-foot button{
  background:#4F6FE8;color:white;border:none;
  padding:10px 0;border-radius:6px;font-weight:700;
  cursor:pointer;width:100%;max-width:340px;font-size:14px;
}

/* ── layout 3 colonnes ── */
.layout{
  display:flex;gap:18px;padding:0 20px 24px;
  max-width:1380px;margin:0 auto;align-items:flex-start;
}
.sidebar{
  flex:0 0 230px;background:#5BB8F5;border-radius:10px;padding:14px;
}
.sidebar h3{
  text-align:center;color:white;letter-spacing:1px;
  text-shadow:1px 1px 0 #2a6fa0;font-size:13px;
  margin-bottom:12px;font-weight:700;
}
.streamer{
  display:flex;align-items:center;gap:10px;
  background:rgba(255,255,255,0.18);border-radius:8px;
  padding:8px;margin-bottom:7px;
}
.avatar{
  width:42px;height:42px;border-radius:50%;
  position:relative;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  color:white;font-size:12px;font-weight:900;
  border:2px solid rgba(255,255,255,0.5);
}
.live{
  position:absolute;bottom:-5px;left:50%;transform:translateX(-50%);
  background:#e23;color:white;font-size:8px;font-weight:700;
  padding:1px 5px;border-radius:3px;white-space:nowrap;
}
.sname{color:white;font-weight:700;font-size:12.5px;display:flex;align-items:center;gap:4px;}
.badge{
  width:13px;height:13px;border-radius:50%;
  background:#4F6FE8;display:inline-flex;
  align-items:center;justify-content:center;font-size:8px;color:white;
}
.handle{color:#ddeeff;font-size:11px;}

/* ── panneau central ── */
.main{
  flex:1;background:#5BB8F5;border-radius:10px;
  padding:22px;text-align:center;position:relative;overflow:hidden;
}
.main h2{
  color:white;text-shadow:2px 2px 0 #2a6fa0;
  letter-spacing:2px;font-size:26px;margin-bottom:18px;
  font-weight:900;
}

/* ── selects ── */
.controls{display:flex;gap:10px;justify-content:center;margin-bottom:22px;flex-wrap:wrap;}
.controls select{
  background:white;border:none;border-radius:6px;
  padding:10px 14px;font-weight:700;color:#2a6fa0;
  cursor:pointer;min-width:130px;font-size:13px;
}

/* ── zone dés ── */
#diceStage{position:relative;min-height:140px;margin-bottom:16px;}
#diceArea{
  display:flex;flex-wrap:wrap;gap:16px;
  justify-content:center;align-items:center;
  transition:opacity 0.2s ease;
}
#diceArea.zoom-out{opacity:0;}
.die{
  width:90px;height:90px;border-radius:16px;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 5px 0 rgba(0,0,0,0.22),inset 0 0 0 3px rgba(255,255,255,0.35);
}
.pip{
  width:20px;height:20px;border-radius:50%;
  background:white;box-shadow:0 0 0 2px rgba(0,0,0,0.08);
}

/* ── overlay rolling "GOOD LUCK!" ── */
.rolling-overlay{
  position:absolute;inset:0;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;
  background:transparent;
  opacity:0;pointer-events:none;transition:opacity 0.2s ease;
  z-index:10;
}
.rolling-overlay.show{opacity:1;}

/* Texte GOOD LUCK! style cartoon */
.good-luck-text{
  font-family:Georgia,'Times New Roman',serif;
  font-size:38px;font-weight:900;letter-spacing:3px;
  color:white;
  -webkit-text-stroke:2px #2a7fc0;
  text-shadow:0 3px 0 #2a7fc0,0 5px 10px rgba(0,0,0,0.2);
  animation:bounceTxt 0.4s ease-in-out infinite alternate;
}
@keyframes bounceTxt{
  0%{transform:scale(1) translateY(0);}
  100%{transform:scale(1.04) translateY(-4px);}
}

/* Dés blancs/gris qui s'agitent */
.ghost-dice{display:flex;gap:14px;align-items:center;}
.ghost-die{
  width:80px;height:80px;border-radius:16px;
  background:#e0e0e0;
  border:4px solid white;
  box-shadow:0 4px 12px rgba(0,0,0,0.15);
  display:flex;align-items:center;justify-content:center;
}
.ghost-die::after{
  content:'';width:14px;height:14px;border-radius:50%;background:#bbb;display:block;
}
.ghost-die:nth-child(1){animation:shakeDie1 0.18s ease-in-out infinite alternate;}
.ghost-die:nth-child(2){animation:shakeDie2 0.18s ease-in-out infinite alternate;animation-delay:0.06s;}
.ghost-die:nth-child(3){animation:shakeDie3 0.18s ease-in-out infinite alternate;animation-delay:0.12s;}
.ghost-die:nth-child(4){animation:shakeDie1 0.18s ease-in-out infinite alternate;animation-delay:0.04s;}
.ghost-die:nth-child(5){animation:shakeDie2 0.18s ease-in-out infinite alternate;animation-delay:0.08s;}
@keyframes shakeDie1{0%{transform:rotate(-6deg) translateY(0);}100%{transform:rotate(6deg) translateY(-6px);}}
@keyframes shakeDie2{0%{transform:rotate(5deg) translateY(-4px);}100%{transform:rotate(-5deg) translateY(4px);}}
@keyframes shakeDie3{0%{transform:rotate(-4deg) translateY(3px);}100%{transform:rotate(7deg) translateY(-5px);}}

/* ── game id ── */
.gameid{color:#eaf6ff;font-size:13px;margin-bottom:14px;}
.gameid a{color:white;text-decoration:underline;cursor:pointer;}

/* ── barre avertissement ── */
.warn-bar{
  background:#fff8e1;border:1px solid #ffe082;border-radius:6px;
  padding:9px 13px;font-size:13px;color:#333;
  margin-bottom:14px;text-align:left;
}
.warn-bar b{color:#e24b4a;}
.warn-bar a{color:#e24b4a;font-weight:700;text-decoration:underline;cursor:pointer;}

/* ── popup bonus ── */
.bonus-popup{
  background:white;border-radius:8px;padding:20px;
  max-width:400px;margin:0 auto 16px;
  box-shadow:0 2px 12px rgba(0,0,0,0.18);display:none;
}
.bonus-popup.show{display:block;animation:popIn 0.3s ease;}
@keyframes popIn{0%{transform:scale(0.85);opacity:0;}100%{transform:scale(1);opacity:1;}}
.bonus-popup .bp-ad-label{
  font-size:10px;color:#aaa;text-align:right;margin-bottom:4px;
}
.bonus-popup h4{margin:0 0 10px;font-size:18px;}
.bonus-popup p{margin:5px 0;font-size:14px;color:#333;}
.bonus-popup .robux{color:#2e9e3e;font-weight:700;}
.bonus-popup .bp-actions{display:flex;gap:10px;justify-content:center;margin-top:14px;}
.bonus-popup button{
  border:none;padding:10px 28px;border-radius:6px;
  font-weight:700;cursor:pointer;color:white;font-size:14px;
}
.bonus-popup .btn-oui{background:#2e9e3e;}
.bonus-popup .btn-non{background:#e24b4a;}

/* ── bouton roll ── */
#rollBtn{
  background:#FFD400;color:#1a1a1a;border:none;
  width:100%;max-width:520px;padding:16px;
  font-size:18px;font-weight:900;letter-spacing:1px;
  border-radius:8px;cursor:pointer;
  box-shadow:0 4px 0 #c9a800;transition:transform 0.05s;
}
#rollBtn:active{transform:translateY(2px);box-shadow:0 2px 0 #c9a800;}
#rollBtn:disabled{opacity:0.7;cursor:default;}

/* ── légende couleurs ── */
.legend{
  margin-top:16px;background:rgba(255,255,255,0.85);
  border-radius:8px;padding:11px;font-size:13px;color:#333;
}
.swatch{
  display:inline-block;width:10px;height:10px;
  border-radius:50%;margin:0 4px 0 10px;vertical-align:middle;
}

/* ── footer ── */
footer.bar{
  position:fixed;bottom:0;left:0;right:0;
  background:#1a1a1a;padding:8px 16px;
  display:flex;justify-content:flex-end;gap:10px;z-index:200;
}
footer.bar button{
  background:#333;color:white;border:none;
  padding:8px 16px;border-radius:6px;font-size:13px;cursor:pointer;
}

@media(max-width:800px){
  .layout{flex-direction:column;}
  .sidebar{flex:none;width:100%;}
  .logo-wrap h1{font-size:44px;}
}
</style>
</head>
<body>

<button class="sound-toggle" id="soundToggle">🔊 Son : ON</button>

<!-- Bannière Shine -->
<div class="shine-ad">
  <span class="brand"><span>⌃</span> Shine</span>
  <span class="tagline">Compte pro <b>100% en ligne</b></span>
  <span class="sub">Choisi par +150 000 TPE et indépendant·es</span>
  <button class="cta-btn">Ouvrir mon compte</button>
</div>

<!-- Logo -->
<div class="logo-wrap">
  <h1>ONLINE DICE</h1>
  <div class="sub-title">VIRTUAL DICE SIMULATOR</div>
</div>

<!-- Carte Google Maps style -->
<div class="biz-card">
  <div class="bc-top">
    <div class="bc-pin">📍</div>
    <div class="bc-name">Gouret SAS · Électricien · Plombier · Chauffagiste · Solaire/Photovoltaïque Le Cellier (44)</div>
    <div class="bc-stars">★★★★☆ 4.7 <span>(11)</span></div>
    <div class="bc-source">GOURET | Le Cellier</div>
  </div>
  <div class="bc-body">
    <span class="bc-icon">⛅</span>
    <div>
      <span class="bc-status">OUVERT</span>
      <span class="bc-hours">08:00–17:30</span>
      <div class="bc-addr">35 Rue de la Piarderie, Le Cellier</div>
    </div>
  </div>
  <div class="bc-foot">
    <button>En savoir plus</button>
  </div>
</div>

<!-- Layout 3 colonnes -->
<div class="layout">

  <!-- Sidebar gauche -->
  <aside class="sidebar">
    <h3>OUR TOP STREAMERS</h3>
    {{ streamers_left | safe }}
  </aside>

  <!-- Panneau central -->
  <main class="main">
    <h2>ROLL COLOR DICE</h2>

    <div class="controls">
      <select id="diceCount"></select>
      <select id="diceType">
        <option value="color">COLOR DICE</option>
      </select>
      <select id="theme">
        <option value="default">SELECT THEME</option>
        <option value="pastel">PASTEL THEME</option>
        <option value="neon">NEON THEME</option>
      </select>
    </div>

    <div id="diceStage">
      <div id="diceArea"></div>
      <div class="rolling-overlay" id="rollingOverlay">
        <div class="good-luck-text">GOOD LUCK!</div>
        <div class="ghost-dice" id="ghostDice">
          <div class="ghost-die"></div>
          <div class="ghost-die"></div>
          <div class="ghost-die"></div>
        </div>
      </div>
    </div>

    <p class="gameid">Game ID: <span id="gameId">{{ game_id }}</span> – <a id="verifyLink">Verify</a></p>

    <div class="warn-bar">
      ⚠️ <b>Twizzy @twizzyxcvz</b> is scamming/rigging. <a id="proofLink">Click to see proof</a>
    </div>

    <!-- Popup bonus (affiché tous les 4 lancers) -->
    <div class="bonus-popup" id="bonusPopup">
      <div class="bp-ad-label">▲ Publicité</div>
      <h4>🎉 Génial !</h4>
      <p>Vous avez reçu une<br><span class="robux">Carte ROBUX de 1000 $</span><br>en cadeau !</p>
      <p><strong>Souhaitez-vous en profiter ?</strong></p>
      <div class="bp-actions">
        <button class="btn-oui" id="bonusOui">OUI</button>
        <button class="btn-non" id="bonusNon">NON</button>
      </div>
    </div>

    <button id="rollBtn">ROLL AGAIN !</button>

    <div class="legend">
      Possible colors are:
      {% for c in colors %}
      <span class="swatch" style="background:{{ c.hex }}"></span><b>{{ c.name }}</b>
      {% endfor %}
    </div>
  </main>

  <!-- Sidebar droite -->
  <aside class="sidebar">
    <h3>OUR TOP STREAMERS</h3>
    {{ streamers_right | safe }}
  </aside>

</div>

<footer class="bar">
  <button>Follow us</button>
  <button>Join server</button>
</footer>

<script>
/* ══ Audio ══════════════════════════════════════════════════════════════════ */
let audioCtx = null;
let soundOn  = true;

function getCtx(){
  if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  return audioCtx;
}

/* Son de dé qui roule : bruit de cliquetis rapides */
function playRollSound(){
  if(!soundOn) return;
  const ctx = getCtx();
  // Bruit blanc court = son de dés qui roulent
  const buf = ctx.createBuffer(1, ctx.sampleRate * 0.06, ctx.sampleRate);
  const data = buf.getChannelData(0);
  for(let i=0;i<data.length;i++) data[i] = (Math.random()*2-1) * (1 - i/data.length);
  const src = ctx.createBufferSource();
  src.buffer = buf;
  const gain = ctx.createGain();
  gain.gain.value = 0.18;
  // Filtre passe-bande pour sonner "claquement de dé"
  const filter = ctx.createBiquadFilter();
  filter.type = 'bandpass';
  filter.frequency.value = 800 + Math.random()*400;
  filter.Q.value = 0.8;
  src.connect(filter).connect(gain).connect(ctx.destination);
  src.start();
}

/* Son de victoire */
function playWinChime(){
  if(!soundOn) return;
  const ctx = getCtx();
  [523.25,659.25,783.99,1046.5].forEach((freq,i)=>{
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine'; osc.frequency.value = freq;
    gain.gain.value = 0.0001;
    osc.connect(gain).connect(ctx.destination);
    const t = ctx.currentTime + i*0.13;
    osc.start(t);
    gain.gain.linearRampToValueAtTime(0.1, t+0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, t+0.4);
    osc.stop(t+0.45);
  });
}

document.getElementById('soundToggle').addEventListener('click', function(){
  soundOn = !soundOn;
  this.textContent = soundOn ? '🔊 Son : ON' : '🔇 Son : OFF';
});

/* ══ Palettes ═══════════════════════════════════════════════════════════════ */
const palettes = {
  default: {{ colors_default | tojson }},
  pastel:  {{ colors_pastel  | tojson }},
  neon:    {{ colors_neon    | tojson }}
};

/* ══ Sélect nombre de dés ═══════════════════════════════════════════════════ */
const diceSelect = document.getElementById('diceCount');
for(let i=1;i<=20;i++){
  const opt = document.createElement('option');
  opt.value = i;
  opt.textContent = i + (i===1 ? ' DIE' : ' DICE');
  if(i===3) opt.selected = true;
  diceSelect.appendChild(opt);
}

/* ══ Variables globales ══════════════════════════════════════════════════════ */
let rollCount = 0;
let rollInterval = null;
const diceArea       = document.getElementById('diceArea');
const rollBtn        = document.getElementById('rollBtn');
const gameIdSpan     = document.getElementById('gameId');
const rollingOverlay = document.getElementById('rollingOverlay');
const ghostDice      = document.getElementById('ghostDice');
const bonusPopup     = document.getElementById('bonusPopup');

/* ══ Dessin des dés ══════════════════════════════════════════════════════════ */
function buildDice(count, palette){
  diceArea.innerHTML = '';
  for(let i=0;i<count;i++){
    const c = palette[Math.floor(Math.random()*palette.length)];
    const die = document.createElement('div');
    die.className = 'die';
    die.style.background = c.hex;
    die.title = c.name;
    const pip = document.createElement('div');
    pip.className = 'pip';
    die.appendChild(pip);
    diceArea.appendChild(die);
  }
}

/* Met à jour le nombre de ghost-dés pendant le rolling */
function setGhostDice(count){
  ghostDice.innerHTML = '';
  const shown = Math.min(count, 5); // max 5 affichés
  for(let i=0;i<shown;i++){
    const d = document.createElement('div');
    d.className = 'ghost-die';
    ghostDice.appendChild(d);
  }
}

/* ══ Lancer ══════════════════════════════════════════════════════════════════ */
async function roll(){
  const count   = parseInt(diceSelect.value, 10);
  const palette = palettes[document.getElementById('theme').value] || palettes.default;

  rollBtn.disabled = true;
  rollBtn.textContent = 'ROLLING...';
  bonusPopup.classList.remove('show');

  // Afficher les ghost dés correspondant au nombre choisi
  setGhostDice(count);

  // Cacher les vrais dés, montrer l'overlay
  diceArea.classList.add('zoom-out');
  rollingOverlay.classList.add('show');

  // Sons de cliquetis pendant le rolling
  rollInterval = setInterval(playRollSound, 100);

  // Appel API Flask pour le Game ID
  let newId = gameIdSpan.textContent;
  try {
    const res  = await fetch('/api/roll?count=' + count);
    const data = await res.json();
    newId = data.game_id;
  } catch(e){}

  setTimeout(()=>{
    clearInterval(rollInterval);

    buildDice(count, palette);
    gameIdSpan.textContent = newId;

    rollingOverlay.classList.remove('show');
    diceArea.classList.remove('zoom-out');

    rollBtn.disabled = false;
    rollBtn.textContent = 'ROLL AGAIN !';

    rollCount++;
    if(rollCount % 4 === 0){ bonusPopup.classList.add('show'); playWinChime(); }
  }, 1200);
}

/* ══ Événements ══════════════════════════════════════════════════════════════ */
document.getElementById('bonusOui').addEventListener('click', ()=> bonusPopup.classList.remove('show'));
document.getElementById('bonusNon').addEventListener('click', ()=> bonusPopup.classList.remove('show'));
document.getElementById('verifyLink').addEventListener('click', ()=>{
  alert('Game ID : ' + gameIdSpan.textContent + '\\nCe tirage a été généré côté serveur Python (Flask).');
});
document.getElementById('proofLink').addEventListener('click', e=>{
  e.preventDefault();
  alert('Élément décoratif de démonstration.');
});
rollBtn.addEventListener('click', roll);
diceSelect.addEventListener('change', roll);
document.getElementById('theme').addEventListener('change', roll);

/* ══ Premier lancer automatique ══════════════════════════════════════════════ */
roll();
</script>
</body>
</html>
"""

# ── routes Flask ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    sl_html = "".join(streamer_html(s) for s in STREAMERS_LEFT)
    sr_html = "".join(streamer_html(s) for s in STREAMERS_RIGHT)
    return render_template_string(
        PAGE,
        streamers_left  = sl_html,
        streamers_right = sr_html,
        game_id         = rand_id(),
        colors          = COLORS_DEFAULT,
        colors_default  = COLORS_DEFAULT,
        colors_pastel   = COLORS_PASTEL,
        colors_neon     = COLORS_NEON,
    )


@app.route("/api/roll")
def api_roll():
    """Génère un Game ID unique côté serveur."""
    return jsonify({"game_id": rand_id(10)})


# ── point d'entrée ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  Online Dice – serveur Flask démarré")
    print("  Ouvrez : http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
