#!/usr/bin/env python3
"""출가교화단보 PDF → 넘김형 HTML(호별 폴더) 생성기
사용: python3 tools/build_issue.py <단보.pdf> <호수> "<원기111년 11월>" [--qr-url URL] [--qr-page N]
필요: poppler-utils(pdftoppm), ImageMagick(convert), opencv-python(QR 자동탐지), npm 패키지 page-flip
"""
import argparse, base64, glob, json, os, re, subprocess, sys, tempfile
ap=argparse.ArgumentParser()
ap.add_argument('pdf'); ap.add_argument('no'); ap.add_argument('month')
ap.add_argument('--qr-url',default=None,help='QR 클릭 시 이동할 주소(없으면 PDF 속 QR 값 그대로)')
ap.add_argument('--qr-page',type=int,default=None)
ap.add_argument('--lib',default='node_modules/page-flip/dist/js/page-flip.browser.js')
a=ap.parse_args()
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tmp=tempfile.mkdtemp()
subprocess.run(['pdftoppm','-r','150','-png',a.pdf,f'{tmp}/p'],check=True)
pngs=sorted(glob.glob(f'{tmp}/p-*.png'))
jpgs=[]
for p in pngs:
    j=p[:-4]+'.jpg'; subprocess.run(['convert',p,'-quality','82',j],check=True); jpgs.append(j)
# QR 탐지 (여러 개면 첫 번째 사용 — 필요시 --qr-page로 지정)
hot=None; qr_page=a.qr_page; qr_val=None
try:
    import cv2
    det=cv2.QRCodeDetector()
    for i,p in enumerate(pngs,1):
        if qr_page and i!=qr_page: continue
        im=cv2.imread(p); ok,vals,pts,_=det.detectAndDecodeMulti(im)
        if ok and len(pts):
            H,W=im.shape[:2]; xs=pts[0][:,0]; ys=pts[0][:,1]; pad=8
            x0,x1,y0,y1=xs.min()-pad,xs.max()+pad,ys.min()-pad,ys.max()+pad
            hot={k:float(v) for k,v in dict(left=x0/W*100,top=y0/H*100,width=(x1-x0)/W*100,height=(y1-y0)/H*100).items()}
            qr_page=i; qr_val=vals[0]; break
except ImportError:
    print('opencv 없음: QR 링크 생략', file=sys.stderr)
url=a.qr_url or qr_val
print(f'QR: page={qr_page} value={qr_val} -> link={url}')
pages=["data:image/jpeg;base64,"+base64.b64encode(open(j,'rb').read()).decode() for j in jpgs]
lib=open(a.lib).read()
tpl=open(os.path.join(root,'tools','flipbook_template.html')).read()
html=tpl.replace('/*LIB*/',lib).replace('/*PAGES*/',json.dumps(pages)).replace('/*HOT*/',json.dumps(hot or {}))
html=re.sub(r'제\d+호',f'제{a.no}호',html); html=re.sub(r'원기\d+년 \d+월',a.month,html)
html=re.sub(r'/Danbo/\d+/',f'/Danbo/{a.no}/',html)
html=re.sub(r'const SINBUN_URL = ".*?";',f'const SINBUN_URL = {json.dumps(url or "")};',html)
html=re.sub(r'const QR_PAGE = \d+;',f'const QR_PAGE = {qr_page or -1};',html)
out=os.path.join(root,a.no); os.makedirs(out,exist_ok=True)
open(os.path.join(out,'index.html'),'w').write(html)
subprocess.run(['convert',jpgs[0],'-resize','400x','-quality','85',os.path.join(out,'cover.jpg')],check=True)
print('완료:',out,'— 루트 index.html 목록에 카드 한 줄 추가할 것')
