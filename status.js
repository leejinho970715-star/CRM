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
  const render = (value,context='') => {
    const label = String(value || '미확인');
    const kind = tone(label,context);
    return `<span class="state-badge status-${kind}" data-status-tone="${kind}">${escape(label)}</span>`;
  };
  const examples = [
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
  window.CRMStatus = Object.freeze({groups,vocabulary,contexts,examples,tone,render});
})();
