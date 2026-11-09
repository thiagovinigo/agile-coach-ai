import * as THREE from './vendor/three.module.js';
import { GLTFLoader } from './vendor/GLTFLoader.js';
import { createFlight, battlePose, viewQuaternion } from './flight-motion.js';
import { playHyperspaceIntro } from './hyperspace-intro.js';
const previewParams=new URLSearchParams(location.search),previewTime=previewParams.has('t')?Math.max(0,Number(previewParams.get('t'))||0):null;
const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
let opening=null,openingPending=!reducedMotion.matches&&(previewTime===null||previewParams.get('shot')==='intro');
if(openingPending)document.body.classList.add('opening-active');

const canvas=document.getElementById('universe');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance',preserveDrawingBuffer:previewTime!==null});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.7)); renderer.setSize(innerWidth,innerHeight);
renderer.outputColorSpace=THREE.SRGBColorSpace; renderer.toneMapping=THREE.ACESFilmicToneMapping; renderer.toneMappingExposure=1.32;
const scene=new THREE.Scene(); scene.background=new THREE.Color(0x02050c); scene.fog=new THREE.FogExp2(0x02050c,.0015);
const camera=new THREE.PerspectiveCamera(49,innerWidth/innerHeight,.1,300);
const ambient=new THREE.AmbientLight(0x7a91bc,1.12);scene.add(ambient);
const sun=new THREE.DirectionalLight(0xffe0b1,3.35);sun.position.set(-30,24,38);scene.add(sun);
const cold=new THREE.DirectionalLight(0x547dc2,1.45);cold.position.set(60,-10,-30);scene.add(cold);
const worlds=[
 {name:'Tatooine',type:'desert',color:'#d9a05c',atmo:'#eab267',x:0,y:0,z:0,r:2.7,tag:'O MUNDO DOS DOIS SÓIS',region:'Borda Exterior',climate:'Deserto árido · dois sóis',life:'Jawas, Tusken e colonos',event:'Lar de Anakin e Luke Skywalker',coords:'AR-720 / SISTEMA TATOO'},
 {name:'Hoth',type:'ice',color:'#bbd9e8',atmo:'#b5e9ff',x:18,y:4,z:-5,r:2.7,tag:'O SILÊNCIO DO GELO',region:'Borda Exterior',climate:'Glacial · tempestades de neve',life:'Tauntauns e wampas',event:'Batalha da Base Echo',coords:'AR-739 / SISTEMA HOTH'},
 {name:'Naboo',type:'lush',color:'#4c9b88',atmo:'#66e3d6',x:36,y:-3,z:-1,r:2.7,tag:'ONDE ÁGUA E TERRA SE ENCONTRAM',region:'Borda Intermediária',climate:'Temperado · lagos e florestas',life:'Humanos e gungans',event:'Terra natal de Padmé Amidala',coords:'MI-023 / SISTEMA NABOO'},
 {name:'Mustafar',type:'lava',color:'#e24b27',atmo:'#ff672e',x:54,y:3,z:-5,r:2.7,tag:'O CORAÇÃO EM CHAMAS',region:'Borda Exterior',climate:'Vulcânico · rios de lava',life:'Mustafarianos',event:'Duelo de Obi-Wan e Anakin',coords:'AR-442 / SISTEMA MUSTAFAR'},
 {name:'Coruscant',type:'city',color:'#a2a9c1',atmo:'#9bc5f5',x:72,y:-1,z:1,r:2.7,tag:'O CENTRO DA GALÁXIA',region:'Mundos do Núcleo',climate:'Urbano · planeta-cidade',life:'Bilhões de espécies',event:'Sede da República e do Senado',coords:'NU-001 / SISTEMA CORUSCANT'}
];
const mobile=innerWidth<900;
function hash(x,y,s){let n=Math.sin(x*127.1+y*311.7+s*74.7)*43758.5453;return n-Math.floor(n)}
function noise(x,y,s){let a=Math.floor(x),b=Math.floor(y),fx=x-a,fy=y-b;fx=fx*fx*(3-2*fx);fy=fy*fy*(3-2*fy);let p=hash(a,b,s),q=hash(a+1,b,s),r=hash(a,b+1,s),t=hash(a+1,b+1,s);return (p+(q-p)*fx)*(1-fy)+(r+(t-r)*fx)*fy}
function fbm(x,y,s){let n=0,a=.54,f=1;for(let i=0;i<5;i++){n+=noise(x*f,y*f,s+i*17)*a;f*=2.05;a*=.49}return n}
const sphereGeo=new THREE.SphereGeometry(1,96,64);
const worldGroups=[];
const coverGroup=new THREE.Group(),coverPlanets=[];scene.add(coverGroup);coverGroup.visible=false;
for(const w of worlds){let group=new THREE.Group();group.position.set(w.x,w.y,w.z);scene.add(group);worldGroups.push(group);w.group=group;
 let halo=new THREE.Mesh(sphereGeo,new THREE.ShaderMaterial({transparent:true,depthWrite:false,side:THREE.BackSide,blending:THREE.AdditiveBlending,uniforms:{glow:{value:new THREE.Color(w.atmo)}},vertexShader:`varying vec3 n;varying vec3 v;void main(){vec4 p=modelViewMatrix*vec4(position,1.);n=normalize(normalMatrix*normal);v=normalize(-p.xyz);gl_Position=projectionMatrix*p;}`,fragmentShader:`uniform vec3 glow;varying vec3 n;varying vec3 v;void main(){float f=pow(1.-abs(dot(n,v)),2.2);gl_FragColor=vec4(glow,f*.4);}`}));halo.scale.setScalar(w.r*1.08);group.add(halo);
 if(w.type==='desert'){for(let k of [-1,1]){let star=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTexture(),color:k<0?0xffd9a1:0xffe6b4,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}));star.position.set(k*7,4+k*1.2,-10);star.scale.set(3,3,1);group.add(star)}}
}
// As cinco variantes usam apenas as geometrias e os mapas de relevo dos dois GLBs enviados.
const modelLoader=new GLTFLoader();
const deathStar=new THREE.Group();scene.add(deathStar);deathStar.visible=false;
let deathStarBody=null;
function syncDeathStar(){
 if(!deathStarBody)return;
 camera.updateMatrixWorld();
 const ray=new THREE.Raycaster();ray.setFromCamera(new THREE.Vector2(innerWidth<900?.55:.53,.25),camera);
 const distance=(5-ray.ray.origin.z)/ray.ray.direction.z;
 deathStar.position.copy(ray.ray.origin).addScaledVector(ray.ray.direction,distance);
 const radiusPx=Math.max(42,Math.min(92,innerWidth*.072));
 const radius=radiusPx*(2*Math.abs(distance)*Math.tan(THREE.MathUtils.degToRad(camera.fov/2))/innerHeight);
 deathStarBody.scale.setScalar(radius*2/deathStarBody.userData.size);
}
modelLoader.loadAsync('./assets/death-star.glb').then(gltf=>{
 const model=gltf.scene;
 const bounds=new THREE.Box3().setFromObject(model),size=bounds.getSize(new THREE.Vector3()),center=bounds.getCenter(new THREE.Vector3());
 model.position.sub(center);deathStarBody=new THREE.Group();deathStarBody.userData.size=Math.max(size.x,size.y,size.z);deathStarBody.add(model);deathStarBody.rotation.set(.1,-.48,.03);deathStar.add(deathStarBody);
 syncDeathStar();deathStar.visible=stages[index].kind==='cover';
}).catch(error=>console.error('Não foi possível carregar a Estrela da Morte:',error));

// A nave permanece no espaço e conserva sua trajetória após a chegada.
const falconRig=new THREE.Group();scene.add(falconRig);falconRig.visible=false;
let falconModel=null,falconDeparture=null;
modelLoader.loadAsync('./assets/millennium-falcon.glb').then(gltf=>{
 const model=gltf.scene,box=new THREE.Box3().setFromObject(model),size=box.getSize(new THREE.Vector3()),center=box.getCenter(new THREE.Vector3());
 model.position.sub(center);const alignment=new THREE.Group();alignment.add(model);
 alignment.quaternion.setFromUnitVectors(new THREE.Vector3(.3221573,.9394947,.1164666).normalize(),new THREE.Vector3(0,1,0));
 alignment.scale.setScalar(2.43/Math.max(size.x,size.y,size.z));falconRig.add(alignment);falconModel=model;
 animateFalconIdle(0);
}).catch(error=>console.error('Não foi possível carregar a Millennium Falcon:',error));
function animateFalconIdle(now){
 if(!falconModel)return;
 falconRig.visible=true;const t=now*.001;
 if(falconDeparture){const elapsed=Math.max(0,(now-falconDeparture.start)*.001),distance=13.5*(1-Math.exp(-elapsed*elapsed/30));falconRig.position.copy(falconDeparture.position).addScaledVector(falconDeparture.direction,distance);falconRig.quaternion.copy(falconDeparture.quaternion)}
 else{falconRig.position.set(35+Math.sin(t*.13)*7.65,1+Math.sin(t*.17)*1.125,18+Math.cos(t*.13)*1.8);falconRig.rotation.set(.23,.6+Math.sin(t*.13)*.5,-.1+Math.sin(t*.16)*.08)}
}
// Seis caças e 24 rajadas, com as órbitas e a orientação da referência.
const battle=new THREE.Group();scene.add(battle);
const battleShips=[],battleBolts=[];
Promise.all([modelLoader.loadAsync('./assets/jedi-starfighter.glb'),modelLoader.loadAsync('./assets/tie-fighter.glb')]).then(([jedi,tie])=>{
 for(let i=0;i<6;i++){
  const model=(i%2?tie.scene:jedi.scene).clone(true),bounds=new THREE.Box3().setFromObject(model),size=bounds.getSize(new THREE.Vector3());
  model.position.sub(bounds.getCenter(new THREE.Vector3()));
  const pivot=new THREE.Group();pivot.add(model);pivot.scale.setScalar((i%2?1.05:1.23)/Math.max(size.x,size.y,size.z));battle.add(pivot);battleShips.push(pivot);
 }
 const geometry=new THREE.CylinderGeometry(.018,.018,.9,5);geometry.rotateX(Math.PI/2);
 for(let i=0;i<24;i++){
  const bolt=new THREE.Mesh(geometry,new THREE.MeshBasicMaterial({color:new THREE.Color(i%2?'#67ff74':'#ff5249').multiplyScalar(3),transparent:true,opacity:.9,depthWrite:false}));
  battle.add(bolt);battleBolts.push(bolt);
 }
}).catch(error=>console.error('Não foi possível carregar os caças:',error));
const boltForward=new THREE.Vector3();
function animateBattle(now){
 const time=now*.001;
 battleShips.forEach((ship,i)=>{const flight=battlePose(time,i);ship.position.copy(flight.position);ship.lookAt(flight.position.add(flight.direction));ship.rotateZ(flight.bank)});
 battleBolts.forEach((bolt,i)=>{const ship=battleShips[i%6],phase=(time*.72+i*.17)%1;boltForward.set(0,0,1).applyQuaternion(ship.quaternion);bolt.position.copy(ship.position).addScaledVector(boltForward,phase*18+1.5);bolt.quaternion.copy(ship.quaternion);bolt.material.opacity=(1-phase)*.95});
}
function adaptedMap(source,type){
 if(type==='desert'||type==='lush')return source;
 const image=source?.image;if(!image)return source;
 const canvas=document.createElement('canvas');canvas.width=1024;canvas.height=512;
 const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(image,0,0,1024,512);
 const pixels=ctx.getImageData(0,0,1024,512),d=pixels.data;
 for(let y=0;y<512;y++)for(let x=0;x<1024;x++){
  const i=(y*1024+x)*4,l=(d[i]*.21+d[i+1]*.72+d[i+2]*.07)/255;
  if(type==='ice'){d[i]=105+l*138;d[i+1]=145+l*103;d[i+2]=175+l*78}
  else if(type==='lava'){
   const n=fbm(x/80,y/75,19),f=fbm(x/19,y/22,27);
   const fissure=Math.abs(Math.sin(x*.083+n*8)*Math.cos(y*.07+f*7));
   const hot=fissure<.085||n>.66&&f>.59;
   d[i]=hot?230:25+l*50;d[i+1]=hot?62+(1-fissure)*80:20+l*23;d[i+2]=hot?9:25+l*18;
  }else{
   const lit=(x%17<2||y%12<2)&&l>.28;
   d[i]=lit?234:39+l*93;d[i+1]=lit?184:48+l*98;d[i+2]=lit?117:67+l*112;
  }
 }
 ctx.putImageData(pixels,0,0);
 const map=new THREE.CanvasTexture(canvas);map.colorSpace=THREE.SRGBColorSpace;map.flipY=source.flipY;map.wrapS=source.wrapS;map.wrapT=source.wrapT;map.anisotropy=renderer.capabilities.getMaxAnisotropy();return map;
}
function usePlanetModel(worldIndex,gltf,scale){
  const w=worlds[worldIndex],model=worldIndex===2||worldIndex===4?gltf.scene:gltf.scene.clone(true);
  model.scale.setScalar(scale);
  model.traverse(object=>{
   if(object.isLight||object.isCamera)object.visible=false;
   if(!object.isMesh)return;
   const materialName=object.material?.name||'';
   if(/Atmosphere/i.test(object.name)||/Atmosphere/i.test(materialName)){object.visible=false;return}
   const isCloud=/Clouds/i.test(object.name)||/Clouds/i.test(materialName);
   object.material=object.material.clone();
   object.material.side=THREE.DoubleSide;
   if(isCloud){object.visible=false;return}
   object.material.map=adaptedMap(object.material.map,w.type);
   object.material.color.set(w.type==='desert'?'#e7b77c':w.type==='lush'?'#e1f2dd':'#ffffff');
   object.material.emissive.set(w.type==='lava'?'#4d1205':w.type==='city'?'#111724':'#000000');
   object.material.emissiveIntensity=w.type==='lava'?.5:w.type==='city'?.25:0;
   object.material.roughness=w.type==='city'?.74:.96;
   object.material.metalness=w.type==='city'?.2:0;
   w.modelSurface=object;
  });
  w.group.add(model);w.model=model;
  const clouds=new THREE.Mesh(sphereGeo,new THREE.MeshStandardMaterial({map:makeClouds(w),color:w.type==='desert'?'#eacb9c':w.type==='lava'?'#fa7041':'#effff6',transparent:true,opacity:{desert:.16,ice:.5,lush:.38,lava:.13,city:.22}[w.type],depthWrite:false,roughness:1}));clouds.scale.setScalar(w.r*1.018);w.group.add(clouds);w.cloud=clouds;
}
Promise.all([modelLoader.loadAsync('./assets/tatooine-base.glb'),modelLoader.loadAsync('./assets/naboo-base.glb'),modelLoader.loadAsync('./assets/naboo-base.glb')]).then(([purple,green,greenCity])=>{
 usePlanetModel(0,purple,worlds[0].r);
 usePlanetModel(1,purple,worlds[1].r);
 usePlanetModel(2,green,worlds[2].r/100);
 usePlanetModel(3,purple,worlds[3].r);
 usePlanetModel(4,greenCity,worlds[4].r/100);
 worlds.forEach(w=>{const globe=new THREE.Mesh(w.modelSurface.geometry,w.modelSurface.material);const cloud=new THREE.Mesh(sphereGeo,w.cloud.material);coverGroup.add(globe,cloud);coverPlanets.push({globe,cloud})});
 syncCoverPlanets();
}).catch(error=>console.error('Não foi possível carregar os modelos dos planetas:',error));
function syncCoverPlanets(){
 if(!coverPlanets.length||!document.querySelector('.cover-worlds'))return;
 camera.updateMatrixWorld();const ray=new THREE.Raycaster();
 document.querySelectorAll('.cover-orb').forEach((orb,i)=>{
  const rect=orb.getBoundingClientRect();const x=(rect.left+rect.width/2)/innerWidth*2-1,y=1-(rect.top+rect.height/2)/innerHeight*2;
  ray.setFromCamera(new THREE.Vector2(x,y),camera);
  const distance=(5-ray.ray.origin.z)/ray.ray.direction.z;
  const center=ray.ray.origin.clone().addScaledVector(ray.ray.direction,distance);
  const radius=rect.width/2*(2*Math.abs(distance)*Math.tan(THREE.MathUtils.degToRad(camera.fov/2))/innerHeight);
  const preview=coverPlanets[i];preview.globe.position.copy(center);preview.cloud.position.copy(center);
  preview.globe.scale.setScalar(radius);preview.cloud.scale.setScalar(radius*1.018);
 });
}
function makeClouds(w){let c=document.createElement('canvas');c.width=1024;c.height=512;let ctx=c.getContext('2d'),im=ctx.createImageData(1024,512),d=im.data,s=worlds.indexOf(w)+65;for(let y=0;y<512;y++)for(let x=0;x<1024;x++){let n=fbm(x/140,y/130,s),i=(y*1024+x)*4;d[i]=d[i+1]=d[i+2]=235;d[i+3]=Math.max(0,Math.min(210,(n-.49)*650))}ctx.putImageData(im,0,0);return new THREE.CanvasTexture(c)}
function glowTexture(){let c=document.createElement('canvas');c.width=c.height=128;let ctx=c.getContext('2d'),g=ctx.createRadialGradient(64,64,0,64,64,64);g.addColorStop(0,'rgba(255,255,240,1)');g.addColorStop(.13,'rgba(255,225,170,.75)');g.addColorStop(1,'rgba(255,145,40,0)');ctx.fillStyle=g;ctx.fillRect(0,0,128,128);return new THREE.CanvasTexture(c)}
const stars=[];let seed=741;function rand(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296}
let starGeo=new THREE.BufferGeometry(),verts=[],colors=[];for(let i=0;i<2300;i++){let x=(rand()-.5)*240,y=(rand()-.5)*125,z=(rand()-.5)*145-22;verts.push(x,y,z);let tint=rand();colors.push(tint>.87?1:.62,tint>.87?.83:.76,1)}starGeo.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));starGeo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));let starMat=new THREE.PointsMaterial({size:.11,vertexColors:true,transparent:true,opacity:.8,sizeAttenuation:true,depthWrite:false});scene.add(new THREE.Points(starGeo,starMat));
let nebula=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTexture(),color:0x394e82,transparent:true,opacity:.1,depthWrite:false,blending:THREE.AdditiveBlending}));nebula.position.set(37,6,-55);nebula.scale.set(105,55,1);scene.add(nebula);
const content=document.getElementById('content'),counter=document.getElementById('counter'),progress=document.querySelector('#progress span'),travelLabel=document.getElementById('travelLabel'),nextBtn=document.getElementById('next'),prevBtn=document.getElementById('prev');
const stages=[{kind:'cover'},...worlds.flatMap((_,i)=>[{kind:'intro',i},{kind:'facts',i}]),{kind:'end'}];let index=0,transition=null;
function panelHTML(stage){if(stage.kind==='cover')return `<section class="panel cover"><div class="cover-copy"><div class="eyebrow">STAR WARS · ATLAS DOS MUNDOS</div><h1>ALÉM DAS<br><em>ESTRELAS</em></h1><p class="cover-sub">CINCO PLANETAS. UMA ÚNICA TRAVESSIA.<br>DO SILÊNCIO DO ESPAÇO AO CORAÇÃO DA GALÁXIA.</p><button class="cue" type="button"><span>↗</span> INICIAR EXPLORAÇÃO</button></div><div class="cover-worlds">${worlds.map((w,i)=>`<button class="cover-world cover-world-${w.type}" type="button" data-world="${i}" aria-label="${w.name}"><span class="cover-orb" aria-hidden="true"></span><span class="cover-world-name">${w.name}</span></button>`).join('')}</div><div class="death-star-tag"><span>ESTRELA DA MORTE</span><small>ESTAÇÃO DE BATALHA / ÓRBITA EXTERIOR</small></div></section>`;
 if(stage.kind==='end')return `<section class="panel ending"><div class="eyebrow">FIM DA TRAJETÓRIA / 05 MUNDOS</div><h2>A GALÁXIA<br>CONTINUA.</h2><p>QUE A FORÇA ESTEJA COM VOCÊ.</p><p class="model-credits">Modelos 3D adaptados: <a href="https://sketchfab.com/3d-models/purple-planet-264eb22207184fc99a5e3b1279a763b8" target="_blank" rel="noopener">Purple Planet · Yo.Ri</a> e <a href="https://sketchfab.com/3d-models/green-planet-965dcf47e69e4c139741598162b147cf" target="_blank" rel="noopener">Green Planet · jimmyn64</a> · CC BY 4.0<br>Jabba the Font · Michael Moss · <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a></p></section>`;
 let w=worlds[stage.i],num=String(stage.i+1).padStart(2,'0');if(stage.kind==='intro')return `<section class="panel planet-hero" role="button" tabindex="0" aria-label="Ver detalhes de ${w.name}"><h2>${w.name}</h2></section>`;
 return `<section class="panel facts"><div class="facts-inner"><div class="facts-kicker">REGISTRO PLANETÁRIO / ${num}</div><h2>${w.name}</h2><ul class="fact-list"><li><span class="fact-label">REGIÃO</span><span class="fact-value">${w.region}</span></li><li><span class="fact-label">CLIMA</span><span class="fact-value">${w.climate}</span></li><li><span class="fact-label">VIDA</span><span class="fact-value">${w.life}</span></li><li><span class="fact-label">LEGADO</span><span class="fact-value">${w.event}</span></li></ul><div class="chapter">${w.coords} &nbsp; ◇ &nbsp; ARQUIVO ${num}/05</div></div></section>`}
function showStage(n){document.body.classList.remove('is-travelling');index=n;let stage=stages[n];document.body.classList.toggle('show-planet-hero',stage.kind==='intro');document.body.classList.toggle('show-cover',stage.kind==='cover');worldGroups.forEach(group=>group.visible=stage.kind!=='cover');coverGroup.visible=stage.kind==='cover';deathStar.visible=stage.kind==='cover';battle.visible=true;content.innerHTML=panelHTML(stage);if(stage.kind==='cover')requestAnimationFrame(syncCoverPlanets);if(stage.kind==='cover'){content.querySelector('.cover-copy').addEventListener('click',()=>startTransition(1));const map=content.querySelector('.cover-worlds');map.addEventListener('click',e=>{const buttons=[...map.querySelectorAll('.cover-world')];const target=e.target.closest('.cover-world')||buttons.reduce((a,b)=>Math.abs(b.getBoundingClientRect().left+b.offsetWidth/2-e.clientX)<Math.abs(a.getBoundingClientRect().left+a.offsetWidth/2-e.clientX)?b:a);startTransition(1+Number(target.dataset.world)*2)});buttonsForKeyboard(map)}requestAnimationFrame(()=>content.firstElementChild.classList.add('active'));let i=stage.i;counter.innerHTML=(i===undefined?(stage.kind==='end'?'05':'00'):String(i+1).padStart(2,'0'))+' <span>/</span> 05';progress.style.width=(n/(stages.length-1)*100)+'%';prevBtn.disabled=n===0;nextBtn.disabled=false;nextBtn.innerHTML=n===stages.length-1?'RECOMEÇAR <span>↺</span>':'PRÓXIMO <span>→</span>';document.documentElement.style.setProperty('--accent',i===undefined?'#e8c78c':worlds[i].atmo)}
function buttonsForKeyboard(map){map.querySelectorAll('.cover-world').forEach(button=>button.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();startTransition(1+Number(button.dataset.world)*2)}}))}
function pose(s){if(s.kind==='cover')return {p:new THREE.Vector3(36,2,68),t:new THREE.Vector3(36,0,0)};if(s.kind==='end')return {p:new THREE.Vector3(36,8,52),t:new THREE.Vector3(36,0,-4)};let w=worlds[s.i];if(s.kind==='intro')return {p:new THREE.Vector3(w.x,w.y+.35,w.z+(mobile?6.5:5.7)),t:new THREE.Vector3(w.x,w.y+(mobile?1.85:2.15),w.z)};return {p:new THREE.Vector3(w.x+(mobile?0:1.55),w.y+.15,w.z+(mobile?5.3:4.05)),t:new THREE.Vector3(w.x+(mobile?0:2.25),w.y-.2,w.z)}}
let current=pose(stages[0]);camera.position.copy(current.p);camera.lookAt(current.t);
function smooth(t){return t*t*(3-2*t)}
function startTransition(to){if(transition||opening||openingPending)return;if(to<0||to>=stages.length)return;let from=index,a=stages[from],b=stages[to],p0=pose(a),p1=pose(b),long=Math.abs(to-from)>1||a.kind==='cover'||b.kind==='end'||(a.i!==undefined&&b.i!==undefined&&a.i!==b.i);let points,looks,duration;const falconTransit=long&&!!falconModel;if(a.kind==='cover'){worldGroups.forEach(group=>group.visible=true);coverGroup.visible=false}
 if(long){let wa=a.i===undefined?worlds[0]:worlds[a.i],wb=b.i===undefined?worlds[4]:worlds[b.i];let mid=(wa.x+wb.x)/2;points=[p0.p,new THREE.Vector3(wa.x,wa.y+2,wa.z+13),new THREE.Vector3(mid,5,29),new THREE.Vector3(wb.x,wb.y+2,wb.z+16),p1.p];looks=[p0.t,new THREE.Vector3(wa.x,wa.y,wa.z),new THREE.Vector3(mid,0,-7),new THREE.Vector3(wb.x,wb.y,wb.z),p1.t];duration=a.kind==='cover'?3400:b.kind==='end'?3200:4400;travelLabel.classList.add('visible')}
 else{points=[p0.p,p1.p];looks=[p0.t,p1.t];duration=2200}
 let flight=null;if(falconTransit){flight=createFlight({from:{p:camera.position.clone(),quaternion:camera.quaternion.clone()},to:p1,shipPosition:falconRig.position.clone(),shipQuaternion:falconRig.quaternion.clone(),worlds});duration=flight.duration;falconDeparture=null}
 if(reducedMotion.matches){camera.position.copy(p1.p);camera.lookAt(p1.t);camera.fov=49;camera.updateProjectionMatrix();travelLabel.classList.remove('visible');showStage(to);return}
 document.body.classList.add('is-travelling');travelLabel.querySelector('span').textContent='ROTA EM CURSO';travelLabel.querySelector('small').textContent=b.i===undefined?'Atlas galáctico':worlds[b.i].name;content.firstElementChild?.classList.add('exit');nextBtn.disabled=prevBtn.disabled=true;transition={from,to,start:previewTime===null?performance.now():0,points,looks,duration,long,falconTransit,flight};}
function interpolate(points,t){if(points.length===2)return points[0].clone().lerp(points[1],smooth(t));let seg=Math.min(points.length-2,Math.floor(t*(points.length-1))),u=t*(points.length-1)-seg;let a=points[Math.max(0,seg-1)],b=points[seg],c=points[seg+1],d=points[Math.min(points.length-1,seg+2)];return new THREE.Vector3().copy(b).multiplyScalar(2).addScaledVector(c.clone().sub(a),u).addScaledVector(a.clone().multiplyScalar(2).addScaledVector(b,-5).addScaledVector(c,4).addScaledVector(d,-1),u*u).addScaledVector(a.clone().multiplyScalar(-1).addScaledVector(b,3).addScaledVector(c,-3).add(d),u*u*u).multiplyScalar(.5)}
function animate(now){if(previewTime===null)requestAnimationFrame(animate);const motionTime=reducedMotion.matches?0:now;for(let i=0;i<worlds.length;i++){let w=worlds[i];if(w.cloud)w.cloud.rotation.y=motionTime*.06*[.00042,.00115,.00072,.00035,.00027][i];if(w.modelSurface)w.modelSurface.rotation.y=motionTime*.06*[.00028,.00035,.00042,.00018,.00055][i];if(coverPlanets[i]){coverPlanets[i].globe.rotation.y=motionTime*.00003;coverPlanets[i].cloud.rotation.y=motionTime*.000048}}if(deathStarBody)deathStarBody.rotation.y=-.48+motionTime*.0000198;if(battleShips.length)animateBattle(motionTime);if(!transition?.flight&&!opening&&!openingPending)animateFalconIdle(motionTime);
 if(transition){
  const t=Math.min(1,(now-transition.start)/transition.duration),ease=smooth(t);
  if(transition.flight){const frame=transition.flight.sample(t);camera.position.copy(frame.position);camera.quaternion.copy(frame.quaternion);camera.fov=frame.fov;camera.updateProjectionMatrix();falconRig.visible=true;falconRig.position.copy(frame.ship);falconRig.quaternion.copy(frame.shipQuaternion)}
  else{camera.position.copy(interpolate(transition.points,ease));camera.lookAt(interpolate(transition.looks,ease));camera.rotation.z=Math.sin(Math.PI*t)*(transition.long?.022:.012)}
  starMat.size=transition.long?.11+Math.sin(Math.PI*t)*.12:.11;
  if(t>=1){const to=transition.to;if(transition.flight){const frame=transition.flight.sample(1);falconDeparture={start:now,position:frame.ship.clone(),quaternion:frame.shipQuaternion.clone(),direction:frame.tangent.clone()}}transition=null;camera.fov=49;camera.updateProjectionMatrix();travelLabel.classList.remove('visible');showStage(to)}
 }

 if(opening){const frame=opening.effect.update((now-opening.start)*.001);
  if(frame.done){falconDeparture={start:now,position:frame.ship.clone(),quaternion:frame.shipQuaternion.clone(),direction:frame.tangent.clone()};opening.effect.dispose();opening=null;document.body.classList.remove('opening-active');travelLabel.classList.remove('visible');syncCoverPlanets();syncDeathStar()}
 }
 renderer.render(scene,camera)}if(previewTime===null)requestAnimationFrame(animate);
nextBtn.addEventListener('click',()=>{if(index===stages.length-1){startTransition(0)}else startTransition(index+1)});prevBtn.addEventListener('click',()=>startTransition(index-1));content.addEventListener('click',()=>{if(stages[index].kind==='intro')startTransition(index+1)});content.addEventListener('keydown',e=>{if(stages[index].kind==='intro'&&e.key==='Enter'){e.preventDefault();startTransition(index+1)}});document.getElementById('home').addEventListener('click',e=>{e.preventDefault();startTransition(0)});
addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();startTransition(index===stages.length-1?0:index+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();startTransition(index-1)}});let wheelAt=0;addEventListener('wheel',e=>{if(Math.abs(e.deltaY)<15)return;let now=performance.now();if(now-wheelAt<900)return;wheelAt=now;startTransition(index+(e.deltaY>0?1:-1))},{passive:true});let touchY=0;addEventListener('touchstart',e=>touchY=e.touches[0].clientY,{passive:true});addEventListener('touchend',e=>{let d=touchY-e.changedTouches[0].clientY;if(Math.abs(d)>55)startTransition(index+(d>0?1:-1))},{passive:true});
addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));if(!opening&&stages[index].kind==='cover'){syncCoverPlanets();syncDeathStar();}});showStage(0);
if(!openingPending)document.getElementById('hyperspace-intro')?.remove();

// Instantes reproduzíveis para conferir partida, voo, chegada e retorno.
modelLoader.manager.onLoad=()=>requestAnimationFrame(()=>{
 document.body.dataset.modelsLoaded='true';
 if(openingPending){
  openingPending=false;const target=pose(stages[0]);
  if(falconModel){travelLabel.classList.add('visible');travelLabel.querySelector('span').textContent='ROTA EM CURSO';travelLabel.querySelector('small').textContent='Salto para a galáxia';opening={start:previewTime===null?performance.now():0,effect:playHyperspaceIntro({camera,scene,ship:falconRig,target})};opening.effect.update(0)}
  else document.body.classList.remove('opening-active');
  document.getElementById('hyperspace-intro')?.remove();
  if(previewTime!==null){animate(previewTime*1000);return}
 }

 if(previewTime!==null){
  const from=THREE.MathUtils.clamp(Number(previewParams.get('from')||previewParams.get('slide'))||0,0,stages.length-1);
  const initial=pose(stages[from]);camera.position.copy(initial.p);camera.lookAt(initial.t);showStage(from);animateFalconIdle(0);
  if(previewParams.get('shot')==='flight')startTransition(THREE.MathUtils.clamp(Number(previewParams.get('to'))||3,0,stages.length-1));
  animate(previewTime*1000);
 }
});
