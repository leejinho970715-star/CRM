const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const url = 'https://leejinho970715-star.github.io/CRM/';
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
const write = (name, data) => fs.writeFileSync(path.join(root, name), data, 'utf8');

if (!fs.existsSync(path.join(root, 'activity.html'))) write('activity.html', read('index.html'));
const metadata = canonical => `
  <meta name="description" content="IONE CRM 리뉴얼 시안. 고객 관리, 영업활동, 후속 업무, 포캐스팅, 보고서와 관리자까지 44개 화면을 살펴보세요.">
  <meta name="theme-color" content="#4263cd">
  <link rel="canonical" href="${canonical}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="assets/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:site_name" content="IONE CRM">
  <meta property="og:title" content="IONE CRM | 고객과 기회를 연결하는 워크스페이스">
  <meta property="og:description" content="고객에서 활동, 다음 업무와 계약까지. 전체 CRM 리뉴얼 UI 시안을 확인하세요.">
  <meta property="og:url" content="${canonical}">
  <meta property="og:image" content="${url}assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:alt" content="IONE CRM 제목과 영업활동 관리 리뉴얼 화면">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="IONE CRM 리뉴얼 시안">
  <meta name="twitter:description" content="고객에서 활동, 다음 업무와 계약까지 연결하는 44개 CRM 화면.">
  <meta name="twitter:image" content="${url}assets/og-image.png">`;
function setHead(html, canonical) {
  const description = html.indexOf('<meta name="description"');
  if (description !== -1) html = html.slice(0, description) + html.slice(html.indexOf('</head>', description));
  html = html.replace(/\s*<link[^>]+(?:theme\.css|responsive\.css|as="font")[^>]*>/g, '');
  return html.replace('</head>', '<link rel="preload" href="assets/fonts/PretendardVariable.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="theme.css?v=3.0"><link rel="stylesheet" href="responsive.css?v=4.1">' + metadata(canonical) + '\n</head>');
}
let crm = read('crm.html').replace(/\?v=2\.[789]/g, '?v=3.0').replace('시안 <span>v2.0', '시안 <span>v3.0');
crm = crm.replace('ローカル UI', '로컬 UI').replace('로컬 UI 시안', 'CRM 리뉴얼 시안');
if (!crm.includes('href="docs/CRM-Renewal-As-Is-To-Be.pdf"')) crm = crm.replace('<span>IONE CRM · Renewal concept</span>', '<span>IONE CRM · Renewal concept</span><a href="docs/CRM-Renewal-As-Is-To-Be.pdf" target="_blank" rel="noopener">개선 비교 PDF</a>');
write('index.html', setHead(crm, url));
write('crm.html', setHead(crm, url + 'crm.html'));
write('activity.html', setHead(read('activity.html'), url + 'activity.html'));
if (!read('404.html').includes('/CRM/theme.css')) write('404.html', read('404.html').replace('</head>', '<link rel="stylesheet" href="/CRM/theme.css?v=3.0"></head>'));
write('suite.js', read('suite.js').replace('src="index.html?embedded=1', 'src="activity.html?embedded=1'));
for (const name of ['PAGE-MAP.md', 'CRM-RENEWAL-AUDIT.md', 'DESIGN-SYSTEM.md', 'VALIDATION.md', 'build-docs.cjs']) {
  const content = read(name).replaceAll('http://127.0.0.1:8937/crm.html', url + 'crm.html').replaceAll('http://127.0.0.1:8937/index.html', url + 'activity.html');
  write(name, content);
}
console.log('Prepared the dashboard entry, original activity page, relative paths and sharing metadata.');
