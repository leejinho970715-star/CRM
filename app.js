(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const seedCustomers = [
    { id:'DEMO001',name:'샘플 고객사 01',business:'000-00-00001',owner:'user_2',status:'미진행',product:'Smart A',last:'2026-10-02',note:'첫 상담을 기다리고 있어요' },
    { id:'DEMO002',name:'샘플 고객사 02',business:'000-00-00002',owner:'user_1',status:'진행',product:'WEHAGO',last:'2026-10-01',note:'제안서 검토 · 다음 미팅 조율' },
    { id:'DEMO003',name:'샘플 고객사 03',business:'000-00-00003',owner:'user_1',status:'진행',product:'iCUBE',last:'2026-09-30',note:'도입 범위 협의 중' },
    { id:'DEMO004',name:'샘플 고객사 04',business:'000-00-00004',owner:'user_3',status:'진행',product:'WEHAGO',last:'2026-09-29',note:'제품 시연 완료' },
    { id:'DEMO005',name:'샘플 고객사 05',business:'000-00-00005',owner:'user_1',status:'진행',product:'iCUBE',last:'2026-09-28',note:'견적 조건 확인 필요' },
    { id:'DEMO006',name:'샘플 고객사 06',business:'000-00-00006',owner:'user_2',status:'진행',product:'Smart A',last:'2026-09-27',note:'후속 연락 예정' },
    { id:'DEMO007',name:'샘플 고객사 07',business:'000-00-00007',owner:'user_3',status:'진행',product:'WEHAGO',last:'2026-09-26',note:'내부 검토 중' },
    { id:'DEMO008',name:'샘플 고객사 08',business:'000-00-00008',owner:'user_1',status:'진행',product:'iCUBE',last:'2026-09-25',note:'계약 일정 협의 중' },
    { id:'DEMO009',name:'샘플 고객사 09',business:'000-00-00009',owner:'user_2',status:'진행',product:'Smart A',last:'2026-09-24',note:'요구사항 정리 중' },
    { id:'DEMO010',name:'샘플 고객사 10',business:'000-00-00010',owner:'user_3',status:'진행',product:'WEHAGO',last:'2026-09-23',note:'도입 일정 확인 필요' }
  ];
  const storageKey = 'ione-crm-renewal-demo-v1';
  let stored = {};
  try { stored = JSON.parse(localStorage.getItem(storageKey) || '{}'); } catch { /* File mode may restrict storage. */ }
  let customers = Array.isArray(stored.customers) && stored.customers.length ? stored.customers : seedCustomers;
  const activities = stored.activities || {};
  const drafts = stored.drafts || {};
  const forecasts = stored.forecasts || {};
  const quotes = stored.quotes || {};
  let selectedId = customers.some(c => c.id === stored.selectedId) ? stored.selectedId : 'DEMO002';
  let activeTab = 'register';
  let dirty = false;
  let pendingCustomer = null;
  let toastTimer;
  let applied = {};
  let listPage = 1;
  const pageSize = 5;
  const productNames = ['Amaranth10','Amaranth10 Cloud','Bizbox Alpha','Bizbox Alpha Cloud','ERP 10','iCUBE','iCUBE G20','iU','OmniEsol','PMS','SI(개발)','Smart A','Smart A Cloud','WEHAGO','WEHAGO T'];
  const embedParams=new URLSearchParams(location.search);
  const embedded=embedParams.get('embedded')==='1';
  if(embedded)document.body.classList.add('embedded');
  const validOwner=name=>/^user_[123]$/.test(name)?name:'user_1';
  customers.forEach(c=>{c.owner=validOwner(c.owner);});
  Object.values(activities).filter(Array.isArray).forEach(list=>list.forEach(a=>{a.author=validOwner(a.author);}));
  Object.values(drafts).forEach(d=>{d.author=validOwner(d.author);});
  if(customers.some(c=>c.id===embedParams.get('customer')))selectedId=embedParams.get('customer');
  let selectedProducts = [];
  let attachmentItems = [];
  const fileMemory = new Map();
  const fileUrls = new Map();
  let fileDb;
  function openFileDb() {
    if (!fileDb) fileDb = new Promise((resolve,reject) => {
      const request = indexedDB.open('ione-crm-demo-files',1);
      request.onupgradeneeded = () => request.result.createObjectStore('files');
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    return fileDb;
  }
  async function storeFile(id,file) {
    const db = await openFileDb();
    await new Promise((resolve,reject) => {
      const transaction = db.transaction('files','readwrite');
      transaction.objectStore('files').put(file,id);
      transaction.oncomplete = resolve;
      transaction.onerror = () => reject(transaction.error);
      transaction.onabort = () => reject(transaction.error);
    });
  }
  async function getFile(id) {
    let file = fileMemory.get(id);
    if (!file) {
      try {
        const db = await openFileDb();
        file = await new Promise((resolve,reject) => {
          const request = db.transaction('files').objectStore('files').get(id);
          request.onsuccess = () => resolve(request.result);request.onerror = () => reject(request.error);
        });
      } catch { /* Fall back to files from this session. */ }
    }
    return file;
  }
  async function prepareFileLink(link) {
    const id = link.dataset.downloadFile;
    const file = await getFile(id);
    if (!file || !link.isConnected) return;
    if (!fileUrls.has(id)) fileUrls.set(id,URL.createObjectURL(file));
    link.href = fileUrls.get(id);link.download = link.dataset.filename;
    link.dataset.available = 'true';link.removeAttribute('aria-busy');
  }
  const activityForm = $('activity-form');
  const customer = () => customers.find(c => c.id === selectedId);
  const escape = (value) => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function persist() {
    try {
      localStorage.setItem(storageKey, JSON.stringify({ customers, activities, drafts, forecasts, quotes, selectedId }));
      return true;
    } catch { toast('현재 브라우저에서는 임시 저장이 이번 실행 동안만 유지됩니다.'); return false; }
  }
  function toast(message) {
    clearTimeout(toastTimer);
    $('toast').textContent = message;
    $('toast').hidden = false;
    toastTimer = setTimeout(() => { $('toast').hidden = true; }, 3600);
  }
  function readActivity() {
    const value = Object.fromEntries(new FormData(activityForm));
    value.followup = Boolean(value.nextTask.trim());
    value.products = [...selectedProducts];
    value.attachments = attachmentItems.map(a => ({...a}));
    return value;
  }
  function markDirty() {
    dirty = true;
    $('draft-state').innerHTML = '<span class="small-dot"></span>저장하지 않은 변경사항';
  }
  function renderProductOptions() {
    const term = $('product-search').value.toLowerCase();
    $('product-checklist').innerHTML = productNames.filter(p => p.toLowerCase().includes(term)).map(p => `<label class="product-option"><input type="checkbox" value="${escape(p)}" ${selectedProducts.includes(p) ? 'checked' : ''}>${escape(p)}</label>`).join('') || '<div class="empty-state">검색 결과가 없습니다.</div>';
    $('product-checklist').querySelectorAll('input').forEach(input => input.addEventListener('change', () => {
      selectedProducts = input.checked ? [...selectedProducts,input.value] : selectedProducts.filter(p => p !== input.value);
      renderProductSummary();markDirty();
    }));
  }
  function renderProductSummary() {
    $('product-summary').textContent = selectedProducts.length ? selectedProducts.join(', ') : '품목을 선택하세요';
    $('product-trigger').classList.toggle('has-products',Boolean(selectedProducts.length));
    $('product-trigger').title = selectedProducts.join(', ');
  }
  function closeProducts() { $('product-options').hidden = true;$('product-trigger').setAttribute('aria-expanded','false'); }
  function renderAttachments() {
    $('attachment-count').textContent = attachmentItems.length ? `${attachmentItems.length}개 파일` : '선택한 파일 없음';
    $('file-list').innerHTML = attachmentItems.map(a => `<div class="file-row"><svg><use href="#i-file"/></svg><span title="${escape(a.name)}">${escape(a.name)}</span><span class="file-size">${a.size >= 1048576 ? (a.size/1048576).toFixed(1)+' MB' : Math.max(1,Math.round(a.size/1024))+' KB'}</span><button type="button" class="icon-button" data-remove-file="${escape(a.id)}" aria-label="${escape(a.name)} 첨부 삭제"><svg><use href="#i-close"/></svg></button></div>`).join('');
    $('file-list').querySelectorAll('[data-remove-file]').forEach(button => button.addEventListener('click', () => {
      attachmentItems = attachmentItems.filter(a => a.id !== button.dataset.removeFile);renderAttachments();markDirty();
    }));
  }
  async function addFiles(files) {
    const writes = [];
    for (const file of files) {
      if (attachmentItems.some(a => a.name === file.name && a.size === file.size)) continue;
      const id = crypto.randomUUID();
      fileMemory.set(id,file);
      attachmentItems.push({id,name:file.name,size:file.size});
      writes.push(storeFile(id,file));
    }
    if (!writes.length) return;
    renderAttachments();markDirty();$('file-input').value = '';
    const results = await Promise.allSettled(writes);
    if (results.some(result => result.status === 'rejected')) toast('일부 파일은 이번 실행 동안 보관됩니다. 브라우저 저장 공간을 확인해주세요.');
  }
  function linksIn(text) { return text.match(/https?:\/\/[^\s<>"']+/g) || []; }
  function mailLabel(url) {
    try { const value = new URL(url);return /amaranth|bizbox/i.test(value.hostname) ? '아마란스 메일 ↗' : '참고 링크 ↗'; } catch { return '참고 링크 ↗'; }
  }
  function renderMailLinks() {
    const links = [...new Set(linksIn(activityForm.elements.content.value))];
    $('mail-link-preview').hidden = !links.length;
    $('mail-link-preview').innerHTML = links.map(url => `<a href="${escape(url)}" target="_blank" rel="noopener noreferrer" title="${escape(url)}">${mailLabel(url)}</a>`).join('');
  }
  function linkedContent(value) {
    return value.split(/(https?:\/\/[^\s<>"']+)/g).map(part => /^https?:\/\//.test(part) ? `<a class="history-link" href="${escape(part)}" target="_blank" rel="noopener noreferrer" title="${escape(part)}">${mailLabel(part)}</a>` : escape(part)).join('');
  }
  function loadDraft() {
    activityForm.reset();
    const draft = drafts[selectedId];
    if (draft) {
      Object.entries(draft).forEach(([key,value]) => {
        const field = activityForm.elements.namedItem(key);
        if (field && key !== 'followup') field.value = value;
      });
    }
    selectedProducts = Array.isArray(draft?.products) ? [...draft.products] : [];
    attachmentItems = Array.isArray(draft?.attachments) ? draft.attachments.map(a => ({...a})) : [];
    renderProductSummary();renderProductOptions();renderAttachments();renderMailLinks();closeProducts();
    $('content-length').textContent = activityForm.elements.content.value.length;
    $('draft-state').innerHTML = '<span class="small-dot"></span>' + (draft ? '임시 저장한 내용을 불러왔어요' : '새 활동 작성 중');
    dirty = false;
  }
  function saveDraft(notify = true) {
    drafts[selectedId] = readActivity();
    const durable = persist();
    dirty = false;
    $('draft-state').innerHTML = '<span class="small-dot"></span>임시 저장 완료';
    if (notify && durable) toast('임시 저장했어요. 이 브라우저에서 이어서 작성할 수 있습니다.');
  }
  function records(id) {
    if (activities[id]) return activities[id];
    if (id !== 'DEMO002') return [];
    return [
      {date:'2026-10-01T14:30',title:'WEHAGO 도입 제안서 전달',type:'이메일',subtype:'제안서',author:'user_1',result:'자료 전달 완료',content:'병원 회계 업무의 전환 범위와 사용 인원 기준을 정리한 제안서를 전달했습니다. 내부 검토 후 다음 주에 도입 일정을 협의하기로 했습니다.',nextTask:'제안서 검토 의견 및 미팅 가능 시간 확인',nextDate:'2026-10-05',followup:true},
      {date:'2026-09-28T11:00',title:'회계 담당자 대상 제품 시연',type:'온라인 미팅',subtype:'시연',author:'user_1',result:'후속 상담 예정',content:'회계 담당자와 세무 자료 공유 및 결재 흐름을 시연했습니다. 기존 데이터 이관 방법과 사용자 권한에 대한 추가 설명을 요청했습니다.'},
      {date:'2026-09-25T10:00',title:'신규 도입 요구사항 확인',type:'TM',subtype:'상담',author:'user_1',result:'활동 완료',content:'현행 회계 업무와 조직 구성을 확인했습니다. 업무별 계정 권한과 초기 설정 지원이 필요합니다.'}
    ];
  }
  function badgeClass(status) { return status === '진행' ? 'progress' : status === '완료' ? 'done' : 'pending'; }
  function renderCustomers() {
    const clean = s => s.replace(/[^0-9]/g, '');
    let list = customers.filter(c => (!applied.name || (c.name+' '+c.id).toLowerCase().includes(applied.name.toLowerCase())) && (!applied.business || clean(c.business).includes(clean(applied.business))) && (!applied.owner || c.owner === applied.owner) && (!applied.status || c.status === applied.status) && (!applied.product || c.product === applied.product) && (!applied.from || c.last >= applied.from) && (!applied.to || c.last <= applied.to));
    list = [...list].sort($('sort-order').value === 'name' ? (a,b) => a.name.localeCompare(b.name,'ko') : (a,b) => b.last.localeCompare(a.last) || b.id.localeCompare(a.id));
    $('customer-count').textContent = list.length;
    const pages = Math.max(1,Math.ceil(list.length/pageSize));
    listPage = Math.min(listPage,pages);
    const visible = list.slice((listPage-1)*pageSize,listPage*pageSize);
    $('customer-pagination').innerHTML = `<button type="button" data-page="${listPage-1}" aria-label="이전 페이지" ${listPage===1 ? 'disabled' : ''}>‹</button>${Array.from({length:pages},(_,i) => `<button type="button" data-page="${i+1}" ${i+1===listPage ? 'aria-current="page"' : ''} aria-label="${i+1}페이지">${i+1}</button>`).join('')}<button type="button" data-page="${listPage+1}" aria-label="다음 페이지" ${listPage===pages ? 'disabled' : ''}>›</button><span>${list.length ? (listPage-1)*pageSize+1 : 0}–${Math.min(listPage*pageSize,list.length)} / ${list.length}</span>`;
    $('customer-pagination').querySelectorAll('[data-page]').forEach(button => button.addEventListener('click', () => { listPage = Number(button.dataset.page);renderCustomers(); }));
    $('customer-list').innerHTML = visible.length ? visible.map(c => `<button class="customer-row${selectedId === c.id ? ' selected' : ''}" data-customer="${escape(c.id)}" aria-pressed="${selectedId === c.id}"><div class="row-top"><span class="row-name" title="${escape(c.name)}">${escape(c.name)}</span><span class="badge ${badgeClass(c.status)}">${escape(c.status)}</span></div><div class="row-meta"><span>${escape(c.id)}</span><span>${escape(c.business)}</span></div><div class="row-foot">${escape(c.note)}</div></button>`).join('') : '<div class="empty-state">검색 결과가 없습니다.<br>검색어 또는 필터를 변경해주세요.</div>';
    $('customer-list').querySelectorAll('[data-customer]').forEach(button => button.addEventListener('click', () => requestCustomer(button.dataset.customer)));
  }
  function renderHistory() {
    const list = [...records(selectedId)].sort((a,b) => b.date.localeCompare(a.date));
    $('history-count').textContent = list.length;
    $('history-list').innerHTML = list.length ? list.map(a => `<article class="history-entry"><div class="history-date"><span>${escape(a.date.replace('T',' · '))}</span><span>${escape(a.author)}</span></div><h3>${escape(a.title)}</h3><p>${linkedContent(a.content)}</p><div class="history-tags"><span>${escape(a.type)}</span><span>${escape(a.subtype)}</span>${a.contact ? `<span>고객 담당자: ${escape(a.contact)}</span>` : ''}${a.result ? `<span>${escape(a.result)}</span>` : ''}${(a.products || []).map(p => `<span>${escape(p)}</span>`).join('')}</div>${a.followup ? `<div class="history-next">다음 행동 · ${escape((a.nextDate || '').replace('T',' '))} &nbsp; ${escape(a.nextTask)}</div>` : ''}${a.attachments?.length ? `<div class="history-attachments">${a.attachments.map(f => `<a href="#" aria-busy="true" data-download-file="${escape(f.id)}" data-filename="${escape(f.name)}"><svg><use href="#i-file"/></svg>${escape(f.name)} ↓</a>`).join('')}</div>` : ''}</article>`).join('') : '<div class="empty-state">아직 등록한 활동이 없어요.<br>첫 번째 상담 내용을 기록해보세요.</div>';
    $('history-list').querySelectorAll('[data-download-file]').forEach(link => {
      prepareFileLink(link);
      link.addEventListener('click',event => { if (link.dataset.available !== 'true') {event.preventDefault();toast('첨부 원본을 준비 중입니다. 파일이 보관되지 않았다면 다시 첨부해주세요.');} });
    });
  }
  function renderSelection() {
    const c = customer();
    $('selected-name').textContent = c.name;
    $('selected-code').textContent = c.id;
    $('selected-business').textContent = c.business;
    $('selected-owner').textContent = c.owner;
    $('selected-product').textContent = c.product;
    $('customer-initial').textContent = c.name.replace(/^\(주\)|^주식회사\s*/g,'').charAt(0);
    $('selected-status').textContent = c.status;
    $('selected-status').className = 'badge '+badgeClass(c.status);
    renderHistory();
    loadDraft();
    const forecast = forecasts[selectedId];
    $('forecast-form').reset();
    if (forecast) Object.entries(forecast).forEach(([key,value]) => { if ($('forecast-form').elements[key]) $('forecast-form').elements[key].value = value; });
    $('quote-form').reset();
    $('quote-form').elements.product.value = c.product;
    renderQuote(quotes[selectedId]);
    renderCustomers();
  }
  function chooseCustomer(id) {
    selectedId = id;
    renderSelection();
    persist();
  }
  function requestCustomer(id) {
    if (id === selectedId) return;
    if (dirty) { pendingCustomer = id; $('unsaved-dialog').showModal(); }
    else chooseCustomer(id);
  }
  function switchTab(name) {
    closeProducts();
    activeTab = name;
    document.querySelectorAll('[data-tab]').forEach(button => {
      button.setAttribute('aria-selected', String(button.dataset.tab === name));
      button.tabIndex = button.dataset.tab === name ? 0 : -1;
    });
    ['register','history','quote','forecast'].forEach(key => { $('panel-'+key).hidden = key !== name; });
    if (name === 'history') renderHistory();
  }
  function setAi(open) {
    $('ai-panel').hidden = !open;
    $('ai-button').setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('ai-open',open);
  }
  function renderQuote(value) {
    $('quote-preview').hidden = !value;
    if (!value) return;
    $('quote-preview').innerHTML = `<h3>${escape(customer().name)} · 견적 요청 초안</h3><p>제안 제품: ${escape(value.product)}<br>사용 인원: ${escape(value.people)}명</p><p>${escape(value.requirements)}</p><p class="sample-label">UI 시안에서는 요청 내용만 정리합니다. 가격 산출 및 AI 생성은 실제 시스템 연동이 필요합니다.</p>`;
  }
  $('search-form').addEventListener('submit', event => {
    event.preventDefault();
    const from = $('search-from').value, to = $('search-to').value;
    if (from && to && from > to) { toast('종료일은 시작일 이후로 선택해주세요.'); return; }
    applied = {name:$('search-name').value.trim(),business:$('search-business').value.trim(),owner:$('search-owner').value,status:$('search-status').value,product:$('search-product').value,from,to};
    if (applied.business && !/^[\d\s-]+$/.test(applied.business)) { toast('사업자등록번호는 숫자와 하이픈으로 입력해주세요.'); return; }
    listPage = 1;
    renderCustomers();
    const labels = {name:'검색',business:'사업자번호',owner:'담당자',status:'상태',product:'제품',from:'시작일',to:'종료일'};
    const entries = Object.entries(applied).filter(([,value]) => value);
    $('applied-filters').hidden = !entries.length;
    $('applied-filters').innerHTML = entries.map(([key,value]) => `<span>${labels[key]}: ${escape(value)}</span>`).join('');
    const extraCount = ['status','product','from','to'].filter(key => applied[key]).length;
    $('filter-count').hidden = !extraCount;
    $('filter-count').textContent = extraCount;
  });
  $('detail-filter').addEventListener('click', () => {
    const expanded = $('extra-filters').hidden;
    $('extra-filters').hidden = !expanded;
    $('detail-filter').setAttribute('aria-expanded',String(expanded));
  });
  $('reset-filter').addEventListener('click', () => {
    $('search-form').reset();applied = {};listPage = 1;
    $('applied-filters').hidden = true;$('filter-count').hidden = true;
    renderCustomers();
  });
  $('sort-order').addEventListener('change', () => {listPage = 1;renderCustomers();});
  document.querySelectorAll('[data-tab]').forEach(button => {
    button.addEventListener('click', () => switchTab(button.dataset.tab));
    button.addEventListener('keydown',event => {
      const tabs = [...document.querySelectorAll('[data-tab]')];
      if (['ArrowRight','ArrowLeft','Home','End'].includes(event.key)) {
        event.preventDefault();
        const delta = event.key === 'ArrowLeft' ? -1 : 1;
        const index = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (tabs.indexOf(button)+delta+tabs.length)%tabs.length;
        switchTab(tabs[index].dataset.tab);tabs[index].focus();
      }
    });
  });
  activityForm.addEventListener('input', () => {
    markDirty();
    $('content-length').textContent = activityForm.elements.content.value.length;
    renderMailLinks();
  });
  $('draft-button').addEventListener('click', () => saveDraft());
  activityForm.addEventListener('submit',event => {
    event.preventDefault();
    const value = readActivity();
    if (!value.title.trim() || !value.content.trim() || (value.followup && !value.nextTask.trim())) { toast('필수 항목에 내용을 입력해주세요.'); return; }
    value.id='ACT-'+Date.now();
    if (value.nextDate && !value.nextTask.trim()) { toast('기한에 해당하는 다음 행동을 입력해주세요.');return; }
    const list = [...records(selectedId)];
    list.unshift(value);activities[selectedId] = list;
    delete drafts[selectedId];
    const c = customer();c.last = [c.last,value.date.slice(0,10)].sort().at(-1);c.note = value.title;
    const durable = persist();
    loadDraft();renderHistory();renderCustomers();
    switchTab('history');
    if(embedded)parent.postMessage({type:'crm-activity-saved',activity:{...value,customerName:c.name}},location.origin);
    if (durable) toast('활동을 저장했어요. 활동 이력에서 확인할 수 있습니다.');
  });
  $('new-activity').addEventListener('click', () => switchTab('register'));
  $('focus-button').addEventListener('click', () => {
    const enabled = !document.body.classList.contains('focus-mode');
    document.body.classList.toggle('focus-mode',enabled);
    $('focus-button').setAttribute('aria-pressed',String(enabled));
    $('focus-button').innerHTML = `<svg><use href="#i-focus"/></svg>${enabled ? '고객 목록 보기' : '집중 입력'}`;
    if (enabled) setAi(false);
  });
  $('ai-button').addEventListener('click', () => setAi($('ai-panel').hidden));
  $('close-ai').addEventListener('click', () => { setAi(false);$('ai-button').focus(); });
  $('ai-recommendations').innerHTML = seedCustomers.filter(c => c.status === '진행').slice(0,5).map((c,i) => `<div class="ai-recommendation"><strong>${escape(c.name)}</strong><span>${['제안서 검토 이후 연락을 준비하세요.','도입 범위와 일정을 확인하세요.','시연 이후 고객 의견을 확인하세요.','견적 조건을 다시 확인하세요.','다음 상담 일정을 조율하세요.'][i]}</span><button type="button" data-ai-customer="${c.id}">고객 활동 확인 <svg><use href="#i-arrow"/></svg></button></div>`).join('');
  document.querySelectorAll('[data-ai-customer]').forEach(button => button.addEventListener('click', () => {
    document.body.classList.remove('focus-mode');$('focus-button').setAttribute('aria-pressed','false');$('focus-button').innerHTML = '<svg><use href="#i-focus"/></svg>집중 입력';
    requestCustomer(button.dataset.aiCustomer);setAi(false);
  }));
  $('add-customer').addEventListener('click', () => { $('customer-form').reset();$('customer-dialog').showModal(); });
  ['close-customer','cancel-customer'].forEach(id => $(id).addEventListener('click', () => $('customer-dialog').close()));
  $('customer-form').addEventListener('submit',event => {
    event.preventDefault();const value = Object.fromEntries(new FormData(event.target));
    const id = value.code.trim(), name = value.name.trim();
    if (!id || !name) { toast('고객사명과 거래처코드를 입력해주세요.');return; }
    if (customers.some(c => c.id.toLowerCase() === id.toLowerCase() || c.business.replace(/-/g,'') === value.business.replace(/-/g,''))) { toast('이미 등록된 거래처코드 또는 사업자등록번호입니다.');return; }
    customers.push({id,name,business:value.business.replace(/^(\d{3})-?(\d{2})-?(\d{5})$/,'$1-$2-$3'),owner:value.owner,product:value.product,status:'미진행',last:'2026-10-02',note:'첫 활동을 기록해보세요'});
    persist();$('customer-dialog').close();$('reset-filter').click();renderCustomers();requestCustomer(id);toast('새 고객사를 추가했어요.');
  });
  $('stay-customer').addEventListener('click', () => { pendingCustomer = null;$('unsaved-dialog').close(); });
  $('discard-customer').addEventListener('click', () => { delete drafts[selectedId];chooseCustomer(pendingCustomer);pendingCustomer = null;$('unsaved-dialog').close(); });
  $('save-move').addEventListener('click', () => { saveDraft(false);chooseCustomer(pendingCustomer);pendingCustomer = null;$('unsaved-dialog').close();toast('작성 내용을 임시 저장하고 고객을 변경했어요.'); });
  $('unsaved-dialog').addEventListener('cancel', () => { pendingCustomer = null; });
  $('quote-form').addEventListener('submit',event => {
    event.preventDefault();quotes[selectedId] = Object.fromEntries(new FormData(event.target));persist();renderQuote(quotes[selectedId]);toast('견적 요청 초안을 준비했어요.');
  });
  $('forecast-form').addEventListener('submit',event => {
    event.preventDefault();forecasts[selectedId] = Object.fromEntries(new FormData(event.target));if (persist()) toast('포캐스팅을 저장했어요.');
  });
  document.querySelectorAll('.side-nav button').forEach(button => button.addEventListener('click', () => toast('이 시안은 영업활동 관리 페이지를 중심으로 구현되어 있습니다.')));
  document.querySelector('.brand').addEventListener('click',event => { event.preventDefault();window.scrollTo({top:0,behavior:'smooth'}); });
  $('product-trigger').addEventListener('click', () => {
    const open = $('product-options').hidden;
    $('product-options').hidden = !open;$('product-trigger').setAttribute('aria-expanded',String(open));
    if (open) {renderProductOptions();$('product-search').focus();}
  });
  $('product-search').addEventListener('input',renderProductOptions);
  $('product-done').addEventListener('click', () => {closeProducts();$('product-trigger').focus();});
  document.addEventListener('click',event => { if (!event.target.closest('.product-picker')) closeProducts(); });
  $('choose-files').addEventListener('click', () => $('file-input').click());
  $('file-input').addEventListener('change',event => addFiles(event.target.files));
  ['dragenter','dragover'].forEach(name => $('file-dropzone').addEventListener(name,event => { event.preventDefault();$('file-dropzone').classList.add('drag-over'); }));
  ['dragleave','drop'].forEach(name => $('file-dropzone').addEventListener(name,event => { event.preventDefault();$('file-dropzone').classList.remove('drag-over'); }));
  $('file-dropzone').addEventListener('drop',event => addFiles(event.dataTransfer.files));
  document.addEventListener('keydown',event => { if (event.key === 'Escape') {closeProducts();if (!$('ai-panel').hidden) setAi(false);} });
  window.addEventListener('beforeunload',event => { if (dirty) {event.preventDefault();event.returnValue = ''; } });
  renderSelection();switchTab(activeTab);
  if(embedded){
    ['search-product'].forEach(id=>{$(id).innerHTML='<option value="">전체</option>'+productNames.map(p=>`<option>${p}</option>`).join('');});
    document.querySelectorAll('#customer-form select[name="product"],#quote-form select[name="product"]').forEach(el=>el.innerHTML=productNames.map(p=>`<option>${p}</option>`).join(''));
    new ResizeObserver(()=>parent.postMessage({type:'crm-activity-height',height:document.documentElement.scrollHeight},location.origin)).observe(document.body);
    $('tab-forecast').addEventListener('click',()=>parent.postMessage({type:'crm-suite-route',route:'forecast-add'},location.origin));
  }
})();
