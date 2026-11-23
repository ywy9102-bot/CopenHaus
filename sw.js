/* Copen Haus 가이드북 오프라인 지원
   - 페이지와 그림: 인터넷이 되면 늘 새 내용을 받아 오고(network-first), 안 되면 저장해 둔 내용을 보여줘요.
   - 글꼴: 한 번 받으면 저장해 둔 것을 써요.
   가이드 내용을 고치면 별도 작업 없이 다음 접속 때 반영돼요. */
var CACHE='copenhaus-v1';
var CORE=['./','index.html','hero.jpg','qr.png','favicon.png','apple-touch-icon.png','icon-192.png','manifest.webmanifest',
  'img/boiler.png','img/washer.png','img/dryer.png','img/microwave.png','img/induction.png','img/remote.png',
  'img/route.png','img/overview.jpg','img/entrance.jpg','img/alley.jpg'];
self.addEventListener('install',function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){return Promise.all(CORE.map(function(u){return c.add(u).catch(function(){})}))}).then(function(){return self.skipWaiting()}));
});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k!==CACHE}).map(function(k){return caches.delete(k)}))}).then(function(){return self.clients.claim()}));
});
self.addEventListener('fetch',function(e){
  var r=e.request;if(r.method!=='GET')return;
  var u=new URL(r.url);
  if(/fonts\.(googleapis|gstatic)\.com$/.test(u.hostname)){
    e.respondWith(caches.match(r).then(function(hit){return hit||fetch(r).then(function(res){var cp=res.clone();caches.open(CACHE).then(function(c){c.put(r,cp)});return res})}));
    return;
  }
  if(u.origin!==self.location.origin)return;
  e.respondWith(fetch(r).then(function(res){
    if(res&&res.ok){var cp=res.clone();caches.open(CACHE).then(function(c){c.put(r,cp)})}
    return res;
  }).catch(function(){
    return caches.match(r,{ignoreSearch:true}).then(function(hit){return hit||(r.mode==='navigate'?caches.match('./'):null)}).then(function(hit){return hit||Response.error()});
  }));
});
