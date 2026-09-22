'use strict';
const $ = id => document.getElementById(id);
let session;
const names = {explain:'Explain', defend:'Defend', learn:'Learn', transfer:'Transfer', complete:'Complete'};
const node = (tag, text, cls) => {const n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;return n;};
async function api(path, data) {
  const res = await fetch(path, data ? {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)} : {});
  const body = await res.json(); if(!res.ok) throw new Error(body.error || 'Request failed'); return body;
}
function show(id){for(const section of ['catalog','workspace','research-panel']) $(section).hidden=section!==id;$('error').textContent='';}
function render(s){
  session=s;sessionStorage.setItem('edi-session',s.id);show('workspace');$('concept-title').textContent=s.title;
  $('export').href=`/api/learning/${s.id}/export`;$('steps').replaceChildren();
  for(const [key,label] of Object.entries(names)) $('steps').append(node('li',label,key===s.stage?'current':''));
  $('stage-label').textContent=names[s.stage];$('question').textContent=s.stage==='learn'?'Review the idea, then explain what changed.':s.question || 'You completed this concept.';
  $('lesson').replaceChildren();$('lesson').hidden=!s.lesson;
  if(s.lesson){$('lesson').append(node('p',s.lesson),node('p','Activity: '+s.activity));for(const url of s.sources){const a=node('a','Reference material ↗');a.href=url;a.target='_blank';a.rel='noopener noreferrer';$('lesson').append(a,document.createElement('br'));}}
  $('answer-form').hidden=s.stage==='complete';$('complete-note').hidden=s.stage!=='complete';$('answer').value='';
  $('answer-label').textContent=s.stage==='learn'?'Your reflection and activity response':'Your explanation';
  $('submit').textContent=s.stage==='transfer'?'Complete loop':'Continue';
  $('history').replaceChildren();
  for(const item of s.history){
    const card=node('article','','trail');card.append(node('h4',names[item.stage]),node('blockquote',item.answer));
    const e=item.evaluation;
    // Defer evaluation feedback until after the defense, so it cannot supply that answer.
    if(e && s.stage!=='defend'){
      card.append(node('p',`${e.engine==='live_llm'?'AI feedback score':'Keyword coverage demo'}: ${e.overall_score}/10`,'score'));
      if(e.flag_reason)card.append(node('p',e.flag_reason));
      for(const tip of e.suggestions)card.append(node('p',tip));
      for(const quote of e.evidence_quotes)card.append(node('blockquote',quote));
    }
    $('history').append(card);
  }
}
$('answer-form').addEventListener('submit',async event=>{event.preventDefault();$('submit').disabled=true;$('error').textContent='';try{render(await api(`/api/learning/${session.id}/advance`,{stage:session.stage,answer:$('answer').value}));}catch(e){$('error').textContent=e.message;}finally{$('submit').disabled=false;}});
$('home').onclick=()=>show('catalog');
$('research').onclick=async()=>{show('research-panel');try{$('research-status').textContent=(await api('/api/research/benchmark')).summary_conclusion;}catch(e){$('error').textContent=e.message;}};
$('theme').onclick=()=>{document.body.classList.toggle('light');localStorage.setItem('edi-light',document.body.classList.contains('light'));};
if(localStorage.getItem('edi-light')==='true')document.body.classList.add('light');
(async()=>{try{const concepts=await api('/api/concepts');for(const [index,c] of concepts.entries()){const b=node('button','','concept');b.append(node('small',String(index+1).padStart(2,'0')+' / FOUNDATION'),node('strong',c.title),node('small','Explain → apply · Start practice ↗'));b.onclick=async()=>{b.disabled=true;try{render(await api('/api/learning/start',{concept_id:c.id}));}catch(e){$('error').textContent=e.message;}finally{b.disabled=false;}};$('concepts').append(b);}const saved=sessionStorage.getItem('edi-session');if(saved){try{render(await api('/api/learning/'+saved));}catch{sessionStorage.removeItem('edi-session');}}}catch(e){$('error').textContent=e.message;}})();
