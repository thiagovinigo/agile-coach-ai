import * as THREE from './vendor/three.module.js';

const v=(x=0,y=0,z=0)=>new THREE.Vector3(x,y,z);
const ease=t=>{t=THREE.MathUtils.clamp(t,0,1);return t*t*(3-2*t)};
export const viewQuaternion=(position,target)=>new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().lookAt(position,target,v(0,1,0)));

// Curvas e acompanhamento do ASIMOV-Universo-v2, dimensionados para este atlas.
export function createFlight({from,to,shipPosition,shipQuaternion,worlds,scale=.45}){
 const offset=(x,y,z)=>v(x*scale,y*scale,z*scale);
 const q0=from.quaternion.clone(),q1=viewQuaternion(to.p,to.t);
 const avoid=(point,padding)=>{
  const result=point.clone();
  for(let pass=0;pass<3;pass++)for(const w of worlds){
   const center=v(w.x,w.y,w.z),delta=result.clone().sub(center),radius=w.r+padding,distance=delta.length();
   if(distance<radius){if(distance<1e-5)delta.set(0,0,1);else delta.divideScalar(distance);result.copy(center).addScaledVector(delta,radius)}
  }
  return result;
 };
 const mid=from.p.clone().lerp(to.p,.5);
 mid.y=Math.max(from.p.y,to.p.y)+9*scale;
 mid.z=Math.max(from.p.z,to.p.z,shipPosition.z,32*scale)+24*scale;
 const cameraPath=new THREE.CatmullRomCurve3([
  from.p,from.p.clone().add(offset(0,5,22).applyQuaternion(q0)),mid,
  to.p.clone().add(offset(0,5,18).applyQuaternion(q1)),to.p
 ],false,'centripetal');
 const arrival=to.p.clone().add(offset(-18,-5,-7).applyQuaternion(q1));
 const shipPath=new THREE.CatmullRomCurve3([
  shipPosition,shipPosition.clone().add(offset(0,0,10).applyQuaternion(shipQuaternion)),
  mid.clone().add(offset(0,-3,-25)),arrival.clone().add(offset(10,2,4).applyQuaternion(q1)),arrival
 ],false,'centripetal');
 function shipAt(t){
  const u=ease(t),q=q0.clone().slerp(q1,u),cameraPoint=avoid(cameraPath.getPointAt(u),2.2*scale);
  const pathPoint=shipPath.getPoint(cameraPath.getUtoTmapping(u));
  const chase=cameraPoint.clone().add(offset(-2.2,-1.6,-18).applyQuaternion(q));
  return avoid(pathPoint.lerp(chase,ease(t/.24)*(1-ease((t-.76)/.24))),4*scale);
 }
 const tracking=new THREE.CatmullRomCurve3([0,.25,.5,.75,1].map(t=>{
  if(t===0||t===1)return v();
  const u=ease(t),q=q0.clone().slerp(q1,u);
  const relative=shipAt(t).sub(cameraPath.getPointAt(u)).applyQuaternion(q.invert());
  const distance=relative.length(),forward=-relative.z/Math.max(distance,.001);
  const weight=ease((forward-.15)/.4)*ease((distance-8*scale)/(8*scale));
  return v(.32*Math.tanh(-Math.atan2(relative.x,-relative.z)/.32)*weight,.16*Math.tanh(Math.atan2(relative.y,Math.hypot(relative.x,relative.z))/.16)*weight,0);
 }),false,'catmullrom',.35);
 return {
  duration:Math.max(6.2,q0.angleTo(q1)*1.875/.58)*1000,
  sample(t){
   t=THREE.MathUtils.clamp(t,0,1);const u=ease(t);
   const position=avoid(cameraPath.getPointAt(u),2.2*scale),ship=shipAt(t);
   const tangent=shipAt(Math.min(1,t+.001)).sub(shipAt(Math.max(0,t-.001))).normalize();
   const quaternion=q0.clone().slerp(q1,u),track=tracking.getPoint(t).multiplyScalar(Math.sin(Math.PI*t)**2);
   quaternion.multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(track.y,track.x,0,'YXZ')));
   const shipRotation=new THREE.Quaternion().setFromUnitVectors(v(0,0,1),tangent);
   shipRotation.multiply(new THREE.Quaternion().setFromAxisAngle(v(0,0,1),Math.sin(Math.PI*t*2)*-.16));
   shipRotation.slerp(shipQuaternion,1-ease(t/.2));
   return {position,quaternion,ship,shipQuaternion:shipRotation,tangent,fov:49+Math.sin(Math.PI*t)**2*4};
  }
 };
}

export function battlePose(time,index){
 const angle=time*(.09+index%3*.016)+index*1.13,radius=35+index%3*9;
 return {
  position:v(36+Math.cos(angle)*radius,8+Math.sin(angle*1.7+index)*9,-45+Math.sin(angle)*23),
  direction:v(-Math.sin(angle)*radius,Math.cos(angle*1.7+index)*15,Math.cos(angle)*23),
  bank:Math.sin(angle+index)*.4
 };
}
