# GalA-Consult mark with the apple-shaped globe (reference to Almaty)
import math
CY = 35.7        # D centres at y = -CY (upper) / +CY (lower), radius 100
XM = 70.0        # half width of the globe
A = 24.0         # top lobes: ellipses centred at (+-A, 0) give the apple dip at the top
RXL = XM - A     # lobe x radius, so lobe and bottom circle meet at the widest point
RYT = 60.0       # top height
RYB = 60.0       # bottom: one round ellipse across both halves
S = 3.6          # half width of the groove between the two halves
G = 6.0          # gap between globe and crescents
FIL = 3.2        # rounded corner where the top dips into the groove

def f(v): return f'{v:.2f}'.rstrip('0').rstrip('.')

def _cut_inside(x, y):
    """inside the (offset) cutout around the RIGHT half (mirror x for the left)"""
    if y >= 0:
        return (x / (XM + G)) ** 2 + (y / (RYB + G)) ** 2 < 1
    return ((x - A) / (RXL + G)) ** 2 + (y / (RYT + G)) ** 2 < 1

def crescent_up():
    rxl, ryt, rxb, ryb = RXL + G, RYT + G, XM + G, RYB + G
    yq = -ryt * math.sqrt(1 - (A / rxl) ** 2)
    # walk the D_up arc clockwise from the top until it enters the cutout
    prev = None
    for k in range(-900, 900):
        t = math.radians(k / 10)
        x, y = 100 * math.cos(t), -CY + 100 * math.sin(t)
        if x < 0: continue
        if _cut_inside(x, y): t1 = t; break
        prev = t
    a_, b_ = prev, t1
    for _ in range(60):
        m = (a_ + b_) / 2
        x, y = 100 * math.cos(m), -CY + 100 * math.sin(m)
        if _cut_inside(x, y): b_ = m
        else: a_ = m
    px, py = 100 * math.cos(b_), -CY + 100 * math.sin(b_)
    return (f'M0,{f(-CY - 100)}A100,100 0 0 1 {f(px)},{f(py)}'
            f'A{f(rxb)},{f(ryb)} 0 0 0 {f(rxb)},0'
            f'A{f(rxl)},{f(ryt)} 0 0 0 0,{f(yq)}Z'), (px, py), yq

def crescent_lo():
    rxl, ryt, rxb, ryb = RXL + G, RYT + G, XM + G, RYB + G
    # walk the left lobe cutout from its widest point upwards until it leaves the D_lo circle
    prev = None
    for k in range(1800, 3600):
        t = math.radians(k / 10)
        x, y = -A + rxl * math.cos(t), ryt * math.sin(t)
        if y > 0: continue
        if x * x + (y - CY) ** 2 > 100 ** 2: t1 = t; break
        prev = t
    a_, b_ = prev, t1
    for _ in range(60):
        m = (a_ + b_) / 2
        x, y = -A + rxl * math.cos(m), ryt * math.sin(m)
        if x * x + (y - CY) ** 2 > 100 ** 2: b_ = m
        else: a_ = m
    px, py = -A + rxl * math.cos(a_), ryt * math.sin(a_)
    return (f'M0,{f(CY + 100)}L0,{f(ryb)}'
            f'A{f(rxb)},{f(ryb)} 0 0 1 {f(-rxb)},0'
            f'A{f(rxl)},{f(ryt)} 0 0 1 {f(px)},{f(py)}'
            f'A100,100 0 0 0 0,{f(CY + 100)}Z')

def half(side):
    """one half of the apple: lobe on top (dips into the groove with a rounded corner),
       round bottom shared by both halves, straight groove edge"""
    sg = 1 if side > 0 else -1
    yt = -RYT * math.sqrt(1 - ((S - A) / RXL) ** 2)          # top corner at the groove
    ex = S + FIL * 1.15
    ey = -RYT * math.sqrt(1 - ((ex - A) / RXL) ** 2)
    yb = RYB * math.sqrt(1 - (S / XM) ** 2)                  # bottom corner at the groove
    X = lambda x: f(sg * x)
    sw = 1 if sg > 0 else 0
    return (f'M{X(S)},{f(yt + FIL)}Q{X(S)},{f(yt)} {X(ex)},{f(ey)}'
            f'A{f(RXL)},{f(RYT)} 0 0 {sw} {X(XM)},0'
            f'A{f(XM)},{f(RYB)} 0 0 {sw} {X(S)},{f(yb)}Z')

def lines(meridian=False):
    """globe lines as in the original logo: equator, an upper parallel that dips
       towards the groove, a lower parallel that rises towards it"""
    out = []
    yg, ye = .56 * RYT, .76 * RYT
    xt = A + RXL * math.sqrt(1 - (ye / RYT) ** 2) - .5
    yg2, ye2 = .56 * RYB, .76 * RYB
    xb = XM * math.sqrt(1 - (ye2 / RYB) ** 2) - .5
    for sg in (1, -1):
        X = lambda x: f(sg * x)
        out.append(f'M{X(S + 1.2)},0L{X(XM - .6)},0')
        out.append(f'M{X(S + 1.2)},{f(-yg)}Q{X((S + xt) / 2 + 4)},{f(-yg - 1.5)} {X(xt)},{f(-ye)}')
        out.append(f'M{X(S + 1.2)},{f(yg2)}Q{X((S + xb) / 2 + 3)},{f(yg2 + 1.5)} {X(xb)},{f(ye2)}')
    return ''.join(out)

STOPS = [(0, '#86A9FF'), (.2, '#3F72F2'), (.44, '#1B42B0'), (.56, '#2D5DD8'), (.78, '#14317F'), (1, '#0A1D57')]

def defs(p, bevel=True):
    stops = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in STOPS)
    flt = (f'<filter id="{p}bv" x="-30%" y="-30%" width="160%" height="160%">'
           f'<feGaussianBlur in="SourceAlpha" stdDeviation="6" result="b"/>'
           f'<feSpecularLighting in="b" surfaceScale="4" specularConstant=".9" specularExponent="18" lighting-color="#fff" result="s"><fePointLight x="-160" y="-260" z="260"/></feSpecularLighting>'
           f'<feComposite in="s" in2="SourceAlpha" operator="in" result="si"/>'
           f'<feComposite in="SourceGraphic" in2="si" operator="arithmetic" k1="0" k2="1" k3=".38" k4="0"/></filter>') if bevel else ''
    return (f'<linearGradient id="{p}cr" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient>'
            f'<linearGradient id="{p}rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".45" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="{p}spL" cx=".38" cy=".3" r=".9"><stop offset="0" stop-color="#fff"/><stop offset=".45" stop-color="#EFF3FA"/><stop offset=".82" stop-color="#D3DCEB"/><stop offset="1" stop-color="#B7C4DB"/></radialGradient>'
            f'<radialGradient id="{p}spR" cx=".3" cy=".3" r=".95"><stop offset="0" stop-color="#FBFCFE"/><stop offset=".45" stop-color="#E9EEF7"/><stop offset=".82" stop-color="#CCD6E7"/><stop offset="1" stop-color="#B0BED7"/></radialGradient>'
            f'<radialGradient id="{p}gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            + flt)

def body(p, bevel=True, sw=1.5, rim=True, meridian=False, glare=True, line_op=.72, lines_on=True):
    up, lo = crescent_up()[0], crescent_lo()
    flt = f' filter="url(#{p}bv)"' if bevel else ''
    rimp = (f'<path d="{up}" fill="none" stroke="url(#{p}rim)" stroke-width="1.6"/>'
            f'<path d="{lo}" fill="none" stroke="url(#{p}rim)" stroke-width="1.6"/>') if rim else ''
    hl, hr = half(-1), half(1)
    gl = (f'<ellipse cx="-40" cy="-30" rx="15" ry="8.5" transform="rotate(-38 -40 -30)" fill="url(#{p}gl)" opacity=".75"/>'
          f'<ellipse cx="20" cy="-40" rx="9.5" ry="5" transform="rotate(-20 20 -40)" fill="url(#{p}gl)" opacity=".5"/>') if glare else ''
    return (f'<g{flt}><path d="{up}" fill="url(#{p}cr)"/><path d="{lo}" fill="url(#{p}cr)"/></g>{rimp}'
            f'<path d="{hl}" fill="url(#{p}spL)"/><path d="{hr}" fill="url(#{p}spR)"/>'
            + (f'<path d="{lines(meridian)}" fill="none" stroke="#2E66EE" stroke-opacity="{line_op}" stroke-width="{sw}" stroke-linecap="round"/>' if lines_on else '') +
            f'<path d="{hl}{hr}" fill="none" stroke="#7E97C8" stroke-width="1.25"/>' + gl)

VIEW = '-112 -146 224 292'
def mark_svg(p='m', **kw):
    bevel = kw.pop('bevel', True)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VIEW}"><defs>{defs(p, bevel)}</defs>{body(p, bevel=bevel, **kw)}</svg>'

if __name__ == '__main__':
    print(crescent_up())
    print(half(1))
