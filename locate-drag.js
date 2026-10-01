/* Pointer and keyboard placement for the "current sentence" shortcut. */
(() => {
  'use strict';
  const button = document.querySelector('#locatePlayingBtn');
  if (!button) return;
  const key = 'fr4000-locate-position';
  const margin = 8;
  let start = null;
  let suppressClick = false;
  const clamp = (value,min,max) => Math.max(min,Math.min(max,value));
  function bounds() {
    const dock = window.innerWidth <= 800 ? document.querySelector('.mobileNav')?.getBoundingClientRect().height || 0 : 0;
    return {maxX:Math.max(margin,window.innerWidth-button.offsetWidth-margin),maxY:Math.max(margin,window.innerHeight-button.offsetHeight-dock-margin)};
  }
  function place(x,y,save=false) {
    const {maxX,maxY} = bounds();
    const left = clamp(x,margin,maxX),top = clamp(y,margin,maxY);
    button.classList.add('custom-position');
    button.style.left = `${left}px`;
    button.style.top = `${top}px`;
    if (save) {
      try {localStorage.setItem(key,JSON.stringify({x:(left-margin)/Math.max(1,maxX-margin),y:(top-margin)/Math.max(1,maxY-margin)}));} catch {}
    }
  }
  function restore() {
    try {
      const saved = JSON.parse(localStorage.getItem(key) || 'null');
      if (!saved || !Number.isFinite(saved.x) || !Number.isFinite(saved.y)) return;
      const {maxX,maxY} = bounds();
      place(margin+clamp(saved.x,0,1)*(maxX-margin),margin+clamp(saved.y,0,1)*(maxY-margin));
    } catch {}
  }
  button.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    const rect = button.getBoundingClientRect();
    start = {id:event.pointerId,x:event.clientX,y:event.clientY,left:rect.left,top:rect.top,moved:false};
    button.setPointerCapture(event.pointerId);
  });
  button.addEventListener('pointermove', event => {
    if (!start || start.id !== event.pointerId) return;
    const dx=event.clientX-start.x,dy=event.clientY-start.y;
    if (!start.moved && Math.hypot(dx,dy)<5) return;
    start.moved=true;
    button.classList.add('dragging');
    place(start.left+dx,start.top+dy);
  });
  function end(event) {
    if (!start || start.id !== event.pointerId) return;
    if (start.moved) {
      suppressClick=true;
      setTimeout(() => {suppressClick=false;},500);
      const rect=button.getBoundingClientRect();
      place(rect.left,rect.top,true);
    }
    button.classList.remove('dragging');
    start=null;
  }
  button.addEventListener('pointerup',end);
  button.addEventListener('pointercancel',end);
  button.addEventListener('click',event => {
    if (!suppressClick) return;
    suppressClick=false;
    event.preventDefault();
    event.stopImmediatePropagation();
  },true);
  button.addEventListener('keydown',event => {
    if (!event.altKey || !['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    const rect=button.getBoundingClientRect();
    const dx=event.key==='ArrowLeft'?-24:event.key==='ArrowRight'?24:0;
    const dy=event.key==='ArrowUp'?-24:event.key==='ArrowDown'?24:0;
    place(rect.left+dx,rect.top+dy,true);
  });
  window.addEventListener('resize',() => {
    if (button.classList.contains('custom-position')) restore();
  });
  restore();
})();
