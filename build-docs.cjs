const fs=require('node:fs');
const path=require('node:path');
const root=__dirname;
const pages=JSON.parse(fs.readFileSync(path.join(root,'docs/pages.json'),'utf8'));
const url='https://leejinho970715-star.github.io/CRM/';
const intro='# CRM 원본·리뉴얼 화면 대응\n\n42개 CRM 화면과 로그인은 읽기 전용으로 확인했습니다. 마이그레이션은 원본 미열람 제안입니다. 44개 화면을 Pretendard와 공통 뉴트럴 Bento 테마로 통일했습니다.\n\n| 화면 | 원본 경로 | 시안 | 개선 방향 |\n| --- | --- | --- | --- |\n';
fs.writeFileSync(path.join(root,'PAGE-MAP.md'),intro+pages.map(p=>`| ${p.title} | ${p.source} | [보기](${url}#${p.id}) | ${p.improvement} |`).join('\n')+'\n','utf8');
console.log('Updated the 44-page mapping. Design and validation documents remain editorial sources.');
