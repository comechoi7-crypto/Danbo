# 출가교화단보 넘김형 웹판 (Danbo)

원불교 수위단회사무처 출가교화단보를 호별로 넘겨 보는 웹 페이지.

- 사이트: https://comechoi7-crypto.github.io/Danbo/
- 호별 주소: https://comechoi7-crypto.github.io/Danbo/<호수>/

## 새 호 올리기
```bash
npm install                                  # 최초 1회 (page-flip)
python3 tools/build_issue.py 단보408.pdf 408 "원기111년 12월" \
        --qr-url https://comechoi7-crypto.github.io/sinbun/   # QR 연결 주소가 따로 있을 때만
```
1. `408/` 폴더(index.html, cover.jpg)가 생성됨
2. 루트 `index.html`의 `<!-- 새 호는 이 줄 아래 맨 앞에 추가 -->` 아래에 카드 한 줄 추가
3. 커밋·푸시 → 1~2분 후 반영

필요 도구: poppler-utils, ImageMagick, Python opencv(QR 자동 탐지)
