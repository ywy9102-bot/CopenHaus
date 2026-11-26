#!/usr/bin/env python3
"""2F·3F 인덕션, GF·2F·3F 세탁기·건조기(한 조작부) 그림을 5개 언어로 만드는 스크립트.

원본: 호스트가 준 A5 안내 PDF 두 장(CopenHaus_induction_2FL_3FL.pdf, CopenHaus_washer_dryer_GF__2F.pdf).
그림 속 글자만 언어별로 바꾸고, 번호·배치는 PDF와 똑같이 둬요.

쓰는 법 (저장소 맨 위에서, 글꼴 원본이 tools/.font-src/ 에 있어야 해요 → build_fonts.py가 내려받음):
    python3 tools/diagrams_floor.py
결과: img/induction-23.png, img/washer-dryer.png 와 img/<언어>/ 아래 같은 이름 파일
"""
import os, json, pathlib, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
FS = ROOT / 'tools' / '.font-src'
FONT = {'ko': 'NotoSansKR', 'en': 'NotoSansKR', 'ja': 'NotoSansJP', 'zh-hans': 'NotoSansSC', 'zh-hant': 'NotoSansTC'}
OUTDIR = {'ko': 'img', 'en': 'img/en', 'ja': 'img/ja', 'zh-hans': 'img/zh-hans', 'zh-hant': 'img/zh-hant'}

T = {
  'timer':  {'ko': '타이머', 'en': 'Timer', 'ja': 'タイマー', 'zh-hans': '定时', 'zh-hant': '定時'},
  'heat':   {'ko': '화력', 'en': 'Heat', 'ja': '火力', 'zh-hans': '火力', 'zh-hant': '火力'},
  'dryer':  {'ko': '건조기', 'en': 'Dryer', 'ja': '乾燥機', 'zh-hans': '烘干机', 'zh-hant': '烘乾機'},
  'washer': {'ko': '세탁기', 'en': 'Washer', 'ja': '洗濯機', 'zh-hans': '洗衣机', 'zh-hant': '洗衣機'},
  'rinse':  {'ko': '헹굼횟수', 'en': 'Rinses', 'ja': 'すすぎ回数', 'zh-hans': '漂洗次数', 'zh-hant': '漂洗次數'},
  'extra':  {'ko': '부가기능', 'en': 'Options', 'ja': 'オプション', 'zh-hans': '附加功能', 'zh-hant': '附加功能'},
  'topc':   {'ko': '<b>건조기</b> 터치 → 위 칸이 건조기로 작동해요', 'en': 'Tap <b>Dryer</b> → the top unit runs as the dryer',
             'ja': '<b>乾燥機</b>をタッチ → 上段が乾燥機として作動', 'zh-hans': '点触<b>烘干机</b> → 上层作为烘干机运行', 'zh-hant': '點觸<b>烘乾機</b> → 上層作為烘乾機運轉'},
  'botc':   {'ko': '<b>세탁기</b> 터치 → 아래 칸이 세탁기로 작동해요', 'en': 'Tap <b>Washer</b> → the bottom unit runs as the washer',
             'ja': '<b>洗濯機</b>をタッチ → 下段が洗濯機として作動', 'zh-hans': '点触<b>洗衣机</b> → 下层作为洗衣机运行', 'zh-hant': '點觸<b>洗衣機</b> → 下層作為洗衣機運轉'},
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fbf7ef;font-family:F,sans-serif;color:#2f3a2c}
.wrap{width:1000px;padding:0;background:#fbf7ef;display:grid;gap:18px}
.box{background:#f4ecdd;border-radius:28px;padding:34px 40px;position:relative}
.n{position:absolute;width:44px;height:44px;border-radius:50%;background:#6b8160;border:3px solid #fdfcf4;color:#fdfcf4;font-weight:700;font-size:22px;display:grid;place-items:center;transform:translate(-50%,-50%);z-index:3}
.n.dk{border-color:#fdfcf4}
.ln{position:absolute;background:#9fb38f;z-index:2}
.dot{position:absolute;width:9px;height:9px;border-radius:50%;background:#e9e3d2;transform:translate(-50%,-50%);z-index:3}
/* induction */
.ip{position:relative;height:300px;background:#3f4b3a;border-radius:30px}
.ip .sep{position:absolute;left:50%;top:6px;width:2px;height:90px;background:#6f7a66}
.ip .lab{position:absolute;color:#e9e3d2;font-size:17px;transform:translateX(-50%);white-space:nowrap}
.ip .dig{position:absolute;color:#e5bc80;font:700 58px/1 'DejaVu Sans Mono',monospace;transform:translateX(-50%);letter-spacing:2px}
.ip .btn{position:absolute;border:2.5px solid #e9e3d2;border-radius:14px;color:#e9e3d2;display:flex;align-items:center;justify-content:space-around;font-size:34px;line-height:1}
.ip svg{stroke:#e9e3d2;fill:none;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
/* washer-dryer */
.top{display:grid;grid-template-columns:170px 1fr;gap:40px;align-items:center}
.unit{width:170px;border:3px solid #6b8160;border-radius:18px;overflow:hidden;background:#fdfcf4}
.unit .u1{height:78px;background:#dfe6d6;display:grid;place-items:center;border-bottom:3px solid #6b8160}
.unit .u1 span{width:58px;height:58px;border-radius:50%;border:2.5px solid #6b8160;background:#fdfcf4;display:grid;place-items:center;font-size:13px;font-weight:700}
.unit .u2{height:110px;display:grid;place-items:center}
.unit .u2 i{width:72px;height:72px;border-radius:50%;border:3px solid #9fb38f;display:grid;place-items:center}
.unit .u2 i::after{content:'';width:48px;height:48px;border-radius:50%;border:2.5px solid #c9d3bf}
.calls{display:grid;gap:26px}
.call{position:relative;border-radius:99px;padding:16px 26px;font-size:22px;text-align:center;border:2px solid #c9d3bf}
.call.a{background:#dfe6d6}
.call.b{background:#f1f3ec}
.call::before{content:'';position:absolute;left:-42px;top:50%;width:40px;height:2px;background:#6b8160}
.call::after{content:'';position:absolute;left:-46px;top:50%;width:10px;height:10px;margin-top:-4px;border-radius:50%;background:#6b8160}
.wp{position:relative;height:250px;background:#fdfcf4;border:3px solid #8a9a7c;border-radius:26px}
.wp svg{stroke:#3f4b3a;fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.wp .sel{position:absolute;left:120px;top:58px;width:150px;text-align:center;font-weight:700;font-size:22px;line-height:1.2}
.wp .sel hr{border:0;border-top:2.5px solid #3f4b3a;margin:16px 0}
.wp .dial{position:absolute;left:300px;top:50px;width:120px;height:120px;border-radius:50%;background:#dfe6d6;display:grid;place-items:center}
.wp .dial::after{content:'';width:92px;height:92px;border-radius:50%;background:#fdfcf4;border:2px solid #c9d3bf}
.wp .disp{position:absolute;left:520px;top:42px;width:310px;height:120px;background:#3f4b3a;border-radius:12px;color:#fdfcf4;padding:18px 18px}
.wp .disp b{font-size:26px;font-family:'DejaVu Sans',sans-serif}
.wp .disp small{display:block;font-size:11.5px;opacity:.85;margin-top:12px;font-family:'DejaVu Sans',sans-serif}
.wp .disp .v{position:absolute;right:18px;top:44px;font:400 28px/1 'DejaVu Sans',sans-serif;word-spacing:22px}
.wp .row{position:absolute;right:66px;top:178px;display:flex;align-items:center;gap:8px;font-size:20px;white-space:nowrap}
.ni{display:inline-grid;place-items:center;width:40px;height:40px;border-radius:50%;background:#6b8160;border:3px solid #fdfcf4;color:#fdfcf4;font-weight:700;font-size:20px;margin-right:10px}
"""

def num(x, y, n):
    return f'<span class="n" style="left:{x}px;top:{y}px">{n}</span>'

def vline(x, y1, y2):
    return f'<span class="ln" style="left:{x-1.5}px;top:{y1}px;width:3px;height:{y2-y1}px"></span><span class="dot" style="left:{x}px;top:{y1}px"></span>'

def induction(l):
    # 조작부(PDF와 같은 배치): 5 타이머 표시, 8 화력 표시 / 1 잠금, 2 −, 3 ▶II, 4 +, 6 −, 7 +, 9 전원
    W = 920  # 패널 폭
    xs = {1: 140, 2: 255, 3: 345, 4: 435, 6: 560, 7: 655, 9: 805}
    p = []
    p.append('<div class="ip">')
    p.append('<span class="sep" style="left:470px"></span>')
    p.append(f'<span class="lab" style="left:345px;top:118px">{T["timer"][l]}</span><span class="dig" style="left:345px;top:150px">88</span>')
    p.append(f'<span class="lab" style="left:605px;top:118px">{T["heat"][l]}</span><span class="dig" style="left:605px;top:150px">8</span>')
    # 버튼
    p.append('<span class="btn" style="left:108px;top:222px;width:64px;height:58px"><svg width="26" height="30" viewBox="0 0 26 30"><rect x="3" y="13" width="20" height="15" rx="3" fill="#e9e3d2"/><path d="M7 13V9a6 6 0 0112 0v4"/></svg></span>')
    p.append('<span class="btn" style="left:220px;top:222px;width:250px;height:58px"><span>−</span><svg width="38" height="26" viewBox="0 0 38 26"><path d="M4 5v16M10 5v16" /><path d="M17 4l16 9-16 9z" fill="#e9e3d2"/></svg><span>+</span></span>')
    p.append('<span class="btn" style="left:525px;top:222px;width:165px;height:58px"><span>−</span><span>+</span></span>')
    p.append('<span class="btn" style="left:772px;top:222px;width:66px;height:58px"><svg width="30" height="32" viewBox="0 0 30 32"><path d="M15 3v13"/><path d="M8 8a11 11 0 1014 0"/></svg></span>')
    p.append('</div>')
    marks = ''
    # 아래 번호(패널 기준 좌표 + box padding)
    for n, x in xs.items():
        marks += vline(x + 40, 34 + 290, 34 + 370) + num(x + 40, 34 + 378, n)
    # 위 번호 5, 8 (표시창)
    for x, n in ((345, 5), (605, 8)):  # 위 번호: 표시창 라벨 위에서 끝나요
        marks += f'<span class="ln" style="left:{x+40-1.5}px;top:{34+60}px;width:3px;height:40px"></span><span class="dot" style="left:{x+40}px;top:{34+100}px"></span>' + num(x + 40, 34 + 46, n)
    return f'<div class="wrap"><div class="box" style="height:{34+300+150}px">{"".join(p)}{marks}</div></div>'

def washer_dryer(l):
    top = f'''<div class="box"><div class="top"><div class="unit"><div class="u1"><span>{T["dryer"][l]}</span></div><div class="u2"><i></i></div></div>
<div class="calls"><div class="call a">{T["topc"][l]}</div><div class="call b">{T["botc"][l]}</div></div></div></div>'''
    pw = '<div class="wp">'
    pw += '<svg style="position:absolute;left:38px;top:90px" width="40" height="44" viewBox="0 0 40 44"><path d="M20 4v18"/><path d="M10 11a15 15 0 1020 0"/></svg>'
    pw += f'<div class="sel"><div>{T["dryer"][l]}</div><hr><div>{T["washer"][l]}</div></div>'
    pw += '<div class="dial"></div>'
    play = '<svg width="46" height="34" viewBox="0 0 46 34"><path d="M5 5l18 12-18 12z"/><path d="M31 6v22M39 6v22"/></svg>'
    pw += f'<span style="position:absolute;left:442px;top:52px">{play}</span><span style="position:absolute;left:442px;top:128px">{play}</span>'
    pw += '<div class="disp"><b>Normal</b><small>Time set based on load</small><span class="v">47 7 4</span></div>'
    pw += '<svg style="position:absolute;left:856px;top:78px" width="40" height="52" viewBox="0 0 40 52"><path d="M10 6a14 20 0 000 40M30 6a14 20 0 010 40"/><rect x="14" y="12" width="12" height="28" rx="3"/></svg>'
    pw += (f'<div class="row"><b>{T["rinse"][l]}</b><span class="ni">7</span><b>{T["extra"][l]}</b><span class="ni">8</span></div>')
    # 번호
    pw += num(98, 78, 1) + num(290, 88, 2) + num(408, 62, 3) + num(506, 58, 4) + num(506, 150, 5) + num(862, 46, 6) + num(890, 150, 9)
    pw += '</div>'
    return f'<div class="wrap">{top}<div class="box" style="padding:30px 40px">{pw}</div></div>'

def page(l, body):
    ff = ''.join(f"@font-face{{font-family:F;src:url('file://{FS}/{FONT[l]}-{w}.ttf');font-weight:{w}}}" for w in (400, 700))
    return f'<!doctype html><meta charset="utf-8"><style>{ff}{CSS}</style><body>{body}</body>'

JS = """const {chromium}=require('playwright');const jobs=JSON.parse(process.argv[2]);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:800},deviceScaleFactor:1});
for(const [html,out] of jobs){await p.goto('file://'+html);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);
await p.locator('.wrap').screenshot({path:out});console.log(out)}await b.close()})();"""

def main():
    # 그림 HTML을 임시 폴더에 쓰고, Node Playwright(크로미움)로 찍어요
    tmp = pathlib.Path(tempfile.mkdtemp())
    jobs = []
    for l in FONT:
        for name, fn in (('induction-23.png', induction), ('washer-dryer.png', washer_dryer)):
            h = tmp / f'{l}-{name}.html'
            h.write_text(page(l, fn(l)), encoding='utf-8')
            jobs.append([str(h), str(ROOT / OUTDIR[l] / name)])
    js = tmp / 'shot.js'; js.write_text(JS)
    subprocess.run(['node', str(js), json.dumps(jobs)], check=True)

if __name__ == '__main__':
    main()
