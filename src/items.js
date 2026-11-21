/* 하루봇 RPG 아이템 장착 — 장마다 아이템 1개, 장착하면 기능 탑재 메시지·레벨업·효과음 */
(function(){
"use strict";
var ITEMS=window.HB_ITEMS||[],KEY="hb-items-v1",SKEY="hb-sound-v1";
var have={},soundOn=true,lastFocus=null;
function load(){try{(JSON.parse(localStorage.getItem(KEY)||"[]")||[]).forEach(function(n){have[n]=1});soundOn=localStorage.getItem(SKEY)!=="off"}catch(e){}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(Object.keys(have).map(Number)))}catch(e){}}
function count(){return Object.keys(have).length}
function lvText(c){return c>=13?"Lv.MAX":"Lv."+(c+1)}
function all(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))}

/* ---------- 8비트 효과음 (Web Audio, 외부 파일 없음) ---------- */
var AC=null;
function ac(){if(!AC){var C=window.AudioContext||window.webkitAudioContext;if(!C)return null;AC=new C()}if(AC.state==="suspended")AC.resume();return AC}
var NOTE={C3:130.81,G3:196,C4:261.63,E4:329.63,G4:392,A4:440,C5:523.25,D5:587.33,E5:659.25,F5:698.46,G5:783.99,A5:880,B5:987.77,C6:1046.5,D6:1174.66,E6:1318.5,G6:1568,C7:2093};
function tone(c,f,t,d,type,vol){var o=c.createOscillator(),g=c.createGain();o.type=type||"square";o.frequency.setValueAtTime(f,t);
 g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(vol||.07,t+.008);g.gain.setValueAtTime(vol||.07,t+d*.7);g.gain.linearRampToValueAtTime(0,t+d);
 o.connect(g);g.connect(c.destination);o.start(t);o.stop(t+d+.02)}
function seq(notes,step,type,vol,t0){var c=ac();if(!c)return 0;var t=(t0||c.currentTime)+.03;
 notes.forEach(function(n){var name=n[0],len=n[1]||1;if(name)tone(c,NOTE[name],t,step*len*.95,type,vol);t+=step*len});return t}
function sfxItem(){ /* 아이템 획득 징글 */
 if(!soundOn||!ac())return;var t=seq([["G5"],["C6"],["E6"],["G6"],["C7",3]],.075,"square",.06);
 seq([["C4",2],["G4",2],["C5",3]],.075,"triangle",.12);
 return t}
function sfxLevel(t0,done){ /* 레벨업 팡파르 */
 if(!soundOn||!ac())return;
 var mel=done?[["C5"],["E5"],["G5"],["C6",2],["G5"],["C6"],["E6",2],["D6"],["E6"],["G6",4]]:[["C5"],["E5"],["G5"],["C6"],["E5"],["G5"],["C6"],["E6",4]];
 var bass=done?[["C3",4],["G3",4],["C4",4],["C4",2]]:[["C3",4],["G3",4],["C4",4]];
 seq(mel,.085,"square",.055,t0);seq(bass,.085,"triangle",.13,t0);
 seq(mel.map(function(n){return [n[0]==="G6"?"E6":n[0],n[1]]}),.085,"square",.018,(t0||ac().currentTime)+.02)}

/* ---------- 그림·글 갱신 ---------- */
function paint(){
 var c=count();
 all("svg.harubot").forEach(function(svg){var m=svg.getAttribute("data-mode");
  all(".slot",svg).forEach(function(g){var i=+g.getAttribute("data-i");
   if(m==="live")g.classList.toggle("done",!!have[i]);
   else if(m!=="full"&&+m===i){g.classList.toggle("done",!!have[i]);g.classList.toggle("now",!have[i])}})});
 all("svg.harubot[data-mode=live] .hb-face, .hbhud .hb-face").forEach(function(u){
  if(!u.closest(".hbpop"))u.setAttribute("href","#face-"+(c>=13?"proud":"smile"))});
 all(".hb-lv").forEach(function(e){e.textContent=lvText(c)});
 all(".hb-cnt").forEach(function(e){e.textContent=c});
 all(".itemcard").forEach(function(card){var n=+card.getAttribute("data-item"),b=card.querySelector(".equip");
  card.classList.toggle("on",!!have[n]);if(b){b.disabled=!!have[n];b.textContent=have[n]?"장착 완료 ✓":"장착하기 ▶"}});
}

/* ---------- 장착 팝업 ---------- */
var pop,timer;
function show(n){
 var it=ITEMS[n-1],c=count();if(!it)return;pop=pop||document.querySelector(".hbpop");if(!pop)return;
 pop.querySelector(".hbp-spr").innerHTML=it.svg;
 pop.querySelector(".hbp-n").innerHTML="【"+it.name+"】 장착!";
 pop.querySelector(".hbp-m").innerHTML="<b>"+it.func+"이 탑재됐습니다!</b><br>이제 "+it.can+" 가능합니다.";
 pop.querySelector(".hbp-lv").innerHTML=c>=13?"<span>★ LEVEL UP! "+lvText(c-1)+" → Lv.MAX ★</span><br>하루봇 완성! 13가지 기능이 모두 탑재됐습니다."
  :"<span>LEVEL UP! "+lvText(c-1)+" → "+lvText(c)+"</span>";
 var svg=pop.querySelector("svg.harubot");
 all(".slot",svg).forEach(function(g){var i=+g.getAttribute("data-i");g.classList.toggle("done",!!have[i]);g.classList.toggle("new",i===n)});
 svg.querySelector(".hb-face").setAttribute("href","#face-"+(c>=13?"proud":"spark"));
 pop.classList.remove("go");void pop.offsetWidth;pop.classList.add("go");
 lastFocus=document.activeElement;pop.hidden=false;pop.querySelector(".hbp-ok").focus();
 var t=sfxItem();clearTimeout(timer);timer=setTimeout(function(){sfxLevel(null,c>=13)},soundOn&&t?Math.max(0,(t-ac().currentTime)*1000)-120:0);
}
function hide(){if(!pop||pop.hidden)return;pop.hidden=true;if(lastFocus&&lastFocus.focus)lastFocus.focus()}
function equip(n){if(have[n])return;have[n]=1;save();paint();show(n)}

/* ---------- 연결 ---------- */
function soundBtn(){all(".sndbtn").forEach(function(b){b.setAttribute("aria-pressed",soundOn?"true":"false");b.textContent=soundOn?"♪ 효과음 켬":"♪ 효과음 끔"})}
document.addEventListener("DOMContentLoaded",function(){
 load();paint();soundBtn();
 document.addEventListener("click",function(e){
  var t=e.target;
  var eq=t.closest&&t.closest(".equip");if(eq){equip(+eq.getAttribute("data-item"));return}
  var op=t.closest&&t.closest(".quiz .opt");if(op){var q=op.closest(".quiz"),i=all("button.opt",q).indexOf(op);
   if(i===+q.getAttribute("data-ans")){var n=+q.getAttribute("data-ch");if(n&&!have[n])setTimeout(function(){equip(n)},650)}return}
  if(t.closest&&t.closest(".hbp-ok")){hide();return}
  if(t.classList&&t.classList.contains("hbpop")){hide();return}
  if(t.closest&&t.closest(".sndbtn")){soundOn=!soundOn;try{localStorage.setItem(SKEY,soundOn?"on":"off")}catch(x){}soundBtn();if(soundOn){ac();seq([["C6"],["G6",2]],.06,"square",.05)}return}
  if(t.closest&&t.closest(".hb-reset")){have={};save();paint();return}
 });
 document.addEventListener("keydown",function(e){if(e.key==="Escape")hide()});
});
})();
