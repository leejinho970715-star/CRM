# 아이원소프트뱅크 제품 랜딩

기존 CRM과 별도로 열리는 회사·제품 소개 원페이지입니다.

- 배포 경로: `/products/`
- 제품 바로가기: `/products/#omniesol`, `#amaranth10`, `#wehago`, `#oneai`, `#nonprofit`, `#ifrs18`
- 빌드: `python scripts/build-product-landing.py` (표준 라이브러리만 사용)
- 콘텐츠 수정: `products/data.json`
- 스타일·동작: `landing.css`, `landing.js`
- 장식 배경: `backgrounds.css`, `assets/hero-tech-background.webp`, `assets/product-tech-pattern.webp`
- 프리뷰: 저장소 루트에서 `python -m http.server 8940` 실행 후 `/products/` 접속

## 구성

두 로고를 병렬 배치한 헤더 → 제공된 3D 이미지 중심의 메인 → 6개 제품 탭 → 제품 소개 스크롤 모션 → 제품별 3개 기능의 실제 UI → 회사 소개 → 도입 안내 → 공식 상담 링크.

GSAP ScrollTrigger로 비주얼 확대, 안착, 설명 등장을 하나의 타임라인으로 구성했습니다. 스크롤 입력을 가로채지 않고 pin spacing으로 다음 콘텐츠를 연결합니다. 모바일은 세로 구성과 짧은 타임라인을 사용합니다. 운영체제의 모션 줄이기 설정에서는 pin 없이 설명을 표시합니다. 제품 소개 건너뛰기, 방향키 탭 전환, 이미지 확대와 Escape 닫기도 제공합니다.

Pretendard, 네이비 `#1A3C83`, 블루 `#1462FD`를 사용합니다. 제공된 PNG는 보존하고 실제 페이지에서는 투명 여백을 정리한 WebP를 사용합니다. 이미지의 형태와 비율은 유지합니다.

## 자료와 범위

실제 기능 화면 18개는 공개된 제품 소개 자료에서 가져왔습니다. 각 화면에 원문 링크를 제공하며, 정확한 출처는 [SOURCES.md](SOURCES.md)에 기록했습니다. IFRS18은 Amaranth10 재무제표관리 기능으로 설명합니다. 비영리 자료는 공개 제안서의 예시 화면입니다.

모든 모듈을 설명하는 제품 매뉴얼 대신 대표 기능을 소개하는 랜딩입니다. 더 많은 기능은 각 제품의 공식 소개 링크에서 확인할 수 있습니다. 온라인 상담은 기존 아이원 문의 페이지로 이동하며, 이 페이지에서는 사용자 정보를 수집하거나 전송하지 않습니다.

별도의 설치·빌드 설정이 없는 정적 페이지로 GitHub Pages와 Vercel에서 같은 경로를 사용할 수 있습니다. 기존 CRM 소스와 라우트는 수정하지 않았습니다.
