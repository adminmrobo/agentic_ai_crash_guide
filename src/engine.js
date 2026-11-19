/* AI 에이전트 공식 속성 가이드 — 실험 엔진 (외부 라이브러리 없음, 브라우저 저장소 없음) */
(function(){
"use strict";
var $=function(s,r){return (r||document).querySelector(s)};
function h(tag,attrs,kids){var e=document.createElement(tag);if(attrs)for(var k in attrs){if(k==="html")e.innerHTML=attrs[k];else if(k==="text")e.textContent=attrs[k];else if(k.slice(0,2)==="on")e.addEventListener(k.slice(2),attrs[k]);else e.setAttribute(k,attrs[k]);}
 (kids||[]).forEach(function(c){if(c!=null)e.appendChild(typeof c==="string"?document.createTextNode(c):c)});return e}
function fmt(x,d){d=d==null?2:d;return (Math.round(x*Math.pow(10,d))/Math.pow(10,d)).toFixed(d)}
function pct(x){return Math.round(x*100)+"%"}
function slider(label,min,max,step,val,show,cb){
 var out=h("output",{}),inp=h("input",{type:"range",min:min,max:max,step:step,value:val,"aria-label":label});
 var w=h("label",{class:"ctl"},[h("span",{class:"ctl-l",text:label}),inp,out]);
 function upd(){out.textContent=show(+inp.value);cb&&cb()} inp.addEventListener("input",upd);
 return {el:w,get:function(){return +inp.value},set:function(v){inp.value=v;upd()},init:function(){out.textContent=show(+inp.value)}}}
function btn(label,cb,cls){return h("button",{type:"button",class:"btn"+(cls?" "+cls:""),onclick:cb,text:label})}
function bars(rows,max){ /* rows: [label,value,cls,txt] */
 var box=h("div",{class:"bars"});max=max||Math.max.apply(null,rows.map(function(r){return Math.abs(r[1])}))||1;
 rows.forEach(function(r){var w=Math.min(100,Math.abs(r[1])/max*100);
  box.appendChild(h("div",{class:"bar-row"},[h("span",{class:"bar-l",html:r[0]}),
   h("span",{class:"bar-t"},[h("span",{class:"bar-f "+(r[2]||"")+(r[1]<0?" neg":""),style:"width:"+w+"%"})]),
   h("span",{class:"bar-v",text:r[3]!=null?r[3]:fmt(r[1])})]))});return box}
function verdict(txt,ok){return h("p",{class:"verdict "+(ok?"ok":"warn"),html:txt})}

/* 공용 MDP (6~10장) */
var GAM=0.9;
function mdp(pc){pc=pc==null?0.3:pc;return {
 C:{ans:[["D",pc,10],["C",1-pc,-2]],ask:[["U",0.9,-1],["C",0.1,-3]]},
 U:{ans:[["D",0.9,10],["C",0.1,-2]],ask:[["U",1.0,-1]]}}}
var SN={C:"헷갈림",U:"이해함",D:"완료"},AN={ans:"답하기",ask:"되묻기"};
function qv(P,V,s,a,g){return P[s][a].reduce(function(t,x){return t+x[1]*(x[2]+g*V[x[0]])},0)}
function vstar(P,g,it){var V={C:0,U:0,D:0};for(var i=0;i<it;i++){var n={C:0,U:0,D:0};["C","U"].forEach(function(s){n[s]=Math.max(qv(P,V,s,"ans",g),qv(P,V,s,"ask",g))});V=n}return V}
function stepMDP(P,s,a,rnd){var x=rnd(),acc=0,L=P[s][a];for(var i=0;i<L.length;i++){acc+=L[i][1];if(x<acc)return L[i]}return L[L.length-1]}

/* 난수: 대결은 고정 난수(mulberry32), 나머지 실험은 Math.random */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function gauss(rnd){var u1=Math.max(rnd(),1e-12),u2=rnd();return Math.sqrt(-2*Math.log(u1))*Math.cos(2*Math.PI*u2)}
var STYLE=["하루식","존댓말","보고체"],MEAN=[9,7,6];
function softmax(th){var m=Math.max.apply(null,th),e=th.map(function(x){return Math.exp(x-m)}),s=e.reduce(function(a,b){return a+b});return e.map(function(x){return x/s})}

var X={};

/* 1 베이즈 */
X[1]=function(p){
 var r=h("div",{class:"res"});
 var a=slider("처음 짐작 P(A)",0.01,0.99,0.01,0.3,fmt,run),b=slider('회의록일 때 "회의"가 나올 확률',0.01,0.99,0.01,0.8,fmt,run),
 c=slider('아닐 때 "회의"가 나올 확률',0.01,0.99,0.01,0.1,fmt,run),t=slider("되묻기 기준",0.5,0.95,0.05,0.8,pct,run);
 p.append(h("div",{class:"ctls"},[a.el,b.el,c.el,t.el]),r);[a,b,c,t].forEach(function(s){s.init()});
 function run(){var pa=a.get(),pb=b.get()*pa+c.get()*(1-pa),post=b.get()*pa/pb;r.innerHTML="";
  r.append(bars([["고치기 전 P(A)",pa,"c1",pct(pa)],["고친 뒤 P(A | B)",post,"c2",pct(post)]],1),
   h("p",{class:"note",html:"P(B) = "+fmt(b.get())+"×"+fmt(pa)+" + "+fmt(c.get())+"×"+fmt(1-pa)+" = "+fmt(pb,3)}),
   post>=t.get()?verdict("하루봇: 짐작 "+pct(post)+" ≥ 기준 "+pct(t.get())+" → <b>바로 회의록을 정리합니다.</b>",true)
   :verdict("하루봇: 짐작 "+pct(post)+" &lt; 기준 "+pct(t.get())+" → <b>\"회의록 말씀이세요?\"라고 되묻습니다.</b>",false))}
 run()};

/* 2 기대효용 */
X[2]=function(p){
 var r=h("div",{class:"res"});
 var pp=slider("맞을 확률",0,1,0.01,0.77,fmt,run),R=slider("맞았을 때 만족",0,20,1,10,function(v){return "+"+v},run),
 L=slider("틀렸을 때 손해",-40,0,1,-20,String,run),K=slider("되묻기 만족",0,10,1,4,function(v){return "+"+v},run);
 p.append(h("div",{class:"ctls"},[pp.el,R.el,L.el,K.el]),r);[pp,R,L,K].forEach(function(s){s.init()});
 function run(){var q=pp.get(),ea=q*R.get()+(1-q)*L.get(),ek=K.get();r.innerHTML="";
  var be=(R.get()>L.get())?(ek-L.get())/(R.get()-L.get()):NaN;
  r.append(bars([["바로 답하기",ea,"c1"],["되묻기",ek,"c2"]]),
   h("p",{class:"note",text:"바로 답하기 = "+fmt(q)+"×("+R.get()+") + "+fmt(1-q)+"×("+L.get()+") = "+fmt(ea)+"점"}),
   h("p",{class:"note",text:isFinite(be)?"두 점수가 같아지는 분기점: 맞을 확률 "+fmt(Math.min(1,Math.max(0,be)))+"":""}),
   verdict(ea>ek?"argmax → <b>바로 답하기</b>":(ea<ek?"argmax → <b>되묻기</b>":"두 행동 점수가 같습니다"),ea>ek))}
 run()};

/* 3 제약 최적화 */
X[3]=function(p){
 var T=[["웹 검색",5,6],["일정 조회",2,5],["문서 요약",8,7],["이모티콘",1,2]],on=[true,true,true,true];
 var r=h("div",{class:"res"}),bud=slider("시간 제한(초)",4,16,1,10,function(v){return v+"초"},run);
 var ck=h("div",{class:"chips"});T.forEach(function(t,i){var c=h("input",{type:"checkbox",checked:"checked"});c.addEventListener("change",function(){on[i]=c.checked;run()});
  ck.appendChild(h("label",{class:"chip"},[c," "+t[0]+" ("+t[1]+"초, +"+t[2]+")"]))});
 var best=btn("선 안에서 최고 찾기",function(){var B=null;for(var m=0;m<16;m++){var tt=0,u=0;for(var i=0;i<4;i++)if(m>>i&1){tt+=T[i][1];u+=T[i][2]}
  if(tt<=bud.get()&&(!B||u>B[0]))B=[u,m]}var boxes=ck.querySelectorAll("input");for(var j=0;j<4;j++){on[j]=!!(B[1]>>j&1);boxes[j].checked=on[j]}run()});
 p.append(h("div",{class:"ctls"},[ck,bud.el,best]),r);bud.init();
 function run(){var tt=0,u=0;T.forEach(function(t,i){if(on[i]){tt+=t[1];u+=t[2]}});r.innerHTML="";
  r.append(bars([["걸린 시간",tt,tt<=bud.get()?"c2":"c3",tt+"초"],["시간 제한",bud.get(),"c4",bud.get()+"초"]],16),
   h("p",{class:"note",text:"g(a) = "+tt+" − "+bud.get()+" = "+(tt-bud.get())}),
   tt<=bud.get()?verdict("선 안입니다. 만족도 <b>"+u+"점</b>",true):verdict("선을 넘었습니다(g(a) &gt; 0). 이 조합은 고를 수 없습니다.",false))}
 run()};

/* 4 A* */
X[4]=function(p){
 var N={S:["요청 받음",40,120],M:["메일 읽기",150,40],W:["자료 검색",150,200],K:["일정 확인",280,40],D:["초안 작성",300,130],T:["표 만들기",300,220],R:["검토",430,175],G:["전달",540,120]};
 var E={S:{M:2,W:4},M:{K:3,D:6},W:{D:3,T:5},K:{D:4},D:{R:4,G:7},T:{R:3},R:{G:2},G:{}};
 var H={S:10,M:9,K:8,W:7,D:5,T:4,R:2,G:0};
 var r=h("div",{class:"res"}),w=slider("어림 부풀리기 배수",0,3,0.5,1,function(v){return v+"배"},reset);
 var svgbox=h("div",{class:"svgbox wide"}),st;
 p.append(h("div",{class:"ctls"},[w.el,h("div",{class:"btns"},[btn("한 걸음",step),btn("끝까지",function(){while(!st.done)step()}),btn("처음부터",reset)])]),svgbox,r);w.init();
 function cmp(a,b){return a.f-b.f||a.g-b.g||(a.n<b.n?-1:a.n>b.n?1:0)||(a.path.join()<b.path.join()?-1:1)}
 function reset(){st={open:[{f:w.get()*H.S,g:0,n:"S",path:["S"]}],closed:[],done:false,found:null};draw()}
 function step(){if(st.done)return;st.open.sort(cmp);var c;do{c=st.open.shift()}while(c&&st.closed.indexOf(c.n)>=0);
  if(!c){st.done=true;draw();return}st.closed.push(c.n);st.cur=c;
  if(c.n==="G"){st.done=true;st.found=c}else for(var v in E[c.n])if(st.closed.indexOf(v)<0)st.open.push({f:c.g+E[c.n][v]+w.get()*H[v],g:c.g+E[c.n][v],n:v,path:c.path.concat(v)});draw()}
 function draw(){var ns="http://www.w3.org/2000/svg",s=document.createElementNS(ns,"svg");s.setAttribute("viewBox","0 0 600 260");s.setAttribute("role","img");s.setAttribute("aria-label","할 일 단계 지도");
  var onp=st.found?st.found.path:(st.cur?st.cur.path:[]);
  function mk(t,a){var e=document.createElementNS(ns,t);for(var k in a)e.setAttribute(k,a[k]);s.appendChild(e);return e}
  for(var u in E)for(var v in E[u]){var A=N[u],B=N[v],hot=onp.indexOf(u)>=0&&onp.indexOf(v)===onp.indexOf(u)+1;
   mk("line",{x1:A[1],y1:A[2],x2:B[1],y2:B[2],class:"edge"+(hot?" hot":"")});var t=mk("text",{x:(A[1]+B[1])/2,y:(A[2]+B[2])/2-6,class:"elab"});t.textContent=E[u][v]+"분"}
  for(var n in N){var c=N[n],cls="node"+(st.closed.indexOf(n)>=0?" seen":"")+(onp.indexOf(n)>=0?" path":"");
   mk("circle",{cx:c[1],cy:c[2],r:24,class:cls});var t1=mk("text",{x:c[1],y:c[2]+4,class:"nlab"});t1.textContent=c[0].length>3?c[0].slice(0,2):c[0];
   var t2=mk("text",{x:c[1],y:c[2]+40,class:"nsub"});t2.textContent=c[0]+" · h "+(w.get()*H[n])}
  svgbox.innerHTML="";svgbox.appendChild(s);r.innerHTML="";
  var o=st.open.slice().sort(cmp).filter(function(x){return st.closed.indexOf(x.n)<0});
  var tb=h("table",{class:"tbl"},[h("tr",{},[h("th",{text:"후보 단계"}),h("th",{text:"g 쓴 시간"}),h("th",{text:"h 어림"}),h("th",{text:"f 합"})])]);
  o.slice(0,5).forEach(function(x){tb.appendChild(h("tr",{},[h("td",{text:N[x.n][0]}),h("td",{text:x.g+"분"}),h("td",{text:fmt(x.f-x.g,1)}),h("td",{text:fmt(x.f,1)})]))});
  r.append(h("p",{class:"note",text:"둘러본 단계: "+st.closed.length+"개"}),tb);
  if(st.found){var opt=st.found.g===13;r.append(verdict("찾은 길: "+st.found.path.map(function(x){return N[x][0]}).join(" → ")+" = <b>"+st.found.g+"분</b>"+(opt?" (가장 빠른 길)":" (가장 빠른 13분 길을 놓침)"),opt))}}
 reset()};

/* 5 내시 균형 */
X[5]=function(p){
 var G={"협력 상황":{WW:[2,0],WC:[5,5],CW:[1,1],CC:[0,3]},"숨바꼭질 상황":{WW:[1,-1],WC:[-1,1],CW:[-1,1],CC:[1,-1]}};
 var cur="협력 상황",sel=null,r=h("div",{class:"res"}),tb=h("div",{});
 p.append(h("div",{class:"btns"},Object.keys(G).map(function(k){return btn(k,function(){cur=k;sel=null;draw()})})),tb,r);
 var L={W:"글쓰기",C:"계산"};
 function br(g,a,b){var u=g[a+b];return {me:["W","C"].every(function(x){return u[0]>=g[x+b][0]}),you:["W","C"].every(function(y){return u[1]>=g[a+y][1]})}}
 function draw(){var g=G[cur];tb.innerHTML="";var t=h("table",{class:"tbl game"},[h("tr",{},[h("th",{text:"하루봇 ↓ / 주판봇 →"}),h("th",{text:"글쓰기"}),h("th",{text:"계산"})])]);
  ["W","C"].forEach(function(a){var tr=h("tr",{},[h("th",{text:L[a]})]);["W","C"].forEach(function(b){var u=g[a+b],q=br(g,a,b);
   var td=h("td",{class:"cell"+(q.me&&q.you?" ne":"")+(sel===a+b?" sel":""),tabindex:"0",onclick:function(){sel=a+b;draw()}},
    [h("span",{class:"pay",html:(q.me?"<u>":"")+u[0]+(q.me?"</u>":"")+" , "+(q.you?"<u>":"")+u[1]+(q.you?"</u>":"")})]);tr.appendChild(td)});t.appendChild(tr)});
  tb.appendChild(t);r.innerHTML="";var ne=Object.keys(g).filter(function(k){var q=br(g,k[0],k[1]);return q.me&&q.you});
  r.append(h("p",{class:"note",text:"칸의 숫자는 (하루봇 점수, 주판봇 점수). 밑줄은 '상대 선택을 볼 때 그쪽의 최선'입니다."}));
  if(sel){var a=sel[0],b=sel[1],oa=a==="W"?"C":"W",ob=b==="W"?"C":"W";
   r.append(h("p",{class:"note",text:"이 칸에서 하루봇이 혼자 "+L[oa]+"(으)로 바꾸면 "+g[a+b][0]+" → "+g[oa+b][0]+"점, 주판봇이 혼자 "+L[ob]+"(으)로 바꾸면 "+g[a+b][1]+" → "+g[a+ob][1]+"점."}))}
  r.append(ne.length?verdict("순수 전략 균형: <b>"+ne.map(function(k){return "하루봇 "+L[k[0]]+" · 주판봇 "+L[k[1]]}).join(", ")+"</b>",true)
   :verdict("순수 전략 균형이 <b>없습니다</b>. 둘 다 반반씩 섞어 고르는 것(혼합 전략)이 균형입니다.",false))}
 draw()};

/* 6 상태 전이 */
X[6]=function(p){
 var pol="ask",P=mdp(),r=h("div",{class:"res"}),runs=[];
 var pb=h("div",{class:"btns"},[btn("늘 답하기",function(){pol="ans";runs=[];info()},"tog"),btn("헷갈리면 되묻기",function(){pol="ask";runs=[];info()},"tog"),btn("대화 한 판 돌리기",one)]);
 var tbl=h("table",{class:"tbl"},[h("tr",{},[h("th",{text:"지금 상태 + 행동"}),h("th",{text:"다음 상태 (확률, 보상)"})])]);
 ["C","U"].forEach(function(s){["ans","ask"].forEach(function(a){tbl.appendChild(h("tr",{},[h("td",{text:SN[s]+" + "+AN[a]}),h("td",{text:P[s][a].map(function(x){return SN[x[0]]+" "+pct(x[1])+" ("+(x[2]>0?"+":"")+x[2]+")"}).join(" · ")})]))})});
 p.append(tbl,pb,r);
 function act(s){return pol==="ans"?"ans":(s==="C"?"ask":"ans")}
 function one(){var s="C",path=[],tot=0,n=0;while(s!=="D"&&n<60){var a=act(s),x=stepMDP(P,s,a,Math.random);path.push(SN[s]+" —"+AN[a]+"("+(x[2]>0?"+":"")+x[2]+")→ ");tot+=x[2];s=x[0];n++}
  path.push("완료");runs.push(n);info(path.join(""),tot,n)}
 function info(path,tot,n){r.innerHTML="";r.append(h("p",{class:"note",text:"지금 정책: "+(pol==="ans"?"늘 답하기":"헷갈리면 되묻기, 이해하면 답하기")}));
  pb.querySelectorAll(".tog").forEach(function(b,i){b.classList.toggle("on",(i===0)===(pol==="ans"))});
  if(path){r.append(h("p",{class:"path",text:path}),h("p",{class:"note",text:"이번 판: "+n+"번 주고받음, 보상 합 "+tot}));
   var avg=runs.reduce(function(a,b){return a+b},0)/runs.length;r.append(verdict("지금까지 "+runs.length+"판 평균 "+fmt(avg,1)+"번 만에 완료",true))}}
 info()};

/* 7 할인 누적 보상 */
X[7]=function(p){
 var PR={"되묻고 완료":[-1,10],"바로 완료":[10],"헷갈림 두 번 뒤 완료":[-2,-2,10],"끝없이 헷갈림":null},cur="되묻고 완료",r=h("div",{class:"res"});
 var g=slider("γ (할인율)",0,1,0.05,0.9,fmt,run);
 p.append(h("div",{class:"btns"},Object.keys(PR).map(function(k){return btn(k,function(){cur=k;run()})})),h("div",{class:"ctls"},[g.el]),r);g.init();
 function run(){var gm=g.get(),seq=PR[cur],rows=[],G=0;r.innerHTML="";
  if(seq){seq.forEach(function(x,k){var v=Math.pow(gm,k)*x;G+=v;rows.push(["r"+(k+1)+" = "+x+" × γ<sup>"+k+"</sup>",v,"c1",fmt(v)])});
   r.append(bars(rows,10),verdict("G = <b>"+fmt(G)+"</b>",true))}
  else{for(var k=0;k<8;k++){var v=Math.pow(gm,k)*-2;rows.push(["r"+(k+1)+" = −2 × γ<sup>"+k+"</sup>",v,"c3",fmt(v)])}
   r.append(bars(rows,2),h("p",{class:"note",text:"… 끝없이 이어집니다."}),
    gm<1?verdict("끝없이 더해도 −2 ÷ (1 − "+fmt(gm)+") = <b>"+fmt(-2/(1-gm))+"</b>에서 멈춥니다(등비급수).",true)
    :verdict("γ = 1이면 −2를 끝없이 더해 <b>끝없이 작아집니다</b>. 값이 정해지지 않습니다.",false))}}
 run()};

/* 8 상태가치 V (몬테카를로) */
X[8]=function(p){
 var P=mdp(),pol={C:"ask",U:"ans"},V=vstar(P,GAM,400),sum=0,n=0,hist=[],r=h("div",{class:"res"}),ch=h("div",{class:"svgbox"});
 function ep(){var s="C",G=0,d=1;while(s!=="D"){var x=stepMDP(P,s,pol[s],Math.random);G+=d*x[2];d*=GAM;s=x[0]}return G}
 function add(k){var last;for(var i=0;i<k;i++){last=ep();sum+=last;n++;if(n<=50||n%20===0)hist.push([n,sum/n])}draw(last)}
 p.append(h("div",{class:"btns"},[btn("1판 더",function(){add(1)}),btn("1000판 더",function(){add(1000)}),btn("처음부터",function(){sum=0;n=0;hist=[];draw()})]),ch,r);
 function draw(last){r.innerHTML="";ch.innerHTML="";
  r.append(h("p",{class:"note",text:"정책: 헷갈리면 되묻고, 이해하면 답하기 · 시작 상태: 헷갈림"}),
   h("p",{class:"note",text:n?("마지막 판 G = "+fmt(last)+" · 지금까지 "+n+"판 평균 = "+fmt(sum/n)):"아직 돌린 판이 없습니다."}),
   verdict("벨만 방정식으로 구한 정확한 값 V(헷갈림) = <b>"+fmt(V.C)+"</b>",true));
  if(hist.length>1){var ns="http://www.w3.org/2000/svg",s=document.createElementNS(ns,"svg");s.setAttribute("viewBox","0 0 600 180");
   var mx=hist[hist.length-1][0],y=function(v){return 160-(v-0)/12*150},x=function(k){return 30+Math.log(k)/Math.log(Math.max(mx,2))*560};
   var line=document.createElementNS(ns,"polyline");line.setAttribute("points",hist.map(function(q){return x(q[0])+","+y(Math.max(-1,Math.min(12,q[1])))}).join(" "));line.setAttribute("class","ln");s.appendChild(line);
   var ref=document.createElementNS(ns,"line");ref.setAttribute("x1",30);ref.setAttribute("x2",590);ref.setAttribute("y1",y(V.C));ref.setAttribute("y2",y(V.C));ref.setAttribute("class","ref");s.appendChild(ref);
   var t=document.createElementNS(ns,"text");t.setAttribute("x",34);t.setAttribute("y",y(V.C)-6);t.setAttribute("class","elab");t.textContent="정확한 값 "+fmt(V.C);s.appendChild(t);
   var t2=document.createElementNS(ns,"text");t2.setAttribute("x",590);t2.setAttribute("y",176);t2.setAttribute("text-anchor","end");t2.setAttribute("class","elab");t2.textContent="판 수 "+mx+" (가로축은 로그 눈금)";s.appendChild(t2);
   ch.appendChild(s)}}
 draw()};

/* 9 행동가치 Q */
X[9]=function(p){
 var r=h("div",{class:"res"}),pc=slider("답하기 성공 확률(헷갈릴 때)",0,1,0.05,0.3,fmt,run);p.append(h("div",{class:"ctls"},[pc.el]),r);pc.init();
 function run(){var P=mdp(pc.get()),V=vstar(P,GAM,600),qa=qv(P,V,"C","ans",GAM),qk=qv(P,V,"C","ask",GAM);r.innerHTML="";
  r.append(bars([["Q(헷갈림, 답하기)",qa,"c1"],["Q(헷갈림, 되묻기)",qk,"c2"]],10),
   h("p",{class:"note",text:"Q(헷갈림, 답하기) = "+fmt(pc.get())+"×10 + "+fmt(1-pc.get())+"×(−2 + 0.9×"+fmt(V.C)+") = "+fmt(qa)}),
   verdict("argmax Q → <b>"+(qa>qk?"답하기":"되묻기")+"</b>",qa>qk))}
 run()};

/* 10 벨만 방정식 (가치 되풀이) */
X[10]=function(p){
 var P=mdp(),rows=[],V,r=h("div",{class:"res"}),g=slider("γ (할인율)",0.5,0.99,0.01,0.9,fmt,reset);
 p.append(h("div",{class:"ctls"},[g.el,h("div",{class:"btns"},[btn("한 번 되풀이",it),btn("처음부터",reset)])]),r);g.init();
 function reset(){V={C:0,U:0,D:0};rows=[[0,0,0]];draw()}
 function it(){var n={C:0,U:0,D:0};["C","U"].forEach(function(s){n[s]=Math.max(qv(P,V,s,"ans",g.get()),qv(P,V,s,"ask",g.get()))});V=n;rows.push([rows.length,V.C,V.U]);draw()}
 function draw(){r.innerHTML="";var t=h("table",{class:"tbl"},[h("tr",{},[h("th",{text:"되풀이"}),h("th",{text:"V(헷갈림)"}),h("th",{text:"V(이해함)"})])]);
  rows.slice(-9).forEach(function(q){t.appendChild(h("tr",{},[h("td",{text:q[0]+"번"}),h("td",{text:fmt(q[1])}),h("td",{text:fmt(q[2])})]))});
  var Vs=vstar(P,g.get(),2000);r.append(t,verdict("끝까지 되풀이한 값: V(헷갈림) = <b>"+fmt(Vs.C)+"</b>, V(이해함) = <b>"+fmt(Vs.U)+"</b>",Math.abs(V.C-Vs.C)<0.01))}
 reset()};

/* 11 소프트맥스 */
X[11]=function(p){
 var r=h("div",{class:"res"}),cnt=[0,0,0];
 var S=[slider("하루식 점수",-2,4,0.1,2.0,function(v){return fmt(v,1)},run),slider("존댓말 점수",-2,4,0.1,1.0,function(v){return fmt(v,1)},run),slider("보고체 점수",-2,4,0.1,0.1,function(v){return fmt(v,1)},run)];
 var T=slider("온도",0.2,3,0.1,1,function(v){return fmt(v,1)},run);
 p.append(h("div",{class:"ctls"},S.map(function(s){return s.el}).concat([T.el,btn("열 번 뽑기",draw10)])),r);S.concat([T]).forEach(function(s){s.init()});
 function pr(){return softmax(S.map(function(s){return s.get()/T.get()}))}
 function draw10(){var q=pr();cnt=[0,0,0];for(var i=0;i<10;i++){var u=Math.random();cnt[u<q[0]?0:(u<q[0]+q[1]?1:2)]++}run(true)}
 function run(keep){if(keep!==true)cnt=null;var q=pr();r.innerHTML="";
  r.append(bars(STYLE.map(function(n,i){return [n,q[i],"c"+(i+1),pct(q[i])]}),1),
   h("p",{class:"note",text:"온도 1이 원래 식입니다. 온도는 점수를 나누는 값으로, 챗봇 설정에서 쓰는 손잡이입니다."}));
  if(cnt)r.append(verdict("열 번 뽑은 결과: "+STYLE.map(function(n,i){return n+" "+cnt[i]+"번"}).join(" · "),true))}
 run()};

/* 12·13 학습 실험 (점수는 하루가 줌) */
function learner(p,critic){
 var alpha=critic?0.1:0.02,th=[0,0,0],V=0,log=[],r=h("div",{class:"res"});
 p.append(h("div",{class:"btns"},[btn("하루에게 보여 주기",function(){go(1)}),btn("스무 번",function(){go(20)}),btn("처음부터",function(){th=[0,0,0];V=0;log=[];draw()})]),r);
 function go(k){for(var i=0;i<k;i++){var q=softmax(th),u=Math.random(),a=u<q[0]?0:(u<q[0]+q[1]?1:2);
  var G=Math.min(10,Math.max(1,MEAN[a]+gauss(Math.random)));G=Math.round(G*10)/10;var A=critic?G-V:G,old=q[a];
  th=th.map(function(t,j){return t+alpha*A*((j===a?1:0)-q[j])});var nw=softmax(th)[a];var v0=V;if(critic)V+=0.1*(G-V);
  log.push([STYLE[a],G,critic?A:null,old,nw,v0])}draw()}
 function draw(){var q=softmax(th);r.innerHTML="";
  r.append(bars(STYLE.map(function(n,i){return [n,q[i],"c"+(i+1),pct(q[i])]}),1));
  if(critic)r.append(h("p",{class:"note",text:"평가자(박사)의 '보통 점수' 어림 V = "+fmt(V)}));
  if(log.length){var t=h("table",{class:"tbl"},[h("tr",{},[h("th",{text:"뽑힌 말투"}),h("th",{text:"하루 점수 G"})].concat(critic?[h("th",{text:"V"}),h("th",{text:"이점 A"})]:[]).concat([h("th",{text:"그 말투 확률"})]))]);
   log.slice(-8).reverse().forEach(function(l){var up=l[4]>l[3];t.appendChild(h("tr",{},[h("td",{text:l[0]}),h("td",{text:fmt(l[1],1)})].concat(critic?[h("td",{text:fmt(l[5])}),h("td",{text:(l[2]>0?"+":"")+fmt(l[2])})]:[]).concat([h("td",{class:up?"up":"down",text:pct(l[3])+" → "+pct(l[4])+(up?" ▲":" ▼")})])))});
   r.append(h("p",{class:"note",text:"최근 "+Math.min(8,log.length)+"번 (전체 "+log.length+"번)"}),t)}}
 draw()}
X[12]=function(p){learner(p,false)};X[13]=function(p){learner(p,true)};

/* 대결 */
function duelRun(seed,critic,alpha,rounds){var rnd=mulberry32(seed),th=[0,0,0],b=0,hist=[],hit=null;
 for(var t=0;t<rounds;t++){var pi=softmax(th),u=rnd(),a=u<pi[0]?0:(u<pi[0]+pi[1]?1:2);var G=Math.min(10,Math.max(1,MEAN[a]+gauss(rnd)));
  var adv=critic?G-b:G;th=th.map(function(x,i){return x+alpha*adv*((i===a?1:0)-pi[i])});if(critic)b+=0.1*(G-b);hist.push(pi[0]);if(hit===null&&pi[0]>=0.9)hit=t+1}
 return {hit:hit||rounds,hist:hist}}
window.__duelRun=duelRun;
X.duel=function(p){var seed=0,r=h("div",{class:"res"}),r2=h("div",{class:"res"}),ch=h("div",{class:"svgbox"});
 p.append(h("div",{class:"btns"},[btn("한 판 붙기",function(){seed=seed%30+1;one()}),btn("30판 모두",all)]),ch,r,r2);
 function one(){var A=duelRun(seed,false,0.02,300),B=duelRun(seed,true,0.1,300);ch.innerHTML="";
  var ns="http://www.w3.org/2000/svg",s=document.createElementNS(ns,"svg");s.setAttribute("viewBox","0 0 600 200");s.setAttribute("role","img");s.setAttribute("aria-label","하루식 확률 변화");
  var y=function(v){return 185-v*170},x=function(k){return 30+k/300*560};
  [[A,"lnA"],[B,"lnB"]].forEach(function(q){var pl=document.createElementNS(ns,"polyline");pl.setAttribute("points",q[0].hist.map(function(v,k){return x(k)+","+y(v)}).join(" "));pl.setAttribute("class",q[1]);s.appendChild(pl)});
  var rf=document.createElementNS(ns,"line");rf.setAttribute("x1",30);rf.setAttribute("x2",590);rf.setAttribute("y1",y(0.9));rf.setAttribute("y2",y(0.9));rf.setAttribute("class","ref");s.appendChild(rf);
  ch.appendChild(s);r.innerHTML="";r.append(h("p",{class:"legend",html:'<span class="kA"></span>하루봇 A(평가자 없음) <span class="kB"></span>하루봇 B(박사 평가자) · 점선: 90%'}),
   h("p",{class:"note",text:seed+"번째 난수 판: A "+(A.hit>=300?"300번 안에 못 닿음":A.hit+"번")+" · B "+(B.hit>=300?"300번 안에 못 닿음":B.hit+"번")}),
   verdict(B.hit<A.hit?"이번 판 승자: <b>하루봇 B</b>":(A.hit<B.hit?"이번 판 승자: <b>하루봇 A</b>":"무승부"),B.hit<=A.hit))}
 function all(){var wa=0,wb=0,sa=0,sb=0,miss=0;for(var k=1;k<=30;k++){var a=duelRun(k,false,0.02,300).hit,b=duelRun(k,true,0.1,300).hit;sa+=a;sb+=b;if(a>=300)miss++;if(b<a)wb++;else if(a<b)wa++}
  r2.innerHTML="";r2.append(verdict("30판 결과: 하루봇 B <b>"+wb+"승</b>, 하루봇 A <b>"+wa+"승</b>. 평균 B "+fmt(sb/30,1)+"번, A "+fmt(sa/30,1)+"번 (A는 "+miss+"판이 300번 안에 못 닿음)",wb>wa))}
 seed=1;one()};

/* 퀴즈 */
function quiz(q){var ans=+q.dataset.ans,fb=$(".qfb",q);q.querySelectorAll("button.opt").forEach(function(b,i){b.addEventListener("click",function(){
 q.querySelectorAll("button.opt").forEach(function(x){x.classList.remove("right","wrong")});b.classList.add(i===ans?"right":"wrong");
 fb.innerHTML=(i===ans?"<b>맞았어요.</b> ":"<b>다시 볼까요?</b> ")+fb.dataset.exp;fb.hidden=false})})}

document.addEventListener("DOMContentLoaded",function(){
 document.querySelectorAll("[data-exp]").forEach(function(p){var k=p.dataset.exp;if(X[k])X[k](p)});
 document.querySelectorAll(".quiz").forEach(quiz)});
})();
