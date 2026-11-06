# 출가교화단보 웹판 게시 안내 (README)

출가교화단보를 휴대폰에서 책처럼 넘겨 보는 웹 페이지로 올리는 방법을 적은 안내서입니다.
업무 전반(청탁·정기일기 선정·인쇄·발송)은 「출가교화단보 업무편람」을 따르고, 이 문서는 **웹판 게시 기술 절차만** 다룹니다.

> 웹판은 선택 업무입니다. 이 절차가 어렵다면 웹판은 쉬고 게시판에 PDF만 올려도 됩니다.

---

## 1. 한눈에 보기

| 구분 | 주소 |
| --- | --- |
| 호별 목록 | https://comechoi7-crypto.github.io/Danbo/ |
| 호별 페이지 | https://comechoi7-crypto.github.io/Danbo/호수/ (예: `/407/`) |
| 저장소 | https://github.com/comechoi7-crypto/Danbo |
| 신분검사 안내 | https://comechoi7-crypto.github.io/sinbun/ (저장소 `sinbun`) |

**어떻게 동작하나요?** 이 저장소에 파일을 올리면 GitHub Pages가 1~2분 안에 자동으로 웹사이트로 공개합니다. 따로 서버나 비용은 없습니다.

```
Danbo/
├── index.html                 ← 호별 목록(첫 화면). 호마다 표지 카드 한 줄
├── 407/
│   ├── index.html             ← 넘김형 단보(쪽 그림을 모두 담은 파일 하나)
│   └── cover.jpg              ← 표지(목록·카톡 미리보기용)
├── tools/
│   ├── build_issue.py         ← PDF → 호별 폴더를 만드는 프로그램
│   └── flipbook_template.html ← 넘김형 화면 틀
├── package.json               ← 책 넘김 효과 라이브러리(page-flip 2.0.7)
└── README.md                  ← 이 문서
```

호별 `index.html`에는 카톡 미리보기 정보(표지·제목), 검색엔진 제외 설정, `☰ 목록` 버튼이 들어 있습니다.

---

## 2. 처음 한 번 준비하기

1. **깃허브 계정**을 만들고, 저장소 관리자에게 Danbo 저장소 쓰기 권한(Collaborator)을 받습니다.
2. **PC에 프로그램 설치**
   - Git: https://git-scm.com
   - Python 3: https://www.python.org (설치 때 "Add to PATH" 체크)
   - Node.js: https://nodejs.org
   - Poppler(PDF를 그림으로 바꾸는 도구)와 ImageMagick(그림 변환 도구)
   - 파이썬 패키지: `pip install opencv-python` (QR 자리 자동 찾기)
3. **저장소 내려받기**
   ```bash
   git clone https://github.com/comechoi7-crypto/Danbo.git
   cd Danbo
   npm install
   ```

> 확인 필요: 위 프로그램은 리눅스·맥 기준으로 시험했습니다. 윈도우에서는 Poppler 설치 경로를 PATH에 넣어야 하고, ImageMagick 7은 `convert` 대신 `magick` 명령을 쓸 수 있습니다. 처음 설치한 사람이 여기에 윈도우 설치 방법을 보완해 주세요.

---

## 3. 새 호 올리기 (매달)

1. **저장소를 최신으로**
   ```bash
   git pull
   ```
2. **호별 폴더 만들기** — 최종 PDF를 저장소 폴더에 두고 실행합니다.
   ```bash
   python3 tools/build_issue.py 단보408.pdf 408 "원기111년 12월" --qr-url https://comechoi7-crypto.github.io/sinbun/
   ```
   - 세 번째 값은 **발행 월호**입니다. 파일을 만든 달이 아닙니다(407호는 10월에 만들었지만 11월호).
   - `--qr-url`: PDF 속 QR을 눌렀을 때 갈 주소. 빼면 QR에 들어 있는 주소(인쇄용 네이버 단축주소)로 연결됩니다.
   - QR이 여러 개면 `--qr-page 12`처럼 쪽 번호를 지정합니다. QR이 없는 호는 신경 쓰지 않아도 됩니다.
   - 결과: `408/index.html`, `408/cover.jpg`
3. **목록에 카드 추가** — 루트 `index.html`에서 `<!-- 새 호는 이 줄 아래 맨 앞에 추가 -->` 바로 아래에 한 줄을 넣습니다.
   ```html
   <a class="issue" href="408/"><img src="408/cover.jpg" alt="제408호 표지"><div><b>제408호</b><br>원기111년 12월</div></a>
   ```
4. **미리 확인** — 브라우저로 `408/index.html`을 열어 첫 쪽부터 끝까지 넘겨 보고, QR을 눌러 연결을 확인합니다. 창을 휴대폰 크기로 줄여서도 봅니다.
5. **올리기**
   ```bash
   git add .
   git commit -m "408호 웹판"
   git push
   ```
   1~2분 뒤 https://comechoi7-crypto.github.io/Danbo/408/ 이 열리면 끝입니다.
6. **게시판에 올리기** — 아래 4장의 게시글 HTML을 붙여넣고 PDF를 첨부합니다.
7. **카톡 공유** — 사이트가 열리는 것을 확인한 *뒤에* 링크를 보냅니다. 카톡은 미리보기를 한동안 기억하므로, 먼저 보내면 빈 카드가 남습니다.

---

## 4. 게시판 게시글 HTML

게시판 글쓰기를 **HTML 모드(소스 편집)** 로 바꾸고 아래를 한 덩어리로 붙여넣습니다. `{호수}`, `{년}`, `{월}`만 바꿉니다.

- QR 안내 줄은 해당 호에 QR이 있을 때만 남깁니다.
- 게시판이 자바스크립트를 지우므로 "눌러서 복사" 기능은 넣지 않습니다. 공유용 주소는 글자로 보여 주고 길게 눌러 복사하도록 안내합니다.

```html
<div style="max-width:820px;margin:0 auto;font-family:'Malgun Gothic',sans-serif;color:#3a3330;line-height:1.7;">
  <p style="font-size:18px;font-weight:bold;margin:0 0 10px;">[출가교화단보 제{호수}호] 원기{년}년 {월}월호</p>
  <p style="font-size:15px;margin:0 0 6px;">휴대폰에서 책처럼 넘겨 보실 수 있도록 웹으로도 함께 보내드립니다.</p>
  <p style="font-size:15px;margin:0 0 14px;">아래 화면에서 페이지를 넘기며 바로 보시거나, 버튼을 눌러 전체 화면으로 보실 수 있습니다. (별도 다운로드 불필요)</p>
  <div style="position:relative;width:100%;height:640px;border:1px solid #e3d6cc;border-radius:8px;overflow:hidden;background:#3a3330;">
    <iframe src="https://comechoi7-crypto.github.io/Danbo/{호수}/" title="출가교화단보 제{호수}호" style="width:100%;height:100%;border:0;" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="text-align:center;margin:16px 0 10px;">
    <a href="https://comechoi7-crypto.github.io/Danbo/{호수}/" target="_blank" style="display:inline-block;background:#b8876b;color:#fff;text-decoration:none;padding:10px 22px;border-radius:22px;font-size:15px;">📖 {호수}호 전체 화면으로 보기</a>
  </p>
  <div style="background:#f6efe9;border:1px solid #e3d6cc;border-radius:8px;padding:12px 16px;margin:0 0 16px;text-align:center;">
    <p style="font-size:14px;font-weight:bold;margin:0 0 4px;">🔗 공유용 주소</p>
    <p style="font-size:15px;margin:0 0 4px;word-break:break-all;">https://comechoi7-crypto.github.io/Danbo/{호수}/</p>
    <p style="font-size:12px;color:#8a7d75;margin:0;">단톡방 등에 전하실 때 위 주소를 복사해 붙여넣어 주세요. (휴대폰은 길게 눌러 복사)</p>
  </div>
  <p style="font-size:14px;color:#6b5f58;margin:0 0 4px;">※ 12쪽 신분검사 안내의 QR코드를 누르시면 안내 페이지로 바로 연결됩니다.</p>
  <p style="font-size:14px;color:#6b5f58;margin:0;">※ 인쇄·보관용 PDF는 첨부파일로 함께 올려 드립니다.</p>
</div>
```

---

## 5. 문제가 생겼을 때

| 증상 | 확인할 것 |
| --- | --- |
| 주소가 열리지 않음 (404) | 저장소 **Settings → Pages**에서 Branch가 `main`, 폴더 `/ (root)`인지. 이 설정은 휴대폰 앱이 아니라 브라우저(데스크톱 화면)에서 한다 |
| 올렸는데 예전 화면이 보임 | 1~2분 기다린 뒤 새로고침. 휴대폰은 브라우저 캐시를 지우거나 시크릿 창으로 확인 |
| 카톡 미리보기가 비어 있거나 예전 내용 | 카톡이 미리보기를 기억한 것. 시간이 지나면 바뀐다. 다음부터는 사이트 확인 후 공유 |
| QR을 눌러도 이상한 곳으로 감 | `--qr-url`을 빠뜨렸거나 잘못 넣음. 2단계를 다시 실행하고 다시 올린다 |
| 게시판에서 넘김 화면이 빈 칸 | 그 게시판이 iframe을 막은 것. 버튼과 공유용 주소는 그대로 작동하므로 그대로 두어도 된다 |
| `build_issue.py` 실행 오류 | `npm install`을 했는지, Poppler·ImageMagick·opencv가 설치됐는지 확인 |

---

## 6. 인계할 때

- 이 저장소와 `sinbun` 저장소는 현재 담당자 **개인 깃허브 계정(comechoi7-crypto)** 아래에 있습니다.
- 다음 담당자에게 **Collaborator 권한을 주거나**, 사무처 공용 계정으로 **저장소를 이전(Transfer)** 합니다.
- 이전하면 주소(`comechoi7-crypto.github.io/...`)가 바뀝니다. 인쇄본 QR, 기존 게시글 링크, 이 문서의 주소를 함께 고쳐야 합니다.
- 웹판을 이어갈 사람이 없으면 웹판은 쉬고 PDF만 게시합니다. 이미 올린 호는 저장소를 지우지 않는 한 계속 열립니다.
