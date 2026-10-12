# 배경 이미지 제작 기록

2026-10-12, 기본 내장 Imagegen 도구 사용. 기존 제품 에셋이나 실제 UI는 수정하지 않았습니다. 생성된 PNG 원본을 프로젝트에 복사하고, 웹에서는 같은 이미지의 고품질 WebP 변환본을 사용합니다. 아래 초기 네이비 제품 패턴은 현재 사용하지 않습니다.

## 저장 파일

- 메인 배경: `i-ONE/assets/hero-tech-background.png`, `i-ONE/assets/hero-tech-background.webp` (1672×941)
- 현재 제품·상담 패턴: `i-ONE/assets/product-tech-light.png`, `i-ONE/assets/product-tech-light.webp` (1672×941)
- 초기 네이비 패턴 보존본(미사용): `i-ONE/assets/product-tech-pattern.png`, `i-ONE/assets/product-tech-pattern.webp`
- 적용 스타일: `i-ONE/backgrounds.css`

## 메인 배경 최종 프롬프트

Use case: stylized-concept. Asset type: a wide landscape background image for a polished Korean enterprise software company landing-page hero, approx 16:9. Primary request: a very light sophisticated technology background that will sit BEHIND an existing large colorful glass 3D product artwork on the right and dark navy Korean headline on the left. Create a near-white icy pearl background, quiet layered frosted-glass ribbons and delicate translucent architectural curves, subtle blue light trails with very fine interconnected data points, a restrained sense of depth. Brand palette navy #1A3C83 and blue #1462FD, almost-white pale blue. Composition: the entire left half and upper center must remain nearly plain white negative space for readable copy; concentrate faint abstract depth toward the right perimeter and bottom right, leave room for a separate foreground product asset. Soft studio light, sparse, high-end B2B technology, calm and clean. Wide full-bleed artwork, no frames. No text, no logos, no letters, no product symbols, no mock UI, no dashboards, no fake screenshots, no large foreground object, no dark background, no neon clutter, no dense grids. All elements subtle and low contrast; overall image should remain predominantly white.

## 제품 섹션 패턴 최종 프롬프트

Use case: stylized-concept. Asset type: wide landscape subtle technology texture background for navy enterprise-software product sections. Create a restrained elegant abstract digital-network and microcircuit pattern on a deep navy #102e68 to #1A3C83 background. Fine architectural circuit paths, sparse connecting points, faint layered perspective grids, very delicate translucent data waves, quiet depth. Lines must be thin, low contrast, desaturated cool blue (#5678af), mostly around the perimeter and right side. The left third and central band must remain calm and darker to keep white product copy and colorful foreground 3D logos readable. Premium B2B enterprise tone, calm, professional, editorial sophistication. Pattern detail should be discernible at low opacity, not prominent. Continuous full-bleed 16:9 backdrop. No text, logos, symbols, dashboards, UI, people, recognizable chips, large hexagon decorations, strong lens flares or saturated neon. No border, no frame, no vignette-black corners. This is only a supporting background texture.

## 현재 밝은 제품 패턴 최종 프롬프트

Use case: stylized-concept. Asset type: subtle technology background texture for i-ONE enterprise product landing website. Generate a high-resolution wide 16:9 abstract raster background, near-white and very pale ice blue base, gentle cyan #00ade7 and bright blue #0072ce accents only. Fine flowing data paths, small network nodes, faint circuit lines, subtle translucent frosted glass geometry concentrated on the right and edges. Large clean quiet central and left areas for dark text and separate colorful 3D product assets to be overlaid in code. Professional Korean ICT company aesthetic, restrained premium soft light, very low contrast, airy rather than busy. No dark navy, no dark background, no text, no letters, no numbers, no logo, no interface mockup, no recognizable product mark. Pattern should remain elegant when reused across six product sections.

## 적용

메인은 기존 3D 에셋을 전경으로 두고 밝은 배경을 전체에 배치했습니다. 6개 제품 소개 섹션은 밝은 공통 패턴의 위치를 조금씩 조정합니다. 패턴 불투명도는 PC 65%, 모바일 55%, 하단 상담 45%/35%입니다. 생성 원본은 기본 내장 도구 경로에서 프로젝트로 복사했으며 CLI/API fallback은 사용하지 않았습니다.
