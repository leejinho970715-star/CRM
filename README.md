# IONE CRM 리뉴얼 시안

[전체 시안](https://leejinho970715-star.github.io/CRM/) · [영업활동 관리](https://leejinho970715-star.github.io/CRM/#activity) · [단독 영업활동 시안](https://leejinho970715-star.github.io/CRM/activity.html)

44개 화면을 White / Neutral, Calm Density, Thin Border, Bento 구조와 Pretendard로 통일했습니다. 운영 CRM 42개 화면과 로그인의 기존 분석을 바탕으로 구현했고, 마이그레이션은 원본을 열지 않은 제안입니다. 실제 운영 CRM은 변경하지 않았습니다.

## 결과물

- [페이지별 As-is / To-be PDF — 49쪽](docs/CRM-Renewal-As-Is-To-Be.pdf)
- [전체 화면 PNG 45장 ZIP](docs/CRM-PNG.zip): 단독 영업활동, 통합 영업활동, 나머지 43개 화면. 영업활동이 맨 앞입니다.
- [페이지별 비교 원문](docs/AS-IS-TO-BE.md)
- [원본 화면 대응](PAGE-MAP.md), [디자인 규칙](DESIGN-SYSTEM.md), [검증 기록](VALIDATION.md)

사용자 표시는 **사용자님**, 담당자·입력자는 **user_1~3**입니다. 고객명·코드·사업자번호를 포함한 배포 데이터는 가상 샘플입니다.

## 실행과 배포

설치나 앱 빌드 없이 `python -m http.server 8937 --bind 127.0.0.1`을 실행하고 `http://127.0.0.1:8937/`에서 확인할 수 있습니다. 폰트·아이콘·스크립트는 자체 호스팅합니다.

GitHub Pages는 **main 브랜치 / 루트 디렉터리**를 배포합니다. `.nojekyll`과 상대경로를 사용합니다. `index.html`은 전체 CRM, `crm.html`은 호환 진입점, `activity.html`은 처음 만든 영업활동 시안입니다.

## 주요 파일

| 파일 | 역할 |
| --- | --- |
| index.html / crm.html / suite.js / suite-data.js / suite.css | 44개 화면과 공통 메뉴·표·폼 |
| activity.html / app.js / styles.css | 최초 영업활동 시안 및 로컬 저장 |
| theme.css | 모든 화면의 Pretendard와 통일 디자인 토큰 |
| assets/fonts | 공식 Pretendard 웹 글꼴과 OFL 라이선스 |
| assets/favicon* / assets/og-image.png | 앱 아이콘과 1200×630 공유 이미지 |
| docs/screens | 브라우저 전체 페이지 캡처 PNG와 검증 manifest |
| scripts/prepare-site.cjs | 진입점·메타데이터·공통 테마 구성 |
| scripts/build-comparison.py | 비교 PDF 및 PNG ZIP 생성 |
| scripts/build-public-assets.cjs / scripts/build-og.py | 아이콘·공유 이미지 생성 |

PDF와 OG 재생성은 Python reportlab, pypdf, Pillow 및 공식 Pretendard Regular/Bold TTF가 필요합니다. TTF를 `output/pdf/fonts/`에 두고 스크립트를 실행합니다. 출처는 THIRD-PARTY-NOTICES.md에 있습니다. PNG manifest는 실제 브라우저 캡처를 바탕으로 생성합니다. 아이콘 생성은 Node sharp를 사용합니다.

## 시안 범위

검색·필터·탭·상세 패널·샘플 계산·로컬 저장 동작을 제공합니다. 실제 CRM 서버, 로그인 인증, 접근 권한, AI 생성, 뉴스 수집, 이메일·알림 서비스와 연결되지 않습니다. CSV 읽기를 지원하며 Excel 선택 시 실제 파싱하지 않았음을 안내합니다. 기존 로컬 초안·이력·첨부 저장소는 유지합니다.
