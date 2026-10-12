# 배경 이미지 제작 기록

2026-10-12, 기본 내장 Imagegen 도구로 신규 이미지 2개 생성. 기존 제품 에셋이나 실제 UI는 수정하지 않았습니다. 생성된 PNG 원본을 프로젝트에 복사하고, 웹에서는 같은 이미지의 WebP 변환본을 사용합니다.

## 저장 파일

- 메인 배경: `products/assets/hero-tech-background.png`, `products/assets/hero-tech-background.webp` (1672×941)
- 제품·상담 섹션 패턴: `products/assets/product-tech-pattern.png`, `products/assets/product-tech-pattern.webp` (1672×941)
- 적용 스타일: `products/backgrounds.css`

## 메인 배경 최종 프롬프트

Use case: stylized-concept. Asset type: a wide landscape background image for a polished Korean enterprise software company landing-page hero, approx 16:9. Primary request: a very light sophisticated technology background that will sit BEHIND an existing large colorful glass 3D product artwork on the right and dark navy Korean headline on the left. Create a near-white icy pearl background, quiet layered frosted-glass ribbons and delicate translucent architectural curves, subtle blue light trails with very fine interconnected data points, a restrained sense of depth. Brand palette navy #1A3C83 and blue #1462FD, almost-white pale blue. Composition: the entire left half and upper center must remain nearly plain white negative space for readable copy; concentrate faint abstract depth toward the right perimeter and bottom right, leave room for a separate foreground product asset. Soft studio light, sparse, high-end B2B technology, calm and clean. Wide full-bleed artwork, no frames. No text, no logos, no letters, no product symbols, no mock UI, no dashboards, no fake screenshots, no large foreground object, no dark background, no neon clutter, no dense grids. All elements subtle and low contrast; overall image should remain predominantly white.

## 제품 섹션 패턴 최종 프롬프트

Use case: stylized-concept. Asset type: wide landscape subtle technology texture background for navy enterprise-software product sections. Create a restrained elegant abstract digital-network and microcircuit pattern on a deep navy #102e68 to #1A3C83 background. Fine architectural circuit paths, sparse connecting points, faint layered perspective grids, very delicate translucent data waves, quiet depth. Lines must be thin, low contrast, desaturated cool blue (#5678af), mostly around the perimeter and right side. The left third and central band must remain calm and darker to keep white product copy and colorful foreground 3D logos readable. Premium B2B enterprise tone, calm, professional, editorial sophistication. Pattern detail should be discernible at low opacity, not prominent. Continuous full-bleed 16:9 backdrop. No text, logos, symbols, dashboards, UI, people, recognizable chips, large hexagon decorations, strong lens flares or saturated neon. No border, no frame, no vignette-black corners. This is only a supporting background texture.

## 적용

메인은 기존 3D 에셋을 전경으로 두고 밝은 배경을 전체에 배치했습니다. 6개 제품 소개 섹션은 공통 패턴의 위치를 조금씩 조정해 시각적 통일감을 유지합니다. PC 제품 섹션의 패턴 불투명도는 64%, 모바일은 50%이며, 하단 상담은 더 낮은 36%/28%를 적용했습니다. 이미지 자체의 밝기와 별도의 그라데이션도 함께 작용하므로 이 값은 화면의 최종 대비를 뜻하지 않습니다.
