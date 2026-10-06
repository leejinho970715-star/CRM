const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const context={window:{}};
vm.runInNewContext(fs.readFileSync('status.js','utf8'),context);
const status=context.window.CRMStatus;
const cases=[['미진행','','neutral'],['미계약','','neutral'],['비활성','','neutral'],['영업종료','','neutral'],['실주','','neutral'],['취소','','neutral'],['미확인','','neutral'],['진행','','active'],['검토','','active'],['계약완료','','complete'],['활동 완료','','complete'],['이월','','attention'],['만료','','attention'],['유효','leads','active'],['유효','sslExpiration','complete'],['제안 시안','','neutral'],['새로 추가한 상태','','neutral']];
for(const [value,domain,tone] of cases)assert.equal(status.tone(value,domain),tone,value);
assert(!status.render('<img src=x onerror=alert(1)>').includes('<img'));
assert.equal(status.groups.length,4);
const expectedIcons={홈페이지:'globe',마케팅:'campaign',수동:'edit',높음:'up',보통:'normal',낮음:'down',신규:'new',접촉:'phone',유효:'verified',전환:'converted',진행:'progress'};
for(const [label,key] of Object.entries(expectedIcons))assert(status.icon(label).includes(`data-status-icon="${key}"`),label);
assert.equal(status.icon('새로 추가한 분류'),'');
assert(!status.icon('진행').includes('undefined'));
const css=fs.readFileSync('status.css','utf8');
const luminance=hex=>{const v=hex.slice(1).match(/../g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return v[0]*.2126+v[1]*.7152+v[2]*.0722;};
for(const group of status.groups){
  for(const field of ['fg','bg','border'])assert(css.toLowerCase().includes(`--status-${group.id}-${field}:${group[field].toLowerCase()}`));
  const ratio=(luminance(group.bg)+.05)/(luminance(group.fg)+.05);
  assert(ratio>=4.5,group.id+' contrast '+ratio);
  console.log(group.id+' text contrast '+ratio.toFixed(2)+':1');
}
vm.runInNewContext(fs.readFileSync('suite-data.js','utf8'),context);
const known=new Set(Object.values(status.vocabulary).flat());
for(const page of context.window.CRM_DESIGN.pages){for(const field of (page.form||[]).flatMap(g=>g.fields)){if(['status','priority','stage','budget'].includes(field.key))for(const value of field.options||[])assert(known.has(value),'Unmapped status: '+value);}}
console.log('17 ambiguous/domain status cases, escaping, token consistency, contrast and form status coverage passed.');
