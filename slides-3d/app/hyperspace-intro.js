import * as THREE from './vendor/three.module.js';

export const OPENING_DURATION=6.4;
const v=(x=0,y=0,z=0)=>new THREE.Vector3(x,y,z);
const clamp=t=>THREE.MathUtils.clamp(t,0,1);
const smooth=t=>{t=clamp(t);return t*t*(3-2*t)};
const smoother=t=>{t=clamp(t);return t*t*t*(t*(t*6-15)+10)};

// Tempos, câmera e saída da nave da abertura de ASIMOV-Universo-v2.
export function sampleOpening(seconds,target,scale=.45){
 const t=clamp(seconds/OPENING_DURATION),power=1-smoother((t-.69)/.27);
 const position=target.p.clone().add(v(0,12,420).multiplyScalar(scale*(1-smoother(t))));
 const quaternion=new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().lookAt(position,target.t,v(0,1,0)));
 const departure=smooth((t-.76)/.24);
 const ship=position.clone().add(v(.3,-1.65,-12).multiplyScalar(scale).applyQuaternion(quaternion));
 ship.lerp(target.p.clone().add(v(-35,-15,-92).multiplyScalar(scale)),departure);
 const shipQuaternion=quaternion.clone().multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(-.2,Math.PI,0,'YXZ')));
 const tangent=v(-35,-13,-80).normalize();
 shipQuaternion.slerp(new THREE.Quaternion().setFromUnitVectors(v(0,0,1),tangent),departure);
 return {position,quaternion,ship,shipQuaternion,tangent,power,occlusion:1-smoother((t-.7)/.18),fov:49+power*10,done:t>=1};
}

export function playHyperspaceIntro({camera,scene,ship,target,scale=.45}){
 const tunnelMaterial=new THREE.ShaderMaterial({transparent:true,depthTest:false,depthWrite:false,toneMapped:false,
  uniforms:{uTime:{value:0},uOpacity:{value:1},uAspect:{value:camera.aspect}},
  vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}',
  fragmentShader:`varying vec2 vUv;uniform float uTime,uOpacity,uAspect;
  void main(){vec2 p=(vUv-.5)*vec2(uAspect,1.);float r=length(p),a=atan(p.y,p.x);
   float flow=sin(a*41.+sin(a*17.)*2.+uTime*.23),thread=pow(max(0.,flow),16.);
   float ripples=pow(.5+.5*sin(log(r+.025)*19.-uTime*5.+sin(a*13.)),4.);
   float fog=smoothstep(.015,.35,r)*exp(-r*.9);
   vec3 color=vec3(.001,.003,.008)+vec3(.006,.04,.068)*fog;
   color+=vec3(.01,.1,.19)*thread*ripples*fog;gl_FragColor=vec4(color,uOpacity);
   #include <colorspace_fragment>
  }`});
 const tunnel=new THREE.Mesh(new THREE.PlaneGeometry(2,2),tunnelMaterial);tunnel.frustumCulled=false;tunnel.renderOrder=100;camera.add(tunnel);scene.add(camera);
 let seed=7819;const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 for(let i=0;i<68300;i++)random(); // Mesma sequência após os campos de estrelas da referência.
 const stars=Array.from({length:900},()=>({angle:random()*Math.PI*2,r:1.5+random()*38,z:random()*150,speed:.8+random()*.5}));
 const positions=new Float32Array(stars.length*6),geometry=new THREE.BufferGeometry();
 geometry.setAttribute('position',new THREE.BufferAttribute(positions,3).setUsage(THREE.DynamicDrawUsage));
 const streakMaterial=new THREE.LineBasicMaterial({color:new THREE.Color(.4,1.8,3),transparent:true,opacity:.85,blending:THREE.AdditiveBlending,depthWrite:false,depthTest:false});
 const streaks=new THREE.LineSegments(geometry,streakMaterial);streaks.frustumCulled=false;streaks.renderOrder=101;camera.add(streaks);
 // Halo fino dos rastros, equivalente ao brilho do pós-processamento da referência.
 const glowGeometry=new THREE.InstancedBufferGeometry();glowGeometry.setIndex([0,1,2,2,1,3]);
 glowGeometry.setAttribute('position',new THREE.Float32BufferAttribute([-1,0,0,1,0,0,-1,1,0,1,1,0],3));
 const starts=new Float32Array(stars.length*3),ends=new Float32Array(stars.length*3);
 glowGeometry.setAttribute('start',new THREE.InstancedBufferAttribute(starts,3).setUsage(THREE.DynamicDrawUsage));
 glowGeometry.setAttribute('end',new THREE.InstancedBufferAttribute(ends,3).setUsage(THREE.DynamicDrawUsage));glowGeometry.instanceCount=stars.length;
 const glowMaterial=new THREE.ShaderMaterial({transparent:true,depthTest:false,depthWrite:false,blending:THREE.AdditiveBlending,
  uniforms:{uOpacity:{value:1},uViewport:{value:new THREE.Vector2(innerWidth,innerHeight)}},
  vertexShader:`attribute vec3 start,end;uniform vec2 uViewport;varying float edge;
  void main(){vec4 a=projectionMatrix*vec4(start,1.),b=projectionMatrix*vec4(end,1.);vec2 d=(b.xy/b.w-a.xy/a.w)*uViewport;
   vec2 perpendicular=normalize(vec2(-d.y,d.x)+vec2(.00001));vec4 clip=mix(a,b,position.y);
   clip.xy+=perpendicular*position.x*14./uViewport*clip.w;gl_Position=clip;edge=position.x;}`,
  fragmentShader:'uniform float uOpacity;varying float edge;void main(){gl_FragColor=vec4(.12,.65,1.,exp(-edge*edge*6.)*.35*uOpacity);}'});
 const streakGlow=new THREE.Mesh(glowGeometry,glowMaterial);streakGlow.frustumCulled=false;streakGlow.renderOrder=100.5;camera.add(streakGlow);
 // A Falcon precisa ser desenhada à frente do túnel, preservando seus materiais.
 const alignment=ship.children[0],originalAlignment=alignment.quaternion.clone();alignment.quaternion.identity();
 const meshState=[],materials=new Map();
 ship.traverse(node=>{if(!node.isMesh)return;meshState.push([node,node.renderOrder]);node.renderOrder=102;
  for(const material of Array.isArray(node.material)?node.material:[node.material])if(!materials.has(material)){materials.set(material,material.transparent);material.transparent=true;material.needsUpdate=true}
 });
 const engineMaterial=new THREE.MeshBasicMaterial({color:new THREE.Color(1.5,3.2,4.2),transparent:true,opacity:.85,depthWrite:false});
 const engine=new THREE.Mesh(new THREE.SphereGeometry(1,16,8),engineMaterial);engine.scale.set(.29*5.4*scale,.025*5.4*scale,.022*5.4*scale);engine.position.set(0,.02*5.4*scale,-.37*5.4*scale);engine.renderOrder=103;ship.add(engine);
 const glowCanvas=document.createElement('canvas');glowCanvas.width=glowCanvas.height=128;const ctx=glowCanvas.getContext('2d'),gradient=ctx.createRadialGradient(64,64,0,64,64,64);
 gradient.addColorStop(0,'rgba(180,245,255,.9)');gradient.addColorStop(.2,'rgba(60,200,255,.5)');gradient.addColorStop(1,'rgba(20,140,255,0)');ctx.fillStyle=gradient;ctx.fillRect(0,0,128,128);
 const engineTexture=new THREE.CanvasTexture(glowCanvas),engineGlow=new THREE.Sprite(new THREE.SpriteMaterial({map:engineTexture,transparent:true,opacity:.8,blending:THREE.AdditiveBlending,depthWrite:false,depthTest:false}));
 engineGlow.material.color.setRGB(.5,2.5,4);engineGlow.position.copy(engine.position);engineGlow.scale.set(6*scale,2*scale,1);engineGlow.renderOrder=104;ship.add(engineGlow);
 let disposed=false;
 return {
  update(seconds){
   const frame=sampleOpening(seconds,target,scale);alignment.quaternion.identity().slerp(originalAlignment,smooth((seconds/OPENING_DURATION-.9)/.1));camera.position.copy(frame.position);camera.quaternion.copy(frame.quaternion);camera.fov=frame.fov;camera.updateProjectionMatrix();
   ship.visible=true;ship.position.copy(frame.ship);ship.quaternion.copy(frame.shipQuaternion);
   tunnelMaterial.uniforms.uTime.value=seconds;tunnelMaterial.uniforms.uOpacity.value=frame.occlusion;tunnelMaterial.uniforms.uAspect.value=camera.aspect;tunnel.visible=frame.occlusion>0;
   streakMaterial.opacity=frame.power*.85;glowMaterial.uniforms.uOpacity.value=frame.power;glowMaterial.uniforms.uViewport.value.set(innerWidth,innerHeight);
   stars.forEach((star,i)=>{const z=-2-((star.z-seconds*130*star.speed)%150+150)%150,x=Math.cos(star.angle)*star.r,y=Math.sin(star.angle)*star.r;
    // Segments crossing the eye are clipped just in front of the near plane.
    const endZ=Math.min(-.11,z+3+frame.power*24);
    positions.set([x,y,z,x*1.045,y*1.045,endZ],i*6);starts.set([x,y,z],i*3);ends.set([x*1.045,y*1.045,endZ],i*3);
   });geometry.attributes.position.needsUpdate=true;glowGeometry.attributes.start.needsUpdate=true;glowGeometry.attributes.end.needsUpdate=true;
   const engineFade=1-smooth((seconds/OPENING_DURATION-.92)/.08);engineGlow.material.opacity=.8*engineFade;engineMaterial.opacity=.85*engineFade;
   return frame;
  },
  dispose(){if(disposed)return;disposed=true;alignment.quaternion.copy(originalAlignment);
   for(const [node,order] of meshState)node.renderOrder=order;
   for(const [material,transparent] of materials){material.transparent=transparent;material.needsUpdate=true}
   for(const object of [tunnel,streaks,streakGlow,engine,engineGlow]){object.removeFromParent();object.geometry?.dispose();object.material.dispose()}engineTexture.dispose();
  }
 };
}
