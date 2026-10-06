/* Shared semantic status vocabulary. Unknown and informational labels stay neutral. */
(() => {
  'use strict';
  const groups = [
    { id:'neutral', name:'대기 · 종료 · 기본 정보', color:'뉴트럴', description:'아직 시작하지 않았거나 종료된 상태, 일상적인 운영 정보.', fg:'#626873', bg:'#F2F3F5', border:'#E3E5E9', examples:['미진행','신규','미계약','취소','영업종료'] },
    { id:'active', name:'진행 중', color:'블루 그레이', description:'상담·검토·처리가 실제로 진행 중인 상태.', fg:'#4B6082', bg:'#EEF2F7', border:'#DDE5EF', examples:['진행','접촉','관심 확인','검토','발주'] },
    { id:'complete', name:'완료 · 확정', color:'세이지', description:'완료되었거나 결과가 확정된 상태.', fg:'#486B5A', bg:'#EFF4F0', border:'#DFE9E2', examples:['완료','계약완료','계약 성사','전환','출고'] },
    { id:'attention', name:'확인 · 조치 필요', color:'샌드', description:'기한·우선순위·후속 확인 때문에 주의가 필요한 상태.', fg:'#846836', bg:'#F7F3EA', border:'#EBE2CF', examples:['기한 경과','이월','30일 내 만료','부재/미응답','긴급'] }
  ];
  const vocabulary = {
    neutral:['미진행','미계약','미선택','미확인','대기','예정','편성 예정','미편성','신규','영업종료','취소','실주','제외','중복','비활성','퇴사','중지','반품','등록','사용','활성','재직','기타','보통','낮음'],
    active:['진행','진행 중','관심','관심 확인','접촉','상담','제안','검토','발주','연결됨','견적 전달','후속 상담 예정','설립방침 수립','타당성 검토 준비','1차 협의','타당성 검토 시행','2차 협의'],
    complete:['완료','계약','계약완료','계약 완료','계약 성사','편성 완료','미팅 확정','자료 전달 완료','활동 완료','입고','출고','기관 설립','설립 승인','확인','갱신 완료','전환','유효'],
    attention:['기한 경과','만료','30일 내 만료','7일 내 만료','갱신 필요','확인 필요','부재/미응답','이월','높음','긴급','보류','실패','오류']
  };
  const tones = new Map(Object.entries(vocabulary).flatMap(([tone,labels]) => labels.map(label => [label,tone])));
  const contexts = { leads:{'유효':'active'} };
  const tone = (value,context='') => {
    const label = String(value ?? '').trim();
    return contexts[context]?.[label] || tones.get(label) || 'neutral';
  };
  const escape = value => String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  // Icon meaning follows the label; color still follows the four semantic tones.
  const iconPaths = {
    globe:'<circle cx="8" cy="8" r="6"/><ellipse cx="8" cy="8" rx="2.5" ry="6"/><path d="M2 8h12"/>',
    campaign:'<path d="M2 6h3l8-3v10l-8-3H2V6ZM5 6v4M5 10l1 4h3l-1-3"/>',
    edit:'<path d="m3 10 7-7 3 3-7 7H3v-3Zm6-6 3 3"/>',
    up:'<path d="M8 13V3m-4 4 4-4 4 4"/>',
    normal:'<path d="M4 6h8M4 10h8"/>',
    down:'<path d="M8 3v10m-4-4 4 4 4-4"/>',
    urgent:'<path d="m8 2 6 11H2L8 2ZM8 6v3m0 2v.1"/>',
    new:'<path d="m8 2 1.7 4.3L14 8l-4.3 1.7L8 14l-1.7-4.3L2 8l4.3-1.7L8 2Z"/>',
    phone:'<path d="M5 2H3a1 1 0 0 0-1 1c0 6 5 11 11 11a1 1 0 0 0 1-1v-2l-3-1-2 2-5-5 2-2-1-3Z"/>',
    conversation:'<path d="M3 3h10v8H7l-4 3V3ZM6 6h4M6 8h3"/>',
    verified:'<path d="m8 2 5 2v4c0 3-5 6-5 6s-5-3-5-6V4l5-2Zm-2 6 1.5 1.5L10 6"/>',
    converted:'<circle cx="8" cy="8" r="6"/><path d="M4 8h8m-3-3 3 3-3 3"/>',
    progress:'<path d="M12.5 4A6 6 0 1 0 14 8M12 2v4h-4"/>',
    pause:'<circle cx="8" cy="8" r="6"/><path d="M6 5v6M10 5v6"/>',
    calendar:'<rect x="2" y="3" width="12" height="11" rx="2"/><path d="M5 2v3M11 2v3M2 7h12"/>',
    inspect:'<circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 3 3"/>',
    file:'<path d="M9 2H3v12h10V6L9 2ZM9 2v4h4M5 9h5M5 11h3"/>',
    copy:'<rect x="6" y="6" width="8" height="8" rx="1"/><path d="M10 6V2H2v8h4"/>',
    cancel:'<circle cx="8" cy="8" r="6"/><path d="m5.5 5.5 5 5m0-5-5 5"/>',
    check:'<path d="m3.5 8 3 3 6-6"/>',
    alert:'<path d="M8 4v5m0 3v.1"/><circle cx="8" cy="8" r="6"/>',
    carryover:'<path d="M2 5h9a3 3 0 0 1 0 6H6m3-3-3 3 3 3M2 2v3h3"/>',
    incoming:'<path d="M8 2v8m-3-3 3 3 3-3M3 11v3h10v-3"/>',
    outgoing:'<path d="M8 10V2m-3 3 3-3 3 3M3 11v3h10v-3"/>',
    flag:'<path d="M3 14V2h9l-2 3 2 3H3"/>'
  };
  const labelIcons = {
    '홈페이지':'globe','마케팅':'campaign','수동':'edit',
    '높음':'up','보통':'normal','낮음':'down','긴급':'urgent',
    '신규':'new','접촉':'phone','연결됨':'phone','상담':'conversation','후속 상담 예정':'conversation',
    '유효':'verified','전환':'converted','미진행':'pause','대기':'pause','중지':'pause','보류':'pause',
    '진행':'progress','진행 중':'progress','관심':'inspect','관심 확인':'inspect','검토':'inspect',
    '제안':'file','견적 전달':'outgoing','미계약':'file','이월':'carryover','반품':'carryover',
    '취소':'cancel','실주':'cancel','제외':'cancel','영업종료':'cancel','퇴사':'cancel','비활성':'cancel','중복':'copy',
    '예정':'calendar','편성 예정':'calendar','미팅 확정':'calendar','30일 내 만료':'calendar','7일 내 만료':'calendar','기한 경과':'calendar','만료':'calendar',
    '입고':'incoming','출고':'outgoing','발주':'file','활성':'verified','사용':'verified','재직':'verified','등록':'file',
    '미편성':'file','미선택':'inspect','미확인':'inspect','확인 필요':'inspect','갱신 필요':'carryover','부재/미응답':'phone',
    '설립방침 수립':'file','타당성 검토 준비':'inspect','타당성 검토 시행':'inspect','1차 협의':'conversation','2차 협의':'conversation'
  };
  const icon = (value,context='') => {
    const label=String(value ?? '').trim();
    const name=labelIcons[label] || ({active:'progress',complete:'check',attention:'alert'}[tone(label,context)]);
    if(!name)return ''; // Pure informational and unknown labels do not imply a workflow status.
    return `<svg class="status-icon" data-status-icon="${name}" viewBox="0 0 16 16" aria-hidden="true" focusable="false">${iconPaths[name]}</svg>`;
  };
  const render = (value,context='') => {
    const label = String(value || '미확인');
    const kind = tone(label,context);
    return `<span class="state-badge status-${kind}" data-status-tone="${kind}">${icon(label,context)}${escape(label)}</span>`;
  };
  const examples = [
    {name:'유입경로',context:'source',values:['홈페이지','마케팅','수동']},
    {name:'고객·영업',context:'customers',values:['미진행','진행','이월','계약완료','영업종료']},
    {name:'업무',context:'tasks',values:['진행','완료','취소','기한 경과']},
    {name:'우선순위',context:'priority',values:['낮음','보통','높음','긴급']},
    {name:'리드',context:'leads',values:['신규','접촉','상담','유효','전환','제외','중복']},
    {name:'처리 결과',context:'activities',values:['연결됨','부재/미응답','관심 확인','견적 전달','미팅 확정','계약 성사','실주','기타']},
    {name:'견적·포캐스팅',context:'quotes',values:['제안','검토','미계약','계약','이월','실주']},
    {name:'SSL·구매',context:'sslExpiration',values:['발주','입고','출고','반품','유효','30일 내 만료','만료','미확인','확인']},
    {name:'비영리·예산',context:'nonprofits',values:['설립방침 수립','1차 협의','설립 승인','기관 설립','미편성','편성 예정','편성 완료']},
    {name:'관리·인사',context:'members',values:['사용','활성','비활성','재직','퇴사']}
  ];
  window.CRMStatus = Object.freeze({groups,vocabulary,contexts,examples,tone,icon,render});
})();
