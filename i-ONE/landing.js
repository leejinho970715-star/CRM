(() => {
  'use strict';
  const tabs = [...document.querySelectorAll('[data-product]')];
  const panels = [...document.querySelectorAll('.product-panel')];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  let active = 'omniesol', motion = null, opener = null;
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);
  const topOffset = () => document.querySelector('.site-header').offsetHeight + document.querySelector('.solution-tabs-shell').offsetHeight;
  function jumpTo(element) { element.scrollIntoView({behavior:'instant',block:'start'}); }
  function setupMotion(panel) {
    if (motion) { motion.revert(); motion = null; }
    panels.forEach(p=>p.querySelector('.product-intro').classList.remove('motion-enabled'));
    if (!hasGsap || reduced.matches) return;
    motion = gsap.matchMedia();
    motion.add({desktop:'(min-width:861px)',mobile:'(max-width:860px)',motion:'(prefers-reduced-motion:no-preference)'}, context => {
      if (!context.conditions.motion) return;
      const stage = panel.querySelector('[data-motion-stage]');
      const intro = stage.parentElement;
      intro.classList.add('motion-enabled');
      const asset = stage.querySelector('.stage-asset');
      const copy = stage.querySelector('.stage-copy');
      const progress = stage.querySelector('.stage-progress span');
      const desktop = context.conditions.desktop;
      const timeline = gsap.timeline({scrollTrigger:{id:'product-intro',trigger:intro,start:()=>`top ${topOffset()}`,end:()=>`+=${intro.offsetHeight-stage.offsetHeight}`,scrub:.25,invalidateOnRefresh:true}});
      timeline.fromTo(asset,{scale:.22,x:desktop?-150:0,y:desktop?35:12,rotation:-13},{scale:1,x:0,y:0,rotation:0,duration:.65,ease:'power2.out'},0)
        .fromTo(copy,{autoAlpha:0,y:22},{autoAlpha:1,y:0,duration:.25,ease:'power1.out'},.66)
        .fromTo(progress,{scaleX:0},{scaleX:1,duration:1.2,ease:'none'},0)
        .to({}, {duration:.35});
      // Native sticky owns layout in both directions; GSAP only animates the art.
      return ()=>intro.classList.remove('motion-enabled');
    });
    ScrollTrigger.refresh();
  }
  function selectProduct(id, {navigate = true, focus = false} = {}) {
    const panel = panels.find(p => p.dataset.id === id);
    if (!panel) return;
    if (motion) { motion.revert(); motion = null; }
    active = id;
    panels.forEach(p => p.hidden = p !== panel);
    tabs.forEach(t => {const selected=t.dataset.product===id;t.setAttribute('aria-selected',String(selected));t.tabIndex=selected?0:-1;});
    setupMotion(panel);
    if (navigate) {
      history.replaceState(null,'',`#${id}`);
      const intro = panel.querySelector('.product-intro');
      window.scrollTo({top:intro.getBoundingClientRect().top+scrollY-topOffset(),behavior:'instant'});
    }
    if (focus) tabs.find(t=>t.dataset.product===id).focus({preventScroll:true});
    // Keep the selected mobile tab in the strip without moving the page vertically.
    const current = tabs.find(t=>t.dataset.product===id),strip=current.parentElement;
    if(strip.scrollWidth>strip.clientWidth)strip.scrollTo({left:current.offsetLeft-(strip.clientWidth-current.offsetWidth)/2,behavior:reduced.matches?'instant':'smooth'});
  }
  tabs.forEach(t=>t.addEventListener('click',()=>selectProduct(t.dataset.product)));
  function keyboardTabs(event, list, onSelect, vertical=false) {
    const keys=vertical?['ArrowDown','ArrowUp','ArrowRight','ArrowLeft']:['ArrowRight','ArrowLeft'];
    if(![...keys,'Home','End'].includes(event.key))return;
    event.preventDefault();let i=list.indexOf(event.target);
    if(event.key==='Home')i=0;else if(event.key==='End')i=list.length-1;else i=(i+(['ArrowDown','ArrowRight'].includes(event.key)?1:-1)+list.length)%list.length;
    onSelect(list[i]);list[i].focus({preventScroll:true});
  }
  document.querySelector('.solution-tabs').addEventListener('keydown',e=>keyboardTabs(e,tabs,t=>selectProduct(t.dataset.product)));
  panels.forEach(panel=> {
    const featureTabs=[...panel.querySelectorAll('[data-feature]')];
    function chooseFeature(tab) {
      featureTabs.forEach(t=>{const s=t===tab;t.setAttribute('aria-selected',String(s));t.tabIndex=s?0:-1;panel.querySelector('#'+t.getAttribute('aria-controls')).hidden=!s;});
      if(hasGsap)ScrollTrigger.refresh();
    }
    featureTabs.forEach(t=>t.addEventListener('click',()=>chooseFeature(t)));
    panel.querySelector('.feature-tabs').addEventListener('keydown',e=>keyboardTabs(e,featureTabs,chooseFeature,true));
    panel.querySelector('[data-next]').addEventListener('click',e=>selectProduct(e.currentTarget.dataset.next,{focus:true}));
    panel.querySelectorAll('[data-jump-features]').forEach(button=>button.addEventListener('click',e=>{e.preventDefault();jumpTo(panel.querySelector('.features-section'));}));
  });
  const dialog=document.querySelector('#screen-dialog');
  const viewer=document.querySelector('.dialog-image');
  const viewerImage=document.querySelector('#screen-dialog-image');
  const scaleOutput=document.querySelector('#viewer-scale');
  let viewerScale=1, viewerMode='fit', viewRequest=0;
  function fitScale(){
    const style=getComputedStyle(viewer);
    const w=viewer.clientWidth-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight);
    const h=viewer.clientHeight-parseFloat(style.paddingTop)-parseFloat(style.paddingBottom);
    return Math.min(1,w/viewerImage.naturalWidth,h/viewerImage.naturalHeight);
  }
  function setScale(value,mode='custom'){
    if(!viewerImage.naturalWidth)return;
    const oldWidth=viewerImage.getBoundingClientRect().width;
    const oldHeight=viewerImage.getBoundingClientRect().height;
    const cx=oldWidth>viewer.clientWidth?(viewer.scrollLeft+viewer.clientWidth/2)/oldWidth:.5;
    const cy=oldHeight>viewer.clientHeight?(viewer.scrollTop+viewer.clientHeight/2)/oldHeight:.5;
    viewerScale=Math.min(1,Math.max(fitScale(),value));viewerMode=mode;
    viewerImage.style.width=`${viewerImage.naturalWidth*viewerScale}px`;
    viewerImage.style.height=`${viewerImage.naturalHeight*viewerScale}px`;
    scaleOutput.textContent=`${Math.round(viewerScale*100)}%`;
    dialog.querySelector('[data-viewer=fit]').setAttribute('aria-pressed',String(mode==='fit'));
    dialog.querySelector('[data-viewer=native]').setAttribute('aria-pressed',String(viewerScale===1));
    dialog.querySelector('[data-viewer=in]').disabled=viewerScale>=1;
    dialog.querySelector('[data-viewer=out]').disabled=viewerScale<=fitScale()+.001;
    viewer.scrollTo({left:mode==='fit'?0:cx*viewerImage.width-viewer.clientWidth/2,top:mode==='fit'?0:cy*viewerImage.height-viewer.clientHeight/2,behavior:'instant'});
  }
  document.querySelectorAll('[data-zoom]').forEach(button=>button.addEventListener('click',()=>{
    opener=button;const request=++viewRequest;
    viewerImage.src=button.dataset.zoom;viewerImage.alt=button.dataset.caption;
    document.querySelector('#screen-dialog-title').textContent=button.dataset.caption;
    dialog.showModal();document.body.style.overflow='hidden';
    viewerImage.decode().then(()=>{
      if(request!==viewRequest||!dialog.open)return;
      setScale(button.classList.contains('detail-zoom')?1:fitScale(),button.classList.contains('detail-zoom')?'native':'fit');
    }).catch(()=>{});
  }));
  dialog.querySelectorAll('[data-viewer]').forEach(button=>button.addEventListener('click',()=>{
    const mode=button.dataset.viewer;
    if(mode==='fit')setScale(fitScale(),'fit');
    if(mode==='native')setScale(1,'native');
    if(mode==='in')setScale(viewerScale*1.35);
    if(mode==='out')setScale(viewerScale/1.35);
  }));
  window.addEventListener('resize',()=>{if(dialog.open){if(viewerMode==='fit')setScale(fitScale(),'fit');else setScale(viewerScale,viewerMode);}});
  document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
  dialog.addEventListener('close',()=>{viewRequest++;document.body.style.overflow='';opener?.focus({preventScroll:true});});
  const menuButton=document.querySelector('.menu-toggle'),menu=document.querySelector('#mobile-menu');
  function closeMenu(){menu.hidden=true;menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label','메뉴 열기');}
  menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')==='true';menu.hidden=open;menuButton.setAttribute('aria-expanded',String(!open));menuButton.setAttribute('aria-label',open?'메뉴 열기':'메뉴 닫기');});
  menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu();});
  reduced.addEventListener('change',()=>setupMotion(panels.find(p=>p.dataset.id===active)));
  window.addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(panels.some(p=>p.dataset.id===id)&&id!==active)selectProduct(id);});
  const initial=location.hash.slice(1),deepLink=panels.some(p=>p.dataset.id===initial);
  selectProduct(deepLink?initial:active,{navigate:deepLink});
  if(hasGsap&&!reduced.matches){gsap.from('.hero-copy > *',{y:20,opacity:0,stagger:.075,duration:.65,ease:'power2.out'});gsap.from('.hero-main-visual',{scale:.9,opacity:0,y:25,duration:1,ease:'power2.out'});}
  window.addEventListener('load',()=>{if(hasGsap)ScrollTrigger.refresh();});
  document.fonts.ready.then(()=>{if(hasGsap)ScrollTrigger.refresh();});
})();
