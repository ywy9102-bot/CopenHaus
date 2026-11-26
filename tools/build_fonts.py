#!/usr/bin/env python3
"""가이드북·브로슈어 글꼴을 저장소 안(fonts/)에 직접 만들어 두는 스크립트.

왜: 구글 폰트 서버가 막힌 네트워크(중국 로밍, 느린 공항 와이파이)에서도
첫 화면이 바로 뜨게 하려고 글꼴을 사이트에 직접 둬요(셀프 호스팅).
글꼴 원본은 수십 MB라서, 두 페이지에 실제로 쓰인 글자만 남겨(서브셋) 작게 만들어요.

언제 다시 돌리나: index.html·brochure/index.html에 **새 글자**(새 한자·한글 등)가
들어간 문구를 넣었을 때. 안 돌려도 화면은 깨지지 않고, 없는 글자만 휴대폰 기본 글꼴로 보여요.

쓰는 법 (저장소 맨 위에서):
    pip install fonttools brotli
    python3 tools/build_fonts.py
원본 글꼴(OFL 라이선스, Google Fonts)은 처음 한 번 tools/.font-src/ 에 내려받아요(커밋하지 않음).
"""
import os, re, sys, urllib.request
from fontTools import subset

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', '.font-src')
OUT = os.path.join(ROOT, 'fonts')
PAGES = ['index.html', 'brochure/index.html']
FAMILIES = ('Noto+Sans+KR:wght@400;700&family=Noto+Serif+KR:wght@700'
            '&family=Noto+Sans+JP:wght@400;700&family=Noto+Serif+JP:wght@700'
            '&family=Noto+Sans+SC:wght@400;700&family=Noto+Serif+SC:wght@700'
            '&family=Noto+Sans+TC:wght@400;700&family=Noto+Serif+TC:wght@700')

def fetch_sources():
    os.makedirs(SRC, exist_ok=True)
    # 오래된 User-Agent로 요청하면 구글이 나눠지지 않은 TTF 전체 파일 주소를 줘요
    req = urllib.request.Request('https://fonts.googleapis.com/css2?family=' + FAMILIES, headers={'User-Agent': 'Wget/1.0'})
    css = urllib.request.urlopen(req).read().decode()
    out = []
    for fam, w, url in re.findall(r"font-family: '([^']+)';\s*font-style: \w+;\s*font-weight: (\d+);.*?src: url\(([^)]+)\)", css, re.S):
        name = fam.replace(' ', '') + '-' + w
        path = os.path.join(SRC, name + '.ttf')
        if not os.path.exists(path):
            print('내려받기', name); urllib.request.urlretrieve(url, path)
        out.append((name, path))
    return out

def used_text():
    s = set()
    for p in PAGES:
        s |= set(open(os.path.join(ROOT, p), encoding='utf-8').read())
    s |= set(chr(c) for c in range(0x20, 0x7F))        # 영문·숫자·기호 전부
    s |= set(chr(c) for c in range(0xA0, 0x100))       # 라틴 기본 확장(é 등)
    s |= set('‐‑–—‘’“”•·…※→←↑↓₩€¥℃°×÷')
    return ''.join(sorted(c for c in s if c >= ' '))

def main():
    os.makedirs(OUT, exist_ok=True)
    text = used_text()
    for name, path in fetch_sources():
        opt = subset.Options(); opt.flavor = 'woff2'; opt.layout_features = ['*']; opt.name_IDs = ['*']
        f = subset.load_font(path, opt)
        sub = subset.Subsetter(opt); sub.populate(text=text); sub.subset(f)
        dst = os.path.join(OUT, name + '.woff2')
        subset.save_font(f, dst, opt)
        print(f'{name}.woff2  {os.path.getsize(dst)//1024} KB')

if __name__ == '__main__':
    sys.exit(main())
