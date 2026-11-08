# Logo files for GalA-Consult with the apple-shaped globe
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import applemark as am

SITE = os.path.join(os.path.dirname(HERE), 'site')
WM = json.load(open(os.path.join(HERE, 'wordmark.json')))

def rnd(d, p=1):
    return re.sub(r'-?\d+\.\d+', lambda m: f'{float(m.group(0)):.{p}f}'.rstrip('0').rstrip('.'), d)

def wm(key, x, base, size, fill, cls=''):
    s = size / 100
    c = f' class="{cls}"' if cls else ''
    return f'<path{c} transform="translate({x:.2f} {base:.2f}) scale({s})" d="{rnd(WM[key]["d"])}" fill="{fill}"/>'

# full lockup geometry (original composition): rule, text top-left, mark, text bottom-right, rule
FS = 46
W1 = WM['lat_wide']['w'] * FS / 100
W2 = WM['cyr_wide']['w'] * FS / 100
CAP = 75 * FS / 100
X1 = -24 - W1
X2 = 24
TOP, BOT = -135.7, 135.7
B1 = TOP + 25 + CAP
B2 = BOT - 25
L, R = X1 - 6, X2 + W2 + 6
FULL_VB = f'{L - 4:.0f} -150 {R - L + 8:.0f} 300'

def full_inner(p, sheen=False):
    """inner markup of the full lockup; p = unique id prefix"""
    rules = (f'<linearGradient id="{p}r1" x1="0" x2="1"><stop offset="0" stop-color="#9AA9C4" stop-opacity="0"/><stop offset=".25" stop-color="#7F92B6"/><stop offset="1" stop-color="#1B42B0"/></linearGradient>'
             f'<linearGradient id="{p}r2" x1="0" x2="1"><stop offset="0" stop-color="#1B42B0"/><stop offset=".75" stop-color="#7F92B6"/><stop offset="1" stop-color="#9AA9C4" stop-opacity="0"/></linearGradient>')
    sh_defs = sh = ''
    if sheen:
        up, lo = am.crescent_up()[0], am.crescent_lo()
        sh_defs = (f'<clipPath id="{p}clip"><path d="{up}"/><path d="{lo}"/></clipPath>'
                   f'<linearGradient id="{p}sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
        sh = f'<g clip-path="url(#{p}clip)"><g class="sheen"><rect x="-70" y="-170" width="56" height="340" fill="url(#{p}sh)" transform="skewX(-18)"/></g></g>'
    return (f'<defs>{am.defs(p)}{rules}{sh_defs}</defs>'
            f'<rect x="{L:.1f}" y="{TOP - 1.2:.1f}" width="{-L:.1f}" height="2.4" fill="url(#{p}r1)"/>'
            f'<rect x="0" y="{BOT - 1.2:.1f}" width="{R:.1f}" height="2.4" fill="url(#{p}r2)"/>'
            + am.body(p) + sh + wm('lat_wide', X1, B1, FS, '#0B1F45') + wm('cyr_wide', X2, B2, FS, '#1E3F9A'))

def full_svg(p='fl'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{FULL_VB}">{full_inner(p)}</svg>'

def header_svg(p, light=False):
    ms = 100 / 292
    tx = 224 * ms + 24
    l1 = WM['lat']['w'] * 0.36
    l2 = WM['cyr_wide']['w'] * 0.205
    wh = tx + max(l1, l2) + 4
    c1, c2 = ('#FFFFFF', '#AFC0E0') if light else ('#0B1F45', '#4A5E86')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {wh:.0f} 100"><defs>{am.defs(p, bevel=False)}</defs>'
            f'<g transform="translate({112 * ms:.2f} 50) scale({ms:.4f})">{am.body(p, bevel=False, sw=2.4, glare=False)}</g>'
            + wm('lat', tx, 47, 36, c1) + wm('cyr_wide', tx + 1, 80, 20.5, c2) + '</svg>')

def seal_mark():
    """white monochrome mark for the envelope seal"""
    up, lo = am.crescent_up()[0], am.crescent_lo()
    hl, hr = am.half(-1), am.half(1)
    return (f'<svg viewBox="{am.VIEW}" aria-hidden="true"><path d="{up}{lo}" fill="currentColor"/>'
            f'<path d="{hl}{hr}" fill="none" stroke="currentColor" stroke-width="7"/><path d="{am.lines()}" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/></svg>')

if __name__ == '__main__':
    def w(name, s):
        open(f'{SITE}/{name}', 'w').write(s); print(name, len(s))
    w('assets/img/logo-mark.svg', am.mark_svg('m'))
    w('assets/img/logo-full.svg', full_svg())
    w('assets/img/logo-h.svg', header_svg('h'))
    w('assets/img/logo-h-light.svg', header_svg('hl', light=True))
    fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-146 -146 292 292"><defs>{am.defs("f", bevel=False)}</defs>'
           f'{am.body("f", bevel=False, rim=False, sw=6, glare=False, lines_on=False)}</svg>')
    w('favicon.svg', fav)
