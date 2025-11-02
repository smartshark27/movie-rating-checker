import json
import re
import requests
from bs4 import BeautifulSoup

collection_urls = {
    "movies": "https://10.com.au/shows/movie",
    "shows-comedy": "https://10.com.au/shows/comedy",
    "shows-drama": "https://10.com.au/shows/drama",
    "shows-kids": "https://10.com.au/shows/kids",
}


def get_10play_media_list(collection="movies"):
    """
    Fetch all media from a collection from the 10 Play catalogue.
    """
    if collection not in collection_urls:
        raise ValueError(
            f"Invalid collection '{collection}'. Must be one of {list(collection_urls.keys())}."
        )
    url = collection_urls[collection]

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find <div class="content__wrapper--inner"> then search its <script>s
        wrapper = soup.find("div", class_="content__wrapper--inner")
        if wrapper:
            for script in wrapper.find_all("script"):
                if script.string and "const showsPageData" in script.string:
                    script_with_data = script.string
                    break
        else:
            raise ValueError("Couldn't find content wrapper div")

        # Extract JSON inside const showsPageData = {...};
        match = re.search(
            r"const\s+showsPageData\s*=\s*(\{.*?\});", script_with_data, re.DOTALL
        )

        if not match:
            raise ValueError("Found script but couldn't extract JSON")

        json_str = match.group(1)

        # Convert JS object → valid JSON
        data = json.loads(json_str)["shows"]

        media_list = [
            {
                "mediaType": "movie" if "Movies" in item["genres"] else "show",
                "title": item["name"],
                "10PlayURL": item["url"],
            }
            for item in data
        ]

        print(f"Total media found: {len(media_list)}")
        return media_list
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")


if __name__ == "__main__":
    media_list = get_10play_media_list()
    print("media:", media_list)

# Example HTML
# <!DOCTYPE html>\n
# <html lang="en-AU" style="--theme-color: #0047f4">
#   \n<head>
#     \n
#     <title>Shows for Movies - Network Ten</title>
#     \n
#     <meta charset="utf-8" />
#     <script type="text/javascript">
#       window.NREUM || (NREUM = {});
#       NREUM.info = {
#         beacon: "bam.nr-data.net",
#         errorBeacon: "bam.nr-data.net",
#         licenseKey: "9e41ccb5c5",
#         applicationID: "303663362",
#         transactionName:
#           "Z1BUZhRZV0RSB0FZDl4ae2QlF2pfXBNGHyheUVNKSUNeUl0WUHkFVVtCWwBRXEVOS05DDkJBclsUXVpDWgtbTU5LRllAEkU=",
#         queueTime: 0,
#         applicationTime: 329,
#         agent: "",
#         atts: "",
#       };
#     </script>
#     <script type="text/javascript">
#       (window.NREUM||(NREUM={})).init={ajax:{deny_list:["bam.nr-data.net"]}};(window.NREUM||(NREUM={})).loader_config={licenseKey:"9e41ccb5c5",applicationID:"303663362",browserID:"1103290072"};;/*! For license information please see nr-loader-rum-1.302.0.min.js.LICENSE.txt */\n(()=>{var e,t,r={122:(e,t,r)=>{"use strict";r.d(t,{a:()=>i});var n=r(944);function i(e,t){try{if(!e||"object"!=typeof e)return(0,n.R)(3);if(!t||"object"!=typeof t)return(0,n.R)(4);const r=Object.create(Object.getPrototypeOf(t),Object.getOwnPropertyDescriptors(t)),a=0===Object.keys(r).length?e:r;for(let o in a)if(void 0!==e[o])try{if(null===e[o]){r[o]=null;continue}Array.isArray(e[o])&&Array.isArray(t[o])?r[o]=Array.from(new Set([...e[o],...t[o]])):"object"==typeof e[o]&&"object"==typeof t[o]?r[o]=i(e[o],t[o]):r[o]=e[o]}catch(e){r[o]||(0,n.R)(1,e)}return r}catch(e){(0,n.R)(2,e)}}},154:(e,t,r)=>{"use strict";r.d(t,{OF:()=>c,RI:()=>i,WN:()=>u,bv:()=>a,gm:()=>o,mw:()=>s,sb:()=>d});var n=r(863);const i="undefined"!=typeof window&&!!window.document,a="undefined"!=typeof WorkerGlobalScope&&("undefined"!=typeof self&&self instanceof WorkerGlobalScope&&self.navigator instanceof WorkerNavigator||"undefined"!=typeof globalThis&&globalThis instanceof WorkerGlobalScope&&globalThis.navigator instanceof WorkerNavigator),o=i?window:"undefined"!=typeof WorkerGlobalScope&&("undefined"!=typeof self&&self instanceof WorkerGlobalScope&&self||"undefined"!=typeof globalThis&&globalThis instanceof WorkerGlobalScope&&globalThis),s=Boolean("hidden"===o?.document?.visibilityState),c=/iPad|iPhone|iPod/.test(o.navigator?.userAgent),d=c&&"undefined"==typeof SharedWorker,u=((()=>{const e=o.navigator?.userAgent?.match(/Firefox[/\\s](\\d+\\.\\d+)/);Array.isArray(e)&&e.length>=2&&e[1]})(),Date.now()-(0,n.t)())},163:(e,t,r)=>{"use strict";r.d(t,{j:()=>T});var n=r(384),i=r(741);var a=r(555);r(860).K7.genericEvents;const o="experimental.resources",s="register",c=e=>{if(!e||"string"!=typeof e)return!1;try{document.createDocumentFragment().querySelector(e)}catch{return!1}return!0};var d=r(614),u=r(944),l=r(122);const f="[data-nr-mask]",g=e=>(0,l.a)(e,(()=>{const e={feature_flags:[],experimental:{allow_registered_children:!1,resources:!1},mask_selector:"*",block_selector:"[data-nr-block]",mask_input_options:{color:!1,date:!1,"datetime-local":!1,email:!1,month:!1,number:!1,range:!1,search:!1,tel:!1,text:!1,time:!1,url:!1,week:!1,textarea:!1,select:!1,password:!0}};return{ajax:{deny_list:void 0,block_internal:!0,enabled:!0,autoStart:!0},api:{get allow_registered_children(){return e.feature_flags.includes(s)||e.experimental.allow_registered_children},set allow_registered_children(t){e.experimental.allow_registered_children=t},duplicate_registered_data:!1},distributed_tracing:{enabled:void 0,exclude_newrelic_header:void 0,cors_use_newrelic_header:void 0,cors_use_tracecontext_headers:void 0,allowed_origins:void 0},get feature_flags(){return e.feature_flags},set feature_flags(t){e.feature_flags=t},generic_events:{enabled:!0,autoStart:!0},harvest:{interval:30},jserrors:{enabled:!0,autoStart:!0},logging:{enabled:!0,autoStart:!0},metrics:{enabled:!0,autoStart:!0},obfuscate:void 0,page_action:{enabled:!0},page_view_event:{enabled:!0,autoStart:!0},page_view_timing:{enabled:!0,autoStart:!0},performance:{capture_marks:!1,capture_measures:!1,capture_detail:!0,resources:{get enabled(){return e.feature_flags.includes(o)||e.experimental.resources},set enabled(t){e.experimental.resources=t},asset_types:[],first_party_domains:[],ignore_newrelic:!0}},privacy:{cookies_enabled:!0},proxy:{assets:void 0,beacon:void 0},session:{expiresMs:d.wk,inactiveMs:d.BB},session_replay:{autoStart:!0,enabled:!1,preload:!1,sampling_rate:10,error_sampling_rate:100,collect_fonts:!1,inline_images:!1,fix_stylesheets:!0,mask_all_inputs:!0,get mask_text_selector(){return e.mask_selector},set mask_text_selector(t){c(t)?e.mask_selector="".concat(t,",").concat(f):""===t||null===t?e.mask_selector=f:(0,u.R)(5,t)},get block_class(){return"nr-block"},get ignore_class(){return"nr-ignore"},get mask_text_class(){return"nr-mask"},get block_selector(){return e.block_selector},set block_selector(t){c(t)?e.block_selector+=",".concat(t):""!==t&&(0,u.R)(6,t)},get mask_input_options(){return e.mask_input_options},set mask_input_options(t){t&&"object"==typeof t?e.mask_input_options={...t,password:!0}:(0,u.R)(7,t)}},session_trace:{enabled:!0,autoStart:!0},soft_navigations:{enabled:!0,autoStart:!0},spa:{enabled:!0,autoStart:!0},ssl:void 0,user_actions:{enabled:!0,elementAttributes:["id","className","tagName","type"]}}})());var p=r(154),m=r(324);let h=0;const v={buildEnv:m.F3,distMethod:m.Xs,version:m.xv,originTime:p.WN},b={appMetadata:{},customTransaction:void 0,denyList:void 0,disabled:!1,harvester:void 0,isolatedBacklog:!1,isRecording:!1,loaderType:void 0,maxBytes:3e4,obfuscator:void 0,onerror:void 0,ptid:void 0,releaseIds:{},session:void 0,timeKeeper:void 0,registeredEntities:[],jsAttributesMetadata:{bytes:0},get harvestCount(){return++h}},y=e=>{const t=(0,l.a)(e,b),r=Object.keys(v).reduce((e,t)=>(e[t]={value:v[t],writable:!1,configurable:!0,enumerable:!0},e),{});return Object.defineProperties(t,r)};var _=r(701);const w=e=>{const t=e.startsWith("http");e+="/",r.p=t?e:"https://"+e};var x=r(836),k=r(241);const S={accountID:void 0,trustKey:void 0,agentID:void 0,licenseKey:void 0,applicationID:void 0,xpid:void 0},A=e=>(0,l.a)(e,S),R=new Set;function T(e,t={},r,o){let{init:s,info:c,loader_config:d,runtime:u={},exposed:l=!0}=t;if(!c){const e=(0,n.pV)();s=e.init,c=e.info,d=e.loader_config}e.init=g(s||{}),e.loader_config=A(d||{}),c.jsAttributes??={},p.bv&&(c.jsAttributes.isWorker=!0),e.info=(0,a.D)(c);const f=e.init,m=[c.beacon,c.errorBeacon];R.has(e.agentIdentifier)||(f.proxy.assets&&(w(f.proxy.assets),m.push(f.proxy.assets)),f.proxy.beacon&&m.push(f.proxy.beacon),e.beacons=[...m],function(e){const t=(0,n.pV)();Object.getOwnPropertyNames(i.W.prototype).forEach(r=>{const n=i.W.prototype[r];if("function"!=typeof n||"constructor"===n)return;let a=t[r];e[r]&&!1!==e.exposed&&"micro-agent"!==e.runtime?.loaderType&&(t[r]=(...t)=>{const n=e[r](...t);return a?a(...t):n})})}(e),(0,n.US)("activatedFeatures",_.B),e.runSoftNavOverSpa&&=!0===f.soft_navigations.enabled&&f.feature_flags.includes("soft_nav")),u.denyList=[...f.ajax.deny_list||[],...f.ajax.block_internal?m:[]],u.ptid=e.agentIdentifier,u.loaderType=r,e.runtime=y(u),R.has(e.agentIdentifier)||(e.ee=x.ee.get(e.agentIdentifier),e.exposed=l,(0,k.W)({agentIdentifier:e.agentIdentifier,drained:!!_.B?.[e.agentIdentifier],type:"lifecycle",name:"initialize",feature:void 0,data:e.config})),R.add(e.agentIdentifier)}},234:(e,t,r)=>{"use strict";r.d(t,{W:()=>a});var n=r(836),i=r(687);class a{constructor(e,t){this.agentIdentifier=e,this.ee=n.ee.get(e),this.featureName=t,this.blocked=!1}deregisterDrain(){(0,i.x3)(this.agentIdentifier,this.featureName)}}},241:(e,t,r)=>{"use strict";r.d(t,{W:()=>a});var n=r(154);const i="newrelic";function a(e={}){try{n.gm.dispatchEvent(new CustomEvent(i,{detail:e}))}catch(e){}}},261:(e,t,r)=>{"use strict";r.d(t,{$9:()=>d,BL:()=>s,CH:()=>g,Dl:()=>_,Fw:()=>y,PA:()=>h,Pl:()=>n,Tb:()=>l,U2:()=>a,V1:()=>k,Wb:()=>x,bt:()=>b,cD:()=>v,d3:()=>w,dT:()=>c,eY:()=>p,fF:()=>f,hG:()=>i,k6:()=>o,nb:()=>m,o5:()=>u});const n="api-",i="addPageAction",a="addToTrace",o="addRelease",s="finished",c="interaction",d="log",u="noticeError",l="pauseReplay",f="recordCustomEvent",g="recordReplay",p="register",m="setApplicationVersion",h="setCurrentRouteName",v="setCustomAttribute",b="setErrorHandler",y="setPageViewName",_="setUserId",w="start",x="wrapLogger",k="measure"},289:(e,t,r)=>{"use strict";r.d(t,{GG:()=>a,Qr:()=>s,sB:()=>o});var n=r(878);function i(){return"undefined"==typeof document||"complete"===document.readyState}function a(e,t){if(i())return e();(0,n.sp)("load",e,t)}function o(e){if(i())return e();(0,n.DD)("DOMContentLoaded",e)}function s(e){if(i())return e();(0,n.sp)("popstate",e)}},324:(e,t,r)=>{"use strict";r.d(t,{F3:()=>i,Xs:()=>a,xv:()=>n});const n="1.302.0",i="PROD",a="CDN"},374:(e,t,r)=>{r.nc=(()=>{try{return document?.currentScript?.nonce}catch(e){}return""})()},384:(e,t,r)=>{"use strict";r.d(t,{NT:()=>o,US:()=>u,Zm:()=>s,bQ:()=>d,dV:()=>c,pV:()=>l});var n=r(154),i=r(863),a=r(910);const o={beacon:"bam.nr-data.net",errorBeacon:"bam.nr-data.net"};function s(){return n.gm.NREUM||(n.gm.NREUM={}),void 0===n.gm.newrelic&&(n.gm.newrelic=n.gm.NREUM),n.gm.NREUM}function c(){let e=s();return e.o||(e.o={ST:n.gm.setTimeout,SI:n.gm.setImmediate||n.gm.setInterval,CT:n.gm.clearTimeout,XHR:n.gm.XMLHttpRequest,REQ:n.gm.Request,EV:n.gm.Event,PR:n.gm.Promise,MO:n.gm.MutationObserver,FETCH:n.gm.fetch,WS:n.gm.WebSocket},(0,a.i)(...Object.values(e.o))),e}function d(e,t){let r=s();r.initializedAgents??={},t.initializedAt={ms:(0,i.t)(),date:new Date},r.initializedAgents[e]=t}function u(e,t){s()[e]=t}function l(){return function(){let e=s();const t=e.info||{};e.info={beacon:o.beacon,errorBeacon:o.errorBeacon,...t}}(),function(){let e=s();const t=e.init||{};e.init={...t}}(),c(),function(){let e=s();const t=e.loader_config||{};e.loader_config={...t}}(),s()}},389:(e,t,r)=>{"use strict";function n(e,t=500,r={}){const n=r?.leading||!1;let i;return(...r)=>{n&&void 0===i&&(e.apply(this,r),i=setTimeout(()=>{i=clearTimeout(i)},t)),n||(clearTimeout(i),i=setTimeout(()=>{e.apply(this,r)},t))}}function i(e){let t=!1;return(...r)=>{t||(t=!0,e.apply(this,r))}}r.d(t,{J:()=>i,s:()=>n})},555:(e,t,r)=>{"use strict";r.d(t,{D:()=>s,f:()=>o});var n=r(384),i=r(122);const a={beacon:n.NT.beacon,errorBeacon:n.NT.errorBeacon,licenseKey:void 0,applicationID:void 0,sa:void 0,queueTime:void 0,applicationTime:void 0,ttGuid:void 0,user:void 0,account:void 0,product:void 0,extra:void 0,jsAttributes:{},userAttributes:void 0,atts:void 0,transactionName:void 0,tNamePlain:void 0};function o(e){try{return!!e.licenseKey&&!!e.errorBeacon&&!!e.applicationID}catch(e){return!1}}const s=e=>(0,i.a)(e,a)},566:(e,t,r)=>{"use strict";r.d(t,{LA:()=>s,bz:()=>o});var n=r(154);const i="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx";function a(e,t){return e?15&e[t]:16*Math.random()|0}function o(){const e=n.gm?.crypto||n.gm?.msCrypto;let t,r=0;return e&&e.getRandomValues&&(t=e.getRandomValues(new Uint8Array(30))),i.split("").map(e=>"x"===e?a(t,r++).toString(16):"y"===e?(3&a()|8).toString(16):e).join("")}function s(e){const t=n.gm?.crypto||n.gm?.msCrypto;let r,i=0;t&&t.getRandomValues&&(r=t.getRandomValues(new Uint8Array(e)));const o=[];for(var s=0;s<e;s++)o.push(a(r,i++).toString(16));return o.join("")}},606:(e,t,r)=>{"use strict";r.d(t,{i:()=>a});var n=r(908);a.on=o;var i=a.handlers={};function a(e,t,r,a){o(a||n.d,i,e,t,r)}function o(e,t,r,i,a){a||(a="feature"),e||(e=n.d);var o=t[a]=t[a]||{};(o[r]=o[r]||[]).push([e,i])}},607:(e,t,r)=>{"use strict";r.d(t,{W:()=>n});const n=(0,r(566).bz)()},614:(e,t,r)=>{"use strict";r.d(t,{BB:()=>o,H3:()=>n,g:()=>d,iL:()=>c,tS:()=>s,uh:()=>i,wk:()=>a});const n="NRBA",i="SESSION",a=144e5,o=18e5,s={STARTED:"session-started",PAUSE:"session-pause",RESET:"session-reset",RESUME:"session-resume",UPDATE:"session-update"},c={SAME_TAB:"same-tab",CROSS_TAB:"cross-tab"},d={OFF:0,FULL:1,ERROR:2}},630:(e,t,r)=>{"use strict";r.d(t,{T:()=>n});const n=r(860).K7.pageViewEvent},646:(e,t,r)=>{"use strict";r.d(t,{y:()=>n});class n{constructor(e){this.contextId=e}}},687:(e,t,r)=>{"use strict";r.d(t,{Ak:()=>d,Ze:()=>f,x3:()=>u});var n=r(241),i=r(836),a=r(606),o=r(860),s=r(646);const c={};function d(e,t){const r={staged:!1,priority:o.P3[t]||0};l(e),c[e].get(t)||c[e].set(t,r)}function u(e,t){e&&c[e]&&(c[e].get(t)&&c[e].delete(t),p(e,t,!1),c[e].size&&g(e))}function l(e){if(!e)throw new Error("agentIdentifier required");c[e]||(c[e]=new Map)}function f(e="",t="feature",r=!1){if(l(e),!e||!c[e].get(t)||r)return p(e,t);c[e].get(t).staged=!0,g(e)}function g(e){const t=Array.from(c[e]);t.every(([e,t])=>t.staged)&&(t.sort((e,t)=>e[1].priority-t[1].priority),t.forEach(([t])=>{c[e].delete(t),p(e,t)}))}function p(e,t,r=!0){const o=e?i.ee.get(e):i.ee,c=a.i.handlers;if(!o.aborted&&o.backlog&&c){if((0,n.W)({agentIdentifier:e,type:"lifecycle",name:"drain",feature:t}),r){const e=o.backlog[t],r=c[t];if(r){for(let t=0;e&&t<e.length;++t)m(e[t],r);Object.entries(r).forEach(([e,t])=>{Object.values(t||{}).forEach(t=>{t[0]?.on&&t[0]?.context()instanceof s.y&&t[0].on(e,t[1])})})}}o.isolatedBacklog||delete c[t],o.backlog[t]=null,o.emit("drain-"+t,[])}}function m(e,t){var r=e[1];Object.values(t[r]||{}).forEach(t=>{var r=e[0];if(t[0]===r){var n=t[1],i=e[3],a=e[2];n.apply(i,a)}})}},699:(e,t,r)=>{"use strict";r.d(t,{It:()=>a,KC:()=>s,No:()=>i,qh:()=>o});var n=r(860);const i=16e3,a=1e6,o="SESSION_ERROR",s={[n.K7.logging]:!0,[n.K7.genericEvents]:!1,[n.K7.jserrors]:!1,[n.K7.ajax]:!1}},701:(e,t,r)=>{"use strict";r.d(t,{B:()=>a,t:()=>o});var n=r(241);const i=new Set,a={};function o(e,t){const r=t.agentIdentifier;a[r]??={},e&&"object"==typeof e&&(i.has(r)||(t.ee.emit("rumresp",[e]),a[r]=e,i.add(r),(0,n.W)({agentIdentifier:r,loaded:!0,drained:!0,type:"lifecycle",name:"load",feature:void 0,data:e})))}},741:(e,t,r)=>{"use strict";r.d(t,{W:()=>a});var n=r(944),i=r(261);class a{#e(e,...t){if(this[e]!==a.prototype[e])return this[e](...t);(0,n.R)(35,e)}addPageAction(e,t){return this.#e(i.hG,e,t)}register(e){return this.#e(i.eY,e)}recordCustomEvent(e,t){return this.#e(i.fF,e,t)}setPageViewName(e,t){return this.#e(i.Fw,e,t)}setCustomAttribute(e,t,r){return this.#e(i.cD,e,t,r)}noticeError(e,t){return this.#e(i.o5,e,t)}setUserId(e){return this.#e(i.Dl,e)}setApplicationVersion(e){return this.#e(i.nb,e)}setErrorHandler(e){return this.#e(i.bt,e)}addRelease(e,t){return this.#e(i.k6,e,t)}log(e,t){return this.#e(i.$9,e,t)}start(){return this.#e(i.d3)}finished(e){return this.#e(i.BL,e)}recordReplay(){return this.#e(i.CH)}pauseReplay(){return this.#e(i.Tb)}addToTrace(e){return this.#e(i.U2,e)}setCurrentRouteName(e){return this.#e(i.PA,e)}interaction(e){return this.#e(i.dT,e)}wrapLogger(e,t,r){return this.#e(i.Wb,e,t,r)}measure(e,t){return this.#e(i.V1,e,t)}}},773:(e,t,r)=>{"use strict";r.d(t,{z_:()=>a,XG:()=>s,TZ:()=>n,rs:()=>i,xV:()=>o});r(154),r(566),r(384);const n=r(860).K7.metrics,i="sm",a="cm",o="storeSupportabilityMetrics",s="storeEventMetrics"},782:(e,t,r)=>{"use strict";r.d(t,{T:()=>n});const n=r(860).K7.pageViewTiming},836:(e,t,r)=>{"use strict";r.d(t,{P:()=>s,ee:()=>c});var n=r(384),i=r(990),a=r(646),o=r(607);const s="nr@context:".concat(o.W),c=function e(t,r){var n={},o={},u={},l=!1;try{l=16===r.length&&d.initializedAgents?.[r]?.runtime.isolatedBacklog}catch(e){}var f={on:p,addEventListener:p,removeEventListener:function(e,t){var r=n[e];if(!r)return;for(var i=0;i<r.length;i++)r[i]===t&&r.splice(i,1)},emit:function(e,r,n,i,a){!1!==a&&(a=!0);if(c.aborted&&!i)return;t&&a&&t.emit(e,r,n);var s=g(n);m(e).forEach(e=>{e.apply(s,r)});var d=v()[o[e]];d&&d.push([f,e,r,s]);return s},get:h,listeners:m,context:g,buffer:function(e,t){const r=v();if(t=t||"feature",f.aborted)return;Object.entries(e||{}).forEach(([e,n])=>{o[n]=t,t in r||(r[t]=[])})},abort:function(){f._aborted=!0,Object.keys(f.backlog).forEach(e=>{delete f.backlog[e]})},isBuffering:function(e){return!!v()[o[e]]},debugId:r,backlog:l?{}:t&&"object"==typeof t.backlog?t.backlog:{},isolatedBacklog:l};return Object.defineProperty(f,"aborted",{get:()=>{let e=f._aborted||!1;return e||(t&&(e=t.aborted),e)}}),f;function g(e){return e&&e instanceof a.y?e:e?(0,i.I)(e,s,()=>new a.y(s)):new a.y(s)}function p(e,t){n[e]=m(e).concat(t)}function m(e){return n[e]||[]}function h(t){return u[t]=u[t]||e(f,t)}function v(){return f.backlog}}(void 0,"globalEE"),d=(0,n.Zm)();d.ee||(d.ee=c)},843:(e,t,r)=>{"use strict";r.d(t,{u:()=>i});var n=r(878);function i(e,t=!1,r,i){(0,n.DD)("visibilitychange",function(){if(t)return void("hidden"===document.visibilityState&&e());e(document.visibilityState)},r,i)}},860:(e,t,r)=>{"use strict";r.d(t,{$J:()=>u,K7:()=>c,P3:()=>d,XX:()=>i,Yy:()=>s,df:()=>a,qY:()=>n,v4:()=>o});const n="events",i="jserrors",a="browser/blobs",o="rum",s="browser/logs",c={ajax:"ajax",genericEvents:"generic_events",jserrors:i,logging:"logging",metrics:"metrics",pageAction:"page_action",pageViewEvent:"page_view_event",pageViewTiming:"page_view_timing",sessionReplay:"session_replay",sessionTrace:"session_trace",softNav:"soft_navigations",spa:"spa"},d={[c.pageViewEvent]:1,[c.pageViewTiming]:2,[c.metrics]:3,[c.jserrors]:4,[c.spa]:5,[c.ajax]:6,[c.sessionTrace]:7,[c.softNav]:8,[c.sessionReplay]:9,[c.logging]:10,[c.genericEvents]:11},u={[c.pageViewEvent]:o,[c.pageViewTiming]:n,[c.ajax]:n,[c.spa]:n,[c.softNav]:n,[c.metrics]:i,[c.jserrors]:i,[c.sessionTrace]:a,[c.sessionReplay]:a,[c.logging]:s,[c.genericEvents]:"ins"}},863:(e,t,r)=>{"use strict";function n(){return Math.floor(performance.now())}r.d(t,{t:()=>n})},878:(e,t,r)=>{"use strict";function n(e,t){return{capture:e,passive:!1,signal:t}}function i(e,t,r=!1,i){window.addEventListener(e,t,n(r,i))}function a(e,t,r=!1,i){document.addEventListener(e,t,n(r,i))}r.d(t,{DD:()=>a,jT:()=>n,sp:()=>i})},908:(e,t,r)=>{"use strict";r.d(t,{d:()=>n,p:()=>i});var n=r(836).ee.get("handle");function i(e,t,r,i,a){a?(a.buffer([e],i),a.emit(e,t,r)):(n.buffer([e],i),n.emit(e,t,r))}},910:(e,t,r)=>{"use strict";r.d(t,{i:()=>a});var n=r(944);const i=new Map;function a(...e){return e.every(e=>{if(i.has(e))return i.get(e);const t="function"==typeof e&&e.toString().includes("[native code]");return t||(0,n.R)(64,e?.name||e?.toString()),i.set(e,t),t})}},944:(e,t,r)=>{"use strict";r.d(t,{R:()=>i});var n=r(241);function i(e,t){"function"==typeof console.debug&&(console.debug("New Relic Warning: https://github.com/newrelic/newrelic-browser-agent/blob/main/docs/warning-codes.md#".concat(e),t),(0,n.W)({agentIdentifier:null,drained:null,type:"data",name:"warn",feature:"warn",data:{code:e,secondary:t}}))}},990:(e,t,r)=>{"use strict";r.d(t,{I:()=>i});var n=Object.prototype.hasOwnProperty;function i(e,t,r){if(n.call(e,t))return e[t];var i=r();if(Object.defineProperty&&Object.keys)try{return Object.defineProperty(e,t,{value:i,writable:!0,enumerable:!1}),i}catch(e){}return e[t]=i,i}}},n={};function i(e){var t=n[e];if(void 0!==t)return t.exports;var a=n[e]={exports:{}};return r[e](a,a.exports,i),a.exports}i.m=r,i.d=(e,t)=>{for(var r in t)i.o(t,r)&&!i.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},i.f={},i.e=e=>Promise.all(Object.keys(i.f).reduce((t,r)=>(i.f[r](e,t),t),[])),i.u=e=>"nr-rum-1.302.0.min.js",i.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="NRBA-1.302.0.PROD:",i.l=(r,n,a,o)=>{if(e[r])e[r].push(n);else{var s,c;if(void 0!==a)for(var d=document.getElementsByTagName("script"),u=0;u<d.length;u++){var l=d[u];if(l.getAttribute("src")==r||l.getAttribute("data-webpack")==t+a){s=l;break}}if(!s){c=!0;var f={296:"sha512-wOb3n9Oo7XFlPj8/eeDjhAZxpAcaDdsBkC//L8axozi0po4wdPEJ2ECVlu9KEBVFgfQVL0TCY6kPzr0KcVfkBQ=="};(s=document.createElement("script")).charset="utf-8",i.nc&&s.setAttribute("nonce",i.nc),s.setAttribute("data-webpack",t+a),s.src=r,0!==s.src.indexOf(window.location.origin+"/")&&(s.crossOrigin="anonymous"),f[o]&&(s.integrity=f[o])}e[r]=[n];var g=(t,n)=>{s.onerror=s.onload=null,clearTimeout(p);var i=e[r];if(delete e[r],s.parentNode&&s.parentNode.removeChild(s),i&&i.forEach(e=>e(n)),t)return t(n)},p=setTimeout(g.bind(null,void 0,{type:"timeout",target:s}),12e4);s.onerror=g.bind(null,s.onerror),s.onload=g.bind(null,s.onload),c&&document.head.appendChild(s)}},i.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.p="https://js-agent.newrelic.com/",(()=>{var e={374:0,840:0};i.f.j=(t,r)=>{var n=i.o(e,t)?e[t]:void 0;if(0!==n)if(n)r.push(n[2]);else{var a=new Promise((r,i)=>n=e[t]=[r,i]);r.push(n[2]=a);var o=i.p+i.u(t),s=new Error;i.l(o,r=>{if(i.o(e,t)&&(0!==(n=e[t])&&(e[t]=void 0),n)){var a=r&&("load"===r.type?"missing":r.type),o=r&&r.target&&r.target.src;s.message="Loading chunk "+t+" failed.\\n("+a+": "+o+")",s.name="ChunkLoadError",s.type=a,s.request=o,n[1](s)}},"chunk-"+t,t)}};var t=(t,r)=>{var n,a,[o,s,c]=r,d=0;if(o.some(t=>0!==e[t])){for(n in s)i.o(s,n)&&(i.m[n]=s[n]);if(c)c(i)}for(t&&t(r);d<o.length;d++)a=o[d],i.o(e,a)&&e[a]&&e[a][0](),e[a]=0},r=self["webpackChunk:NRBA-1.302.0.PROD"]=self["webpackChunk:NRBA-1.302.0.PROD"]||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})(),(()=>{"use strict";i(374);var e=i(566),t=i(741);class r extends t.W{agentIdentifier=(0,e.LA)(16)}var n=i(860);const a=Object.values(n.K7);var o=i(163);var s=i(908),c=i(863),d=i(261),u=i(241),l=i(944),f=i(701),g=i(773);function p(e,t,i,a){const o=a||i;!o||o[e]&&o[e]!==r.prototype[e]||(o[e]=function(){(0,s.p)(g.xV,["API/"+e+"/called"],void 0,n.K7.metrics,i.ee),(0,u.W)({agentIdentifier:i.agentIdentifier,drained:!!f.B?.[i.agentIdentifier],type:"data",name:"api",feature:d.Pl+e,data:{}});try{return t.apply(this,arguments)}catch(e){(0,l.R)(23,e)}})}function m(e,t,r,n,i){const a=e.info;null===r?delete a.jsAttributes[t]:a.jsAttributes[t]=r,(i||null===r)&&(0,s.p)(d.Pl+n,[(0,c.t)(),t,r],void 0,"session",e.ee)}var h=i(687),v=i(234),b=i(289),y=i(154),_=i(384);const w=e=>y.RI&&!0===e?.privacy.cookies_enabled;function x(e){return!!(0,_.dV)().o.MO&&w(e)&&!0===e?.session_trace.enabled}var k=i(389),S=i(699);class A extends v.W{constructor(e,t){super(e.agentIdentifier,t),this.agentRef=e,this.abortHandler=void 0,this.featAggregate=void 0,this.onAggregateImported=void 0,this.deferred=Promise.resolve(),!1===e.init[this.featureName].autoStart?this.deferred=new Promise((t,r)=>{this.ee.on("manual-start-all",(0,k.J)(()=>{(0,h.Ak)(e.agentIdentifier,this.featureName),t()}))}):(0,h.Ak)(e.agentIdentifier,t)}importAggregator(e,t,r={}){if(this.featAggregate)return;let n;this.onAggregateImported=new Promise(e=>{n=e});const a=async()=>{let a;await this.deferred;try{if(w(e.init)){const{setupAgentSession:t}=await i.e(296).then(i.bind(i,305));a=t(e)}}catch(e){(0,l.R)(20,e),this.ee.emit("internal-error",[e]),(0,s.p)(S.qh,[e],void 0,this.featureName,this.ee)}try{if(!this.#t(this.featureName,a,e.init))return(0,h.Ze)(this.agentIdentifier,this.featureName),void n(!1);const{Aggregate:i}=await t();this.featAggregate=new i(e,r),e.runtime.harvester.initializedAggregates.push(this.featAggregate),n(!0)}catch(e){(0,l.R)(34,e),this.abortHandler?.(),(0,h.Ze)(this.agentIdentifier,this.featureName,!0),n(!1),this.ee&&this.ee.abort()}};y.RI?(0,b.GG)(()=>a(),!0):a()}#t(e,t,r){if(this.blocked)return!1;switch(e){case n.K7.sessionReplay:return x(r)&&!!t;case n.K7.sessionTrace:return!!t;default:return!0}}}var R=i(630),T=i(614);class E extends A{static featureName=R.T;constructor(e){var t;super(e,R.T),this.setupInspectionEvents(e.agentIdentifier),t=e,p(d.Fw,function(e,r){"string"==typeof e&&("/"!==e.charAt(0)&&(e="/"+e),t.runtime.customTransaction=(r||"http://custom.transaction")+e,(0,s.p)(d.Pl+d.Fw,[(0,c.t)()],void 0,void 0,t.ee))},t),this.ee.on("api-send-rum",(e,t)=>(0,s.p)("send-rum",[e,t],void 0,this.featureName,this.ee)),this.importAggregator(e,()=>i.e(296).then(i.bind(i,108)))}setupInspectionEvents(e){const t=(t,r)=>{t&&(0,u.W)({agentIdentifier:e,timeStamp:t.timeStamp,loaded:"complete"===t.target.readyState,type:"window",name:r,data:t.target.location+""})};(0,b.sB)(e=>{t(e,"DOMContentLoaded")}),(0,b.GG)(e=>{t(e,"load")}),(0,b.Qr)(e=>{t(e,"navigate")}),this.ee.on(T.tS.UPDATE,(t,r)=>{(0,u.W)({agentIdentifier:e,type:"lifecycle",name:"session",data:r})})}}var N=i(843),j=i(878),I=i(782);class O extends A{static featureName=I.T;constructor(e){super(e,I.T),y.RI&&((0,N.u)(()=>(0,s.p)("docHidden",[(0,c.t)()],void 0,I.T,this.ee),!0),(0,j.sp)("pagehide",()=>(0,s.p)("winPagehide",[(0,c.t)()],void 0,I.T,this.ee)),this.importAggregator(e,()=>i.e(296).then(i.bind(i,350))))}}class P extends A{static featureName=g.TZ;constructor(e){super(e,g.TZ),y.RI&&document.addEventListener("securitypolicyviolation",e=>{(0,s.p)(g.xV,["Generic/CSPViolation/Detected"],void 0,this.featureName,this.ee)}),this.importAggregator(e,()=>i.e(296).then(i.bind(i,623)))}}new class extends r{constructor(e){var t;(super(),y.gm)?(this.features={},(0,_.bQ)(this.agentIdentifier,this),this.desiredFeatures=new Set(e.features||[]),this.desiredFeatures.add(E),this.runSoftNavOverSpa=[...this.desiredFeatures].some(e=>e.featureName===n.K7.softNav),(0,o.j)(this,e,e.loaderType||"agent"),t=this,p(d.cD,function(e,r,n=!1){if("string"==typeof e){if(["string","number","boolean"].includes(typeof r)||null===r)return m(t,e,r,d.cD,n);(0,l.R)(40,typeof r)}else(0,l.R)(39,typeof e)},t),function(e){p(d.Dl,function(t){if("string"==typeof t||null===t)return m(e,"enduser.id",t,d.Dl,!0);(0,l.R)(41,typeof t)},e)}(this),function(e){p(d.nb,function(t){if("string"==typeof t||null===t)return m(e,"application.version",t,d.nb,!1);(0,l.R)(42,typeof t)},e)}(this),function(e){p(d.d3,function(){e.ee.emit("manual-start-all")},e)}(this),this.run()):(0,l.R)(21)}get config(){return{info:this.info,init:this.init,loader_config:this.loader_config,runtime:this.runtime}}get api(){return this}run(){try{const e=function(e){const t={};return a.forEach(r=>{t[r]=!!e[r]?.enabled}),t}(this.init),t=[...this.desiredFeatures];t.sort((e,t)=>n.P3[e.featureName]-n.P3[t.featureName]),t.forEach(t=>{if(!e[t.featureName]&&t.featureName!==n.K7.pageViewEvent)return;if(this.runSoftNavOverSpa&&t.featureName===n.K7.spa)return;if(!this.runSoftNavOverSpa&&t.featureName===n.K7.softNav)return;const r=function(e){switch(e){case n.K7.ajax:return[n.K7.jserrors];case n.K7.sessionTrace:return[n.K7.ajax,n.K7.pageViewEvent];case n.K7.sessionReplay:return[n.K7.sessionTrace];case n.K7.pageViewTiming:return[n.K7.pageViewEvent];default:return[]}}(t.featureName).filter(e=>!(e in this.features));r.length>0&&(0,l.R)(36,{targetFeature:t.featureName,missingDependencies:r}),this.features[t.featureName]=new t(this)})}catch(e){(0,l.R)(22,e);for(const e in this.features)this.features[e].abortHandler?.();const t=(0,_.Zm)();delete t.initializedAgents[this.agentIdentifier]?.features,delete this.sharedAggregator;return t.ee.get(this.agentIdentifier).abort(),!1}}}({features:[E,O,P],loaderType:"lite"})})()})();
#     </script>
#     \n
#     <meta
#       name="viewport"
#       content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=0"
#     />
#     \n
#     <meta name="keywords" />
#     \n \n
#     <!-- Optanon 2.0.0 Update - Paramount CMP -->
#     \n
#     <script>
#       \n    !function () {\n        window.semaphore = window.semaphore || [],\n            window.ketch = function () { window.semaphore.push(arguments) }; var e = document.createElement("script"); e.type = "text/javascript",\n                e.src = "https://global.ketchcdn.com/web/v3/config/10_play/web_10play/boot.js",\n                e.defer = e.async = !0, document.getElementsByTagName("head")[0].appendChild(e)\n    }();\n
#     </script>
#     \n\n
#     <!-- Optanon 2.0.0 Update - Optanon Standardized API for Paramount CMP -->
#     \n
#     <script>
#       \n    (function (a) {\n        var w = window, b = \'cbsoptanon\', q = \'cmd\', r = \'config\';\n        w[b] = w[b] ? w[b] : {};\n        w[b][q] = w[b][q] ? w[b][q] : [];\n        w[b][r] = w[b][r] ? w[b][r] : [];\n\n        a.forEach(function (z) {\n            w[b][z] = w[b][z] || function () {\n                var c = arguments;\n                w[b][q].push(function () {\n                    w[b][z].apply(w[b], c);\n                })\n            }\n        });\n    })(["onScriptsReady", "onAdsReady"]);   \n
#     </script>
#     \n\n
#     <script
#       src="https://cdn.privacy.paramount.com/dist/optanon-v2.0.0.js"
#       async
#     ></script>
#     \n\n
#     <script>
#       \n    var googletag = googletag || {};\n    googletag.cmd = googletag.cmd || [];\n
#     </script>
#     \n\n
#     <!-- OneTrust CMP -->
#     \n
#     <script
#       src="https://cdn.cookielaw.org/scripttemplates/otSDKStub.js"
#       type="text/javascript"
#       charset="UTF-8"
#       \n
#       data-domain-script="62537caf-23b2-4fde-9162-4ee4b05ebda7"
#     ></script>
#     \n\n
#     <!-- optanon - standardized api for OneTrust -->
#     \n
#     <script
#       src="//cdn.privacy.paramount.com/dist/optanon-v2.0.0.js"
#       type="text/javascript"
#       async
#     ></script>
#     \n\n
#     <script type="text/javascript">
#       \n    var StatusReadyValidator = function () { };\n    StatusReadyValidator.prototype.status = {\n        ads: {\n            multiRun: false,\n            status: {\n                cmp: false,\n                adhesion: false,\n                adManager: false,\n            },\n            callback: [],\n        }\n    };\n    StatusReadyValidator.prototype.statusRegister = function (cat, sec, bool, multiRun) {\n        var category = this.status[cat];\n        if (typeof category !== "object") {\n            category = this.status[cat] = {\n                status: {},\n                callback: [],\n                multiRun: multiRun,\n            };\n        }\n        category.status[sec] = bool;\n    }\n    StatusReadyValidator.prototype.statusUpdate = function (cat, sec, bool) {\n        var category = this.status[cat];\n        if (typeof category === "object" && [true, false].indexOf(category.status[sec]) > -1) {\n            category.status[sec] = bool;\n            if (this.statusValidate(cat)) {\n                this.runCallback(cat);\n            }\n        }\n    };\n    StatusReadyValidator.prototype.statusValidate = function (cat) {\n        var category = this.status[cat];\n        if (typeof category === "object" && typeof category.status === "object") {\n            var sections = Object.keys(category.status);\n            return sections.map(function (secName) { return category.status[secName] }).filter(function (secValue) { return secValue === false }).length === 0;\n        } else {\n            return false;\n        }\n    }\n    StatusReadyValidator.prototype.registerCallback = function (cat, callback) {\n        var category = this.status[cat];\n        if (typeof category === "object" && Array.isArray(category.callback)) {\n            category.callback.push(callback);\n        }\n    }\n    StatusReadyValidator.prototype.runCallback = function (cat) {\n        var category = this.status[cat];\n        if (typeof category === "object" && Array.isArray(category.callback)) {\n            category.callback.forEach(function (callback) { callback(); })\n            !category.multiRun && category.callback.splice(0);\n        }\n    }\n    window.statusReadyValidator = new StatusReadyValidator();\n
#     </script>
#     \n\n
#     <!-- optanon api bootstrap -->
#     \n
#     <script type="text/javascript">
#       \n    !function (n) { var o = window, a = "cbsoptanon", c = "cmd", d = "config"; o[a] = o[a] ? o[a] : {}, o[a][c] = o[a][c] ? o[a][c] : [], o[a][d] = o[a][d] ? o[a][d] : [], ["onIframesReady", "onFormsReady", "onScriptsReady", "onAdsReady"].forEach(function (n) { o[a][n] = o[a][n] || function () { var d = arguments; o[a][c].push(function () { o[a][n].apply(o[a], d) }) } }) }();\n\n    window.cbsoptanon.config.push({\n        enableServices: false,\n        setNpaOnConsentChange: true\n    });\n\n    window.cbsoptanon.onAdsReady((_cbsoptanon, adOpts) => {\n        window.statusReadyValidator.statusUpdate("ads", "cmp", true);\n    });\n\n    window.statusReadyValidator.registerCallback("ads", function () {\n        googletag.cmd.push(function () {\n            googletag.enableServices();\n            TenPlay.Page.renderAdSlots();\n        });\n    })\n
#     </script>
#     \n
#     <link rel="icon" href="/images/favicon.png" type="image/x-icon" />
#     \n
#     <script
#       async=""
#       type="text/javascript"
#       src="//securepubads.g.doubleclick.net/tag/js/gpt.js"
#     ></script>
#     \n
#     <script
#       async=""
#       type="text/javascript"
#       src="//secure-dcr.imrworldwide.com/novms/js/2/ggcmb510.js"
#     ></script>
#     \n
#     <link
#       rel="stylesheet"
#       charset="UTF-8"
#       href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick.min.css"
#     />
#     \n
#     <link
#       rel="stylesheet"
#       href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick-theme.min.css"
#     />
#     \n\n \n \n
#     <link rel="stylesheet" href="/css/main.css?buildId=1761261624" />
#     \n
#     <link rel="canonical" href="https://10.com.au/shows/movies" />
#     \n\n
#     <meta name="description" content="Browse Movies Shows on 10" />
#     \n
#     <script>
#       var apiUrl = "https://10.com.au";
#     </script>
#     \n
#     <script
#       async
#       src="//platform.twitter.com/widgets.js"
#       charset="utf-8"
#     ></script>
#     \n
#     <script
#       async
#       src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&amp;version=v2.5"
#     ></script>
#     \n
#     <script
#       async=""
#       defer=""
#       src="//platform.instagram.com/en_US/embeds.js"
#     ></script>
#     \n \n
#     <!-- Start of Tealium utag.sync.js script --->
#     <script src="//tags.tiqcdn.com/utag/10/10playsite/prod/utag.sync.js"></script>
#     <!-- End of Tealium utag.sync.js script --->
#     \n
#     <script>
#       \n            var TealiumData = {"siteDomain":"https://10.com.au","siteName":"10","pageContentName":"Shows for Movies","siteSubSection1":"shows","siteSubSection2":"movies","tealium_event":"shows_view","siteSection":"Shows","pageContentFilter":["Movies"]};\n
#     </script>
#     \n\n
#     <script type="text/javascript" src="/static/ads.js"></script>
#     \n
#     <script
#       type="text/javascript"
#       src="/js/GlobalHeader.compiled.js?buildId=1761261624"
#       hot-reload
#     ></script>
#     \n</head
#   >\n
#   <body class="defaultpage" style="--theme-color: #0047f4">
#     \n\n
#     <script type="text/javascript">
#       (function(a,b,c,d){a=\'//tags.tiqcdn.com/utag/10/10playsite/prod/utag.js\';b=document;c=\'script\';d=b.createElement(c);d.src=a;d.type=\'text/java\'+c;d.async=true;a=b.getElementsByTagName(c)[0];a.parentNode.insertBefore(d,a);})();
#     </script>
#     \n\n\n \n \n
#     <div id="nav">
#       <header
#         class="global-header global-header--default-page global-header--fixed"
#       >
#         <div class="container d-flex">
#           <h1 class="global-header__logo">
#             <a
#               href="/"
#               class="global-header__logo-link"
#               aria-label="Return to homepage"
#               ><div class="logo"></div
#             ></a>
#           </h1>
#           <button
#             role="button"
#             aria-label="Mobile Menu Button"
#             class="menu__hamburger"
#           ></button>
#           <div class="global-header__primary">
#             <ul
#               class="global-header__navigation"
#               role="navigation"
#               aria-label="Main Navigation"
#             >
#               <li>
#                 <a class="hide-desktop" href="/shows">Shows</a
#                 ><button class="megamenu__toggle hide-tablet">
#                   Shows <span class="icon-angle-down"></span>
#                 </button>
#                 <div class="megamenu">
#                   <ul class="megamenu__quicklinks">
#                     <li><a href="/news">10 News</a></li>
#                     <li><a href="/sport">10 Sport</a></li>
#                     <li><a href="/10-trending">10 Trending</a></li>
#                   </ul>
#                   <div class="megamenu__menus">
#                     <div class="close-container">
#                       <button class="close-x close-x--light"></button>
#                     </div>
#                     <div class="container">
#                       <div class="row">
#                         <div
#                           class="megamenu__menu--white megamenu__menu--bordered col-sm-12 col-md-5"
#                           data-tp="MjQ2OTMx"
#                         >
#                           <div class="megamenu__menu">
#                             <h3 class="megamenu__heading--text">
#                               Catch Up On...
#                             </h3>
#                             <ul>
#                               <li>
#                                 <a
#                                   href="/the-amazing-race-australia"
#                                   class="megamenu__shows"
#                                   style="
#                                     background-image: url(https://10.com.au/ip/s3/2025/08/25/1438c361fa49fedc5e5d397394dc443d-1391354.jpg?image-profile=image_small&amp;io=landscape);
#                                   "
#                                   >The Amazing Race Australia<small
#                                     >The Amazing Race Australia</small
#                                   ><span class="megamenu__shows-category"></span
#                                 ></a>
#                               </li>
#                               <li>
#                                 <a
#                                   href="/the-celebrity-traitors-uk"
#                                   class="megamenu__shows"
#                                   style="
#                                     background-image: url(https://10.com.au/ip/s3/2025/10/02/d2578510c918df9b409cc93d53561f0e-1396010.jpg?image-profile=image_small&amp;io=landscape);
#                                   "
#                                   >The Celebrity Traitors UK<small
#                                     >The Celebrity Traitors UK</small
#                                   ><span class="megamenu__shows-category"></span
#                                 ></a>
#                               </li>
#                               <li>
#                                 <a
#                                   href="/talkin-bout-your-generation"
#                                   class="megamenu__shows"
#                                   style="
#                                     background-image: url(https://10.com.au/ip/s3/2025/08/27/c5cb0493d5fe7cdbcbddcc4bd31092e2-1391860.jpg?image-profile=image_small&amp;io=landscape);
#                                   "
#                                   >Talkin&#x27; &#x27;Bout Your Generation<small
#                                     >Talkin&#x27; &#x27;Bout Your
#                                     Generation</small
#                                   ><span class="megamenu__shows-category"></span
#                                 ></a>
#                               </li>
#                             </ul>
#                           </div>
#                         </div>
#                         <div class="megamenu__menu--grey col-sm-12 col-md-7">
#                           <div class="row">
#                             <div
#                               class="megamenu__menu col-sm-6"
#                               data-tp="MjQ2OTMz"
#                             >
#                               <h3 class="megamenu__heading--text">
#                                 Featured TV Shows
#                               </h3>
#                               <ul>
#                                 <li>
#                                   <a href="/the-amazing-race-australia"
#                                     >The Amazing Race Australia</a
#                                   >
#                                 </li>
#                                 <li>
#                                   <a href="/australian-survivor"
#                                     >Australian Survivor</a
#                                   >
#                                 </li>
#                                 <li><a href="/broadchurch">Broadchurch</a></li>
#                                 <li>
#                                   <a href="/the-celebrity-traitors-uk"
#                                     >The Celebrity Traitors UK</a
#                                   >
#                                 </li>
#                                 <li>
#                                   <a href="/the-cheap-seats">The Cheap Seats</a>
#                                 </li>
#                                 <li>
#                                   <a href="/the-gilded-age">The Gilded Age</a>
#                                 </li>
#                                 <li><a href="/gogglebox">Gogglebox</a></li>
#                                 <li>
#                                   <a href="/sam-pang-tonight"
#                                     >Sam Pang Tonight</a
#                                   >
#                                 </li>
#                                 <li>
#                                   <a href="/the-office-australia"
#                                     >The Office Australia</a
#                                   >
#                                 </li>
#                                 <li>
#                                   <a href="/talkin-bout-your-generation"
#                                     >Talkin&#x27; &#x27;Bout Your Generation</a
#                                   >
#                                 </li>
#                               </ul>
#                             </div>
#                             <div class="megamenu__menu col-sm-6">
#                               <h3 class="megamenu__heading--text">
#                                 Shows By Genre
#                               </h3>
#                               <ul>
#                                 <li>
#                                   <a href="/shows/adventure">Adventure</a>
#                                 </li>
#                                 <li><a href="/shows/comedy">Comedy</a></li>
#                                 <li><a href="/shows/crime">Crime</a></li>
#                                 <li>
#                                   <a href="/shows/documentary">Documentary</a>
#                                 </li>
#                                 <li><a href="/shows/drama">Drama</a></li>
#                                 <li><a href="/shows/kids">Kids</a></li>
#                                 <li>
#                                   <a href="/shows/lifestyle">Lifestyle</a>
#                                 </li>
#                                 <li>
#                                   <a href="/shows/light-entertainment"
#                                     >Light Entertainment</a
#                                   >
#                                 </li>
#                                 <li><a href="/shows/movie">Movies</a></li>
#                                 <li><a href="/shows/news">News</a></li>
#                                 <li><a href="/shows/reality">Reality</a></li>
#                                 <li>
#                                   <a href="/shows/religious">Religious</a>
#                                 </li>
#                                 <li><a href="/shows/sport">Sport</a></li>
#                                 <li>
#                                   <a
#                                     href="/shows"
#                                     class="megamenu__more"
#                                     style="color: #0047f4"
#                                     >View All Shows<i
#                                       class="icon-arrow-right"
#                                     ></i
#                                   ></a>
#                                 </li>
#                               </ul>
#                             </div>
#                           </div>
#                         </div>
#                       </div>
#                     </div>
#                   </div>
#                   <div class="megamenu__search">
#                     <div class="search-form">
#                       <form action="/search?field">
#                         <input
#                           type="text"
#                           value=""
#                           placeholder="Search for shows, people, recipes"
#                           class="search-form__input"
#                         /><button
#                           class="search-form__button"
#                           aria-label="Search"
#                           type="submit"
#                         >
#                           <i class="search-form__icon icon-search"></i>
#                         </button>
#                       </form>
#                     </div>
#                   </div>
#                   <div class="megamenu__backdrop"></div>
#                 </div>
#               </li>
#               <li>
#                 <a class="hide-desktop" href="/live">Live TV</a
#                 ><button class="megamenu__toggle hide-tablet">
#                   Live TV <span class="icon-angle-down"></span>
#                 </button>
#                 <div id="hide-tablet" class="megamenu megamenu-dark">
#                   <div class="megamenu-darkbackground">
#                     <div class="megamenu__menus">
#                       <div class="close-container">
#                         <button class="close-x close-x--light"></button>
#                       </div>
#                       <div class="container">
#                         <div class="row">
#                           <div class="col-sm-12 col-md-4 dark-gradient-right">
#                             <div class="row flex-column">
#                               <h3 class="megamenu__heading--text">On-Air</h3>
#                               <div class="channelItems">
#                                 <div
#                                   class="card card--liveRightNow channel-ten"
#                                   style="--channelColour: #1882f8"
#                                 >
#                                   <a href="https://10.com.au/live/ten"
#                                     ><div class="card__wrapper">
#                                       <div
#                                         class="card__image--channel--container d-flex"
#                                       >
#                                         <figure
#                                           class="card__image card__image--channel d-flex"
#                                         >
#                                           <img
#                                             src="https://10.com.au/ip/s3/2025/06/25/b18ae76555d114f7bfaf1c3bfa43dd3f-1384577.png"
#                                             alt="10 Logo"
#                                           />
#                                         </figure>
#                                       </div>
#                                       <div
#                                         class="liveRightNow__container d-flex"
#                                       >
#                                         <section class="card__content">
#                                           <div class="card__container">
#                                             <div class="card__titlewrapper">
#                                               <h4
#                                                 class="card__title card__maxwidth"
#                                               >
#                                                 NBL
#                                               </h4>
#                                             </div>
#                                             <h5 class="card__info"></h5>
#                                             <div class="progressbar">
#                                               <span
#                                                 class="progressbar--progress ten"
#                                                 style="width: 0%"
#                                               ></span>
#                                             </div>
#                                           </div>
#                                         </section>
#                                       </div></div
#                                   ></a>
#                                 </div>
#                                 <div
#                                   class="card card--liveRightNow channel-tenbold"
#                                   style="--channelColour: #e6103c"
#                                 >
#                                   <a href="https://10.com.au/live/drama"
#                                     ><div class="card__wrapper">
#                                       <div
#                                         class="card__image--channel--container d-flex"
#                                       >
#                                         <figure
#                                           class="card__image card__image--channel d-flex"
#                                         >
#                                           <img
#                                             src="https://10.com.au/ip/s3/2025/06/25/66c9f2639a7bca4a6691764a0db801d7-1384581.png"
#                                             alt="10 Drama Logo"
#                                           />
#                                         </figure>
#                                       </div>
#                                       <div
#                                         class="liveRightNow__container d-flex"
#                                       >
#                                         <section class="card__content">
#                                           <div class="card__container">
#                                             <div class="card__titlewrapper">
#                                               <h4
#                                                 class="card__title card__maxwidth"
#                                               >
#                                                 JAG
#                                               </h4>
#                                             </div>
#                                             <h5 class="card__info">
#                                               <span class="show-rating-spacer"
#                                                 >|</span
#                                               >PG
#                                             </h5>
#                                             <div class="progressbar">
#                                               <span
#                                                 class="progressbar--progress tenbold"
#                                                 style="width: 0%"
#                                               ></span>
#                                             </div>
#                                           </div>
#                                         </section>
#                                       </div></div
#                                   ></a>
#                                 </div>
#                                 <div
#                                   class="card card--liveRightNow channel-tenpeach"
#                                   style="--channelColour: #ba0df9"
#                                 >
#                                   <a href="https://10.com.au/live/comedy"
#                                     ><div class="card__wrapper">
#                                       <div
#                                         class="card__image--channel--container d-flex"
#                                       >
#                                         <figure
#                                           class="card__image card__image--channel d-flex"
#                                         >
#                                           <img
#                                             src="https://10.com.au/ip/s3/2025/06/25/443fa2a5bca1191f12efa002a2a8ef85-1384586.png"
#                                             alt="10 Comedy Logo"
#                                           />
#                                         </figure>
#                                       </div>
#                                       <div
#                                         class="liveRightNow__container d-flex"
#                                       >
#                                         <section class="card__content">
#                                           <div class="card__container">
#                                             <div class="card__titlewrapper">
#                                               <h4
#                                                 class="card__title card__maxwidth"
#                                               >
#                                                 Ridiculousness
#                                               </h4>
#                                             </div>
#                                             <h5 class="card__info">
#                                               <span class="show-rating-spacer"
#                                                 >|</span
#                                               >PG
#                                             </h5>
#                                             <div class="progressbar">
#                                               <span
#                                                 class="progressbar--progress tenpeach"
#                                                 style="width: 0%"
#                                               ></span>
#                                             </div>
#                                           </div>
#                                         </section>
#                                       </div></div
#                                   ></a>
#                                 </div>
#                                 <div
#                                   class="card card--liveRightNow channel-tenshake"
#                                   style="--channelColour: #f15b22"
#                                 >
#                                   <a href="https://10.com.au/live/nickelodeon"
#                                     ><div class="card__wrapper">
#                                       <div
#                                         class="card__image--channel--container d-flex"
#                                       >
#                                         <figure
#                                           class="card__image card__image--channel d-flex"
#                                         >
#                                           <img
#                                             src="https://10.com.au/ip/s3/2023/07/31/dc4873abc5ba0fde04b59a78c89e0943-1252731.png"
#                                             alt="Nickelodeon Logo"
#                                           />
#                                         </figure>
#                                       </div>
#                                       <div
#                                         class="liveRightNow__container d-flex"
#                                       >
#                                         <section class="card__content">
#                                           <div class="card__container">
#                                             <div class="card__titlewrapper">
#                                               <h4
#                                                 class="card__title card__maxwidth"
#                                               >
#                                                 SpongeBob SquarePants
#                                               </h4>
#                                             </div>
#                                             <h5 class="card__info">
#                                               <span class="show-rating-spacer"
#                                                 >|</span
#                                               >G
#                                             </h5>
#                                             <div class="progressbar">
#                                               <span
#                                                 class="progressbar--progress tenshake"
#                                                 style="width: 0%"
#                                               ></span>
#                                             </div>
#                                           </div>
#                                         </section>
#                                       </div></div
#                                   ></a>
#                                 </div>
#                               </div>
#                             </div>
#                           </div>
#                           <div
#                             class="col-sm-12 col-md-4 dark-gradient-right padding-left-spacer"
#                           >
#                             <div class="row">
#                               <h3 class="megamenu__heading--text">Featured</h3>
#                               <div class="channelItems">
#                                 <div
#                                   class="card card--liveRightNow channel-south-park"
#                                   style="--channelColour: #dc2f34"
#                                 >
#                                   <a href="https://10.com.au/live/south-park"
#                                     ><div class="card__wrapper">
#                                       <div
#                                         class="card__image--channel--container d-flex"
#                                       >
#                                         <figure
#                                           class="card__image card__image--channel d-flex"
#                                         >
#                                           <img
#                                             src="https://10.com.au/ip/s3/2023/08/03/41a79ba6a28f011b379ea68d41c28ea0-1253591.png"
#                                             alt="South Park Logo"
#                                           />
#                                         </figure>
#                                       </div>
#                                       <div
#                                         class="liveRightNow__container d-flex"
#                                       >
#                                         <section class="card__content">
#                                           <div class="card__container">
#                                             <div class="card__titlewrapper">
#                                               <h4
#                                                 class="card__title card__maxwidth"
#                                               >
#                                                 South Park S8 Ep. 8
#                                               </h4>
#                                             </div>
#                                             <h5 class="card__info">
#                                               <span class="show-rating-spacer"
#                                                 >|</span
#                                               >MA15+
#                                             </h5>
#                                             <div class="progressbar">
#                                               <span
#                                                 class="progressbar--progress south-park"
#                                                 style="width: 0%"
#                                               ></span>
#                                             </div>
#                                           </div>
#                                         </section>
#                                       </div></div
#                                   ></a>
#                                 </div>
#                                 <div
#                                   class="card card--liveRightNow channel-becker"
#                                   style="--channelColour: #976ed8"
#                                 >
#                                   <a href="https://10.com.au/live/becker"
#                                     ><div class="card__wrapper">
#                                       <div
#                                         class="card__image--channel--container d-flex"
#                                       >
#                                         <figure
#                                           class="card__image card__image--channel d-flex"
#                                         >
#                                           <img
#                                             src="https://10.com.au/ip/s3/2023/06/28/e0449ed804aaacb1de64f87d94912dd3-1246030.png"
#                                             alt="Becker Logo"
#                                           />
#                                         </figure>
#                                       </div>
#                                       <div
#                                         class="liveRightNow__container d-flex"
#                                       >
#                                         <section class="card__content">
#                                           <div class="card__container">
#                                             <div class="card__titlewrapper">
#                                               <h4
#                                                 class="card__title card__maxwidth"
#                                               >
#                                                 Becker S4 Ep. 15
#                                               </h4>
#                                             </div>
#                                             <h5 class="card__info">
#                                               <span class="show-rating-spacer"
#                                                 >|</span
#                                               >PG
#                                             </h5>
#                                             <div class="progressbar">
#                                               <span
#                                                 class="progressbar--progress becker"
#                                                 style="width: 0%"
#                                               ></span>
#                                             </div>
#                                           </div>
#                                         </section>
#                                       </div></div
#                                   ></a>
#                                 </div>
#                                 <div
#                                   class="card card--liveRightNow channel-forty-eight-hours"
#                                   style="--channelColour: #5f9bfa"
#                                 >
#                                   <a href="https://10.com.au/live/48hours"
#                                     ><div class="card__wrapper">
#                                       <div
#                                         class="card__image--channel--container d-flex"
#                                       >
#                                         <figure
#                                           class="card__image card__image--channel d-flex"
#                                         >
#                                           <img
#                                             src="https://10.com.au/ip/s3/2023/06/28/7dd910de29f31095b69e17f1da8f3f0e-1245997.png"
#                                             alt="48 Hours Logo"
#                                           />
#                                         </figure>
#                                       </div>
#                                       <div
#                                         class="liveRightNow__container d-flex"
#                                       >
#                                         <section class="card__content">
#                                           <div class="card__container">
#                                             <div class="card__titlewrapper">
#                                               <h4
#                                                 class="card__title card__maxwidth"
#                                               >
#                                                 48 Hours S22 Ep. 60
#                                               </h4>
#                                             </div>
#                                             <h5 class="card__info">
#                                               <span class="show-rating-spacer"
#                                                 >|</span
#                                               >M
#                                             </h5>
#                                             <div class="progressbar">
#                                               <span
#                                                 class="progressbar--progress forty-eight-hours"
#                                                 style="width: 0%"
#                                               ></span>
#                                             </div>
#                                           </div>
#                                         </section>
#                                       </div></div
#                                   ></a>
#                                 </div>
#                                 <div
#                                   class="card card--liveRightNow channel-hardcorepawn"
#                                   style="--channelColour: #ca9e04"
#                                 >
#                                   <a href="https://10.com.au/live/hardcore-pawn"
#                                     ><div class="card__wrapper">
#                                       <div
#                                         class="card__image--channel--container d-flex"
#                                       >
#                                         <figure
#                                           class="card__image card__image--channel d-flex"
#                                         >
#                                           <img
#                                             src="https://10.com.au/ip/s3/2025/03/03/1d46b70035ba5c816af46c6d4ee079cd-1366514.png"
#                                             alt="Hardcore Pawn Logo"
#                                           />
#                                         </figure>
#                                       </div>
#                                       <div
#                                         class="liveRightNow__container d-flex"
#                                       >
#                                         <section class="card__content">
#                                           <div class="card__container">
#                                             <div class="card__titlewrapper">
#                                               <h4
#                                                 class="card__title card__maxwidth"
#                                               >
#                                                 Rich vs. Les
#                                               </h4>
#                                             </div>
#                                             <h5 class="card__info">
#                                               <span class="show-rating-spacer"
#                                                 >|</span
#                                               >M
#                                             </h5>
#                                             <div class="progressbar">
#                                               <span
#                                                 class="progressbar--progress hardcorepawn"
#                                                 style="width: 0%"
#                                               ></span>
#                                             </div>
#                                           </div>
#                                         </section>
#                                       </div></div
#                                   ></a>
#                                 </div>
#                               </div>
#                             </div>
#                           </div>
#                           <div class="col-sm-12 col-md-4 padding-left-spacer">
#                             <div class="row">
#                               <h3 class="megamenu__heading--text">
#                                 More Channels
#                               </h3>
#                               <div class="logos--additional">
#                                 <a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/cops"
#                                   style="--channelColour: #0a44ff"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2025/03/30/6fadf0873ac36ecacdc63ed8bba4cf3d-1371071.png"
#                                       alt="COPS"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/mtv-ridiculousness"
#                                   style="--channelColour: #ff0000"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2024/02/19/6a7d740896d031b59c9d33d0e6dff544-1298686.png"
#                                       alt="MTV Ridiculousness"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/diagnosismurder"
#                                   style="--channelColour: #d20001"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2023/06/28/5f85fc3d794a167630b935cb639abcc3-1246005.png"
#                                       alt="Diagnosis Murder"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/world-of-survivor"
#                                   style="--channelColour: #ffa800"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2024/09/24/6a7955dee63fad795d40332b9cfbf8ce-1340644.png"
#                                       alt="World Of Survivor"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/aussie-drama-pop-up"
#                                   style="--channelColour: #91adb7"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2023/01/24/082f00086b990e915cd774644d67484c-1213111.png"
#                                       alt="Rush"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/8-out-of-10-cats"
#                                   style="--channelColour: #f9283e"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2024/11/18/03a9b9a1a42bcf2ce1bbb94a8fa47224-1350731.png"
#                                       alt="8 Out Of 10 Cats"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/spongebob-squarepants"
#                                   style="--channelColour: #4ebecd"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2024/05/27/ee4d9694aa3f7a2fe97b6f18aa773b88-1316803.png"
#                                       alt="SpongeBob SquarePants"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/embarrassing-bodies"
#                                   style="--channelColour: #63c39a"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2024/10/21/f315a8cda9494cc30e29fdba87430ff8-1345391.png"
#                                       alt="Embarrassing Bodies"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/crime-time"
#                                   style="--channelColour: #ff032d"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2024/09/25/c27b803a4128c5b097cd3a23e1be973c-1341004.png"
#                                       alt="Crime Time"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/nicktoons-90s"
#                                   style="--channelColour: #ff6700"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2024/06/07/a1aaf63737e7d2076759dd850b58471a-1319376.png"
#                                       alt="NickToons 90s"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/crime-hunters"
#                                   style="--channelColour: #ff2400"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2024/03/06/cb69de15e7b8989a218ad25b7f6547ef-1301820.png"
#                                       alt="Crime Hunters"
#                                     /></div></a
#                                 ><a
#                                   class="channelLogo--more"
#                                   href="https://10.com.au/live/nick-jr-club"
#                                   style="--channelColour: #ff6700"
#                                   ><div class="channelLogo--container">
#                                     <img
#                                       src="https://10.com.au/ip/s3/2024/06/06/d14509f218578984e3a6f6f34f0ee12c-1319009.png"
#                                       alt="Nick Jr Club"
#                                     /></div
#                                 ></a>
#                               </div>
#                             </div>
#                           </div>
#                         </div>
#                       </div>
#                     </div>
#                     <div class="megamenu__bottom">
#                       <p>
#                         Livestream 24/7 entertainment.
#                         <a href="/live"
#                           >View All Channels <i class="icon-arrow-right"></i
#                         ></a>
#                       </p>
#                     </div>
#                   </div>
#                   <div class="megamenu__backdrop"></div>
#                 </div>
#               </li>
#               <li><a href="/tv-guide">TV Guide</a></li>
#               <li>
#                 <button class="megamenu__toggle undefined">
#                   News &amp; Sport <span class="icon-angle-down"></span>
#                 </button>
#                 <div class="megamenu">
#                   <ul class="megamenu__quicklinks">
#                     <li><a href="/news">News</a></li>
#                     <li><a href="/sport">Sport</a></li>
#                     <li><a href="/10-trending">Trending</a></li>
#                   </ul>
#                   <div class="megamenu__menus">
#                     <div class="close-container">
#                       <button class="close-x close-x--light"></button>
#                     </div>
#                     <div class="container">
#                       <div class="row">
#                         <div
#                           class="megamenu__menu--white megamenu__menu--bordered col-sm-12 col-md-5"
#                         >
#                           <div class="row">
#                             <div class="megamenu__menu col-sm-6">
#                               <h3 class="megamenu__heading--text">10 News</h3>
#                               <ul>
#                                 <li><a href="/news/national">National</a></li>
#                                 <li><a href="/news/sydney">Sydney</a></li>
#                                 <li>
#                                   <a
#                                     href="/news"
#                                     class="megamenu__more"
#                                     style="color: #0047f4"
#                                     >View All News<i
#                                       class="icon-arrow-right"
#                                     ></i
#                                   ></a>
#                                 </li>
#                               </ul>
#                             </div>
#                             <div class="megamenu__menu col-sm-6">
#                               <h3 class="megamenu__heading--text">Sport</h3>
#                               <ul>
#                                 <li><a href="/sport">Sport</a></li>
#                                 <li><a href="/football">Football</a></li>
#                                 <li>
#                                   <a href="/national-basketball-league"
#                                     >National Basketball League</a
#                                   >
#                                 </li>
#                                 <li><a href="/a-league">A-League</a></li>
#                                 <li><a href="/matildas">Matildas</a></li>
#                                 <li>
#                                   <a href="/roshn-saudi-league"
#                                     >Roshn Saudi League</a
#                                   >
#                                 </li>
#                                 <li>
#                                   <a
#                                     href="/sport"
#                                     class="megamenu__more"
#                                     style="color: #0047f4"
#                                     >View All Sports<i
#                                       class="icon-arrow-right"
#                                     ></i
#                                   ></a>
#                                 </li>
#                               </ul>
#                             </div>
#                           </div>
#                         </div>
#                         <div class="megamenu__menu--grey col-sm-12 col-md-7">
#                           <section class="megamenu__menu col-sm-12">
#                             <a
#                               href="/10-trending"
#                               aria-label="Link to trending page"
#                               ><h3 class="megamenu__heading--text">
#                                 Trending
#                               </h3></a
#                             >
#                             <ul class="trending-list">
#                               <li>
#                                 <a
#                                   href="/the-amazing-race-australia/articles/meet-the-13-teams-tackling-the-amazing-race-australia-celebrity-edition-2025/tpa250319kjuoa"
#                                   style="
#                                     background-image: url('https://10.com.au/ip/s3/2025/03/19/02e5b012b4e88494c7a6812960295d8c-1369426.png?image-profile=image_small&amp;io=landscape');
#                                   "
#                                   >Meet The 13 Teams Tackling The Amazing Race
#                                   Australia: Celebrity Edition 2025</a
#                                 >
#                               </li>
#                               <li>
#                                 <a
#                                   href="/masterchef/articles/masterchef-australia-back-to-win-2025-meet-the-full-cast/tpa250312nmpld"
#                                   style="
#                                     background-image: url('https://10.com.au/ip/s3/2025/03/13/5c02c9bda8577e653f94fce13f9c9c8f-1368510.png?image-profile=image_small&amp;io=landscape');
#                                   "
#                                   >MasterChef Australia Back To Win 2025: Meet
#                                   The Full Cast</a
#                                 >
#                               </li>
#                               <li>
#                                 <a
#                                   href="/australian-survivor/articles/australian-survivor-2025-brains-v-brawn-meet-the-full-cast/tpa250115ukfqa"
#                                   style="
#                                     background-image: url('https://10.com.au/ip/s3/2025/01/19/5515bc0ad14d2d8ad018cfa1e7a4cbb3-1359810.png?image-profile=image_small&amp;io=landscape');
#                                   "
#                                   >Australian Survivor 2025: Brains V Brawn -
#                                   Meet The Full Cast</a
#                                 >
#                               </li>
#                               <li>
#                                 <a
#                                   href="/im-a-celebrity-get-me-out-of-here/articles/im-a-celebrity-get-me-out-of-here-2025-meet-the-celebrities/tpa250115choui"
#                                   style="
#                                     background-image: url('https://10.com.au/ip/s3/2025/01/19/731306e1a5f79b797573ec22d263eee2-1359750.png?image-profile=image_small&amp;io=landscape');
#                                   "
#                                   >I\xe2\x80\x99m A Celebrity Get Me Out Of Here
#                                   2025: Meet The Celebrities</a
#                                 >
#                               </li>
#                             </ul>
#                             <a
#                               class="megamenu_more trending"
#                               href="/10-trending"
#                               >View All Trending<i class="icon-arrow-right"></i
#                             ></a>
#                           </section>
#                         </div>
#                       </div>
#                     </div>
#                   </div>
#                   <div class="megamenu__search">
#                     <div class="search-form">
#                       <form action="/search?field">
#                         <input
#                           type="text"
#                           value=""
#                           placeholder="Search for shows, people, recipes"
#                           class="search-form__input"
#                         /><button
#                           class="search-form__button"
#                           aria-label="Search"
#                           type="submit"
#                         >
#                           <i class="search-form__icon icon-search"></i>
#                         </button>
#                       </form>
#                     </div>
#                   </div>
#                   <div class="megamenu__backdrop"></div>
#                 </div>
#               </li>
#               <li><a href="/kids-hub">Kids</a></li>
#               <li><a href="/win">Win</a></li>
#               <li class="global-header__search">
#                 <button role="button" aria-label="Expand search area">
#                   <span class="icon-search"></span>
#                 </button>
#               </li>
#               <div></div>
#             </ul>
#           </div>
#           <div class="global-header__search">
#             <button role="button" aria-label="Expand search overlay">
#               <span class="icon-search"></span>
#             </button>
#           </div>
#         </div>
#       </header>
#     </div>
#     \n\n
#     <script>
#       const headerData = {
#         userName: null,
#         userLoggedIn: false,
#         megaMenu: {
#           showsMenu: {
#             primaryTpId: "MjQ2OTMx",
#             secondaryTpId: "MjQ2OTMz",
#             primaryLinksHeading: "Catch Up On...",
#             primaryLinks: [
#               {
#                 subText: "The Amazing Race Australia",
#                 imageUrl:
#                   "https://10.com.au/ip/s3/2025/08/25/1438c361fa49fedc5e5d397394dc443d-1391354.jpg?image-profile=image_small\\u0026io=landscape",
#                 text: "The Amazing Race Australia",
#                 url: "/the-amazing-race-australia",
#                 external: false,
#               },
#               {
#                 subText: "The Celebrity Traitors UK",
#                 imageUrl:
#                   "https://10.com.au/ip/s3/2025/10/02/d2578510c918df9b409cc93d53561f0e-1396010.jpg?image-profile=image_small\\u0026io=landscape",
#                 text: "The Celebrity Traitors UK",
#                 url: "/the-celebrity-traitors-uk",
#                 external: false,
#               },
#               {
#                 subText: "Talkin\\u0027 \\u0027Bout Your Generation",
#                 imageUrl:
#                   "https://10.com.au/ip/s3/2025/08/27/c5cb0493d5fe7cdbcbddcc4bd31092e2-1391860.jpg?image-profile=image_small\\u0026io=landscape",
#                 text: "Talkin\\u0027 \\u0027Bout Your Generation",
#                 url: "/talkin-bout-your-generation",
#                 external: false,
#               },
#             ],
#             secondaryLinkGroups: [
#               {
#                 heading: "Featured TV Shows",
#                 links: [
#                   {
#                     text: "The Amazing Race Australia",
#                     url: "/the-amazing-race-australia",
#                     external: false,
#                   },
#                   {
#                     text: "Australian Survivor",
#                     url: "/australian-survivor",
#                     external: false,
#                   },
#                   { text: "Broadchurch", url: "/broadchurch", external: false },
#                   {
#                     text: "The Celebrity Traitors UK",
#                     url: "/the-celebrity-traitors-uk",
#                     external: false,
#                   },
#                   {
#                     text: "The Cheap Seats",
#                     url: "/the-cheap-seats",
#                     external: false,
#                   },
#                   {
#                     text: "The Gilded Age",
#                     url: "/the-gilded-age",
#                     external: false,
#                   },
#                   { text: "Gogglebox", url: "/gogglebox", external: false },
#                   {
#                     text: "Sam Pang Tonight",
#                     url: "/sam-pang-tonight",
#                     external: false,
#                   },
#                   {
#                     text: "The Office Australia",
#                     url: "/the-office-australia",
#                     external: false,
#                   },
#                   {
#                     text: "Talkin\\u0027 \\u0027Bout Your Generation",
#                     url: "/talkin-bout-your-generation",
#                     external: false,
#                   },
#                 ],
#               },
#               {
#                 heading: "Shows By Genre",
#                 links: [
#                   {
#                     text: "Adventure",
#                     url: "/shows/adventure",
#                     external: false,
#                   },
#                   { text: "Comedy", url: "/shows/comedy", external: false },
#                   { text: "Crime", url: "/shows/crime", external: false },
#                   {
#                     text: "Documentary",
#                     url: "/shows/documentary",
#                     external: false,
#                   },
#                   { text: "Drama", url: "/shows/drama", external: false },
#                   { text: "Kids", url: "/shows/kids", external: false },
#                   {
#                     text: "Lifestyle",
#                     url: "/shows/lifestyle",
#                     external: false,
#                   },
#                   {
#                     text: "Light Entertainment",
#                     url: "/shows/light-entertainment",
#                     external: false,
#                   },
#                   { text: "Movies", url: "/shows/movie", external: false },
#                   { text: "News", url: "/shows/news", external: false },
#                   { text: "Reality", url: "/shows/reality", external: false },
#                   {
#                     text: "Religious",
#                     url: "/shows/religious",
#                     external: false,
#                   },
#                   { text: "Sport", url: "/shows/sport", external: false },
#                 ],
#               },
#             ],
#           },
#           liveTvMenu: {
#             primaryTitle: "On-Air",
#             primaryItems: [
#               {
#                 channelId: "ten",
#                 channelName: "10",
#                 channelUrl: "https://10.com.au/live/ten",
#                 channelCssClass: "ten",
#                 channelColour: "#1882f8",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2025/06/25/f4cdf0245b4ef0d5cd74929c1217a881-1384576.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2025/06/25/b18ae76555d114f7bfaf1c3bfa43dd3f-1384577.png",
#                 eventTitle: "NBL",
#                 eventStartDate: "2025-11-02T03:30:00Z",
#                 eventEndDate: "2025-11-02T05:29:00Z",
#                 eventRating: "",
#                 eventIsWebLive: true,
#               },
#               {
#                 channelId: "drama",
#                 channelName: "10 Drama",
#                 channelUrl: "https://10.com.au/live/drama",
#                 channelCssClass: "tenbold",
#                 channelColour: "#e6103c",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2025/06/25/a1dd1ff9b4d062a9bcdaafde684b30d5-1384580.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2025/06/25/66c9f2639a7bca4a6691764a0db801d7-1384581.png",
#                 eventTitle: "JAG",
#                 eventStartDate: "2025-11-02T03:00:00Z",
#                 eventEndDate: "2025-11-02T03:59:00Z",
#                 eventRating: "PG",
#                 eventIsWebLive: true,
#               },
#               {
#                 channelId: "comedy",
#                 channelName: "10 Comedy",
#                 channelUrl: "https://10.com.au/live/comedy",
#                 channelCssClass: "tenpeach",
#                 channelColour: "#ba0df9",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2025/06/25/861b025a0af95c74523333b2c0eb8549-1384587.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2025/06/25/443fa2a5bca1191f12efa002a2a8ef85-1384586.png",
#                 eventTitle: "Ridiculousness",
#                 eventStartDate: "2025-11-02T03:34:00Z",
#                 eventEndDate: "2025-11-02T04:04:00Z",
#                 eventRating: "PG",
#                 eventIsWebLive: true,
#               },
#               {
#                 channelId: "nickelodeon",
#                 channelName: "Nickelodeon",
#                 channelUrl: "https://10.com.au/live/nickelodeon",
#                 channelCssClass: "tenshake",
#                 channelColour: "#f15b22",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2023/07/31/9bf17d41aaafa3d5f0c416dfed96ef08-1252730.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2023/07/31/dc4873abc5ba0fde04b59a78c89e0943-1252731.png",
#                 eventTitle: "SpongeBob SquarePants",
#                 eventStartDate: "2025-11-02T03:13:00Z",
#                 eventEndDate: "2025-11-02T03:39:00Z",
#                 eventRating: "G",
#                 eventIsWebLive: true,
#               },
#             ],
#             secondaryTitle: "Featured",
#             secondaryItems: [
#               {
#                 channelId: "south-park",
#                 channelName: "South Park",
#                 channelUrl: "https://10.com.au/live/south-park",
#                 channelCssClass: "south-park",
#                 channelColour: "#dc2f34",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2023/08/03/3c8d2ec1df1b072b7aa68e2a219415a1-1253593.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2023/08/03/41a79ba6a28f011b379ea68d41c28ea0-1253591.png",
#                 eventTitle: "South Park S8 Ep. 8",
#                 eventStartDate: "2025-11-02T03:23:00+00:00",
#                 eventEndDate: "2025-11-02T03:51:00+00:00",
#                 eventRating: "MA15+",
#                 eventIsWebLive: true,
#               },
#               {
#                 channelId: "becker",
#                 channelName: "Becker",
#                 channelUrl: "https://10.com.au/live/becker",
#                 channelCssClass: "becker",
#                 channelColour: "#976ed8",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2023/06/28/263730838d298ff594e227374cf0c963-1246029.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2023/06/28/e0449ed804aaacb1de64f87d94912dd3-1246030.png",
#                 eventTitle: "Becker S4 Ep. 15",
#                 eventStartDate: "2025-11-02T03:30:00+00:00",
#                 eventEndDate: "2025-11-02T03:58:00+00:00",
#                 eventRating: "PG",
#                 eventIsWebLive: true,
#               },
#               {
#                 channelId: "48hours",
#                 channelName: "48 Hours",
#                 channelUrl: "https://10.com.au/live/48hours",
#                 channelCssClass: "forty-eight-hours",
#                 channelColour: "#5f9bfa",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2023/06/28/ba204c627bd221c6dd725d498bb76076-1245996.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2023/06/28/7dd910de29f31095b69e17f1da8f3f0e-1245997.png",
#                 eventTitle: "48 Hours S22 Ep. 60",
#                 eventStartDate: "2025-11-02T03:15:00+00:00",
#                 eventEndDate: "2025-11-02T04:05:00+00:00",
#                 eventRating: "M",
#                 eventIsWebLive: true,
#               },
#               {
#                 channelId: "hardcore-pawn",
#                 channelName: "Hardcore Pawn",
#                 channelUrl: "https://10.com.au/live/hardcore-pawn",
#                 channelCssClass: "hardcorepawn",
#                 channelColour: "#ca9e04",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2025/03/03/467951b2412f2bbda1ba427dd2c9d40f-1366515.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2025/03/03/1d46b70035ba5c816af46c6d4ee079cd-1366514.png",
#                 eventTitle: "Rich vs. Les",
#                 eventStartDate: "2025-11-02T03:28:00+00:00",
#                 eventEndDate: "2025-11-02T03:54:00+00:00",
#                 eventRating: "M",
#                 eventIsWebLive: true,
#               },
#             ],
#             moreItemsTitle: "More Channels",
#             moreItems: [
#               {
#                 channelId: "cops",
#                 channelName: "COPS",
#                 channelUrl: "https://10.com.au/live/cops",
#                 channelCssClass: "cops",
#                 channelColour: "#0a44ff",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2025/03/30/4962cf90377b417b7ee60c2fa5c2f87b-1371072.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2025/03/30/6fadf0873ac36ecacdc63ed8bba4cf3d-1371071.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "mtv-ridiculousness",
#                 channelName: "MTV Ridiculousness",
#                 channelUrl: "https://10.com.au/live/mtv-ridiculousness",
#                 channelCssClass: "mtvridiculousness",
#                 channelColour: "#ff0000",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2024/02/19/1092259b52f72956f99070de99194473-1298685.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2024/02/19/6a7d740896d031b59c9d33d0e6dff544-1298686.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "diagnosismurder",
#                 channelName: "Diagnosis Murder",
#                 channelUrl: "https://10.com.au/live/diagnosismurder",
#                 channelCssClass: "diagnosismurder",
#                 channelColour: "#d20001",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2023/06/28/a1cd4cdbf31746b011394bf319bbfe43-1246004.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2023/06/28/5f85fc3d794a167630b935cb639abcc3-1246005.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "world-of-survivor",
#                 channelName: "World Of Survivor",
#                 channelUrl: "https://10.com.au/live/world-of-survivor",
#                 channelCssClass: "world-of-survivor",
#                 channelColour: "#ffa800",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2024/09/24/c1b85364f9457d04cb39a3c8622c45b5-1340643.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2024/09/24/6a7955dee63fad795d40332b9cfbf8ce-1340644.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "aussie-drama-pop-up",
#                 channelName: "Rush",
#                 channelUrl: "https://10.com.au/live/aussie-drama-pop-up",
#                 channelCssClass: "aussiedramapopup",
#                 channelColour: "#91adb7",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2023/01/24/01cd4d7f2180ecfd47cd16cd5d0e1dc7-1213110.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2023/01/24/082f00086b990e915cd774644d67484c-1213111.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "8-out-of-10-cats",
#                 channelName: "8 Out Of 10 Cats",
#                 channelUrl: "https://10.com.au/live/8-out-of-10-cats",
#                 channelCssClass: "eightoutof10cats",
#                 channelColour: "#f9283e",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2024/11/18/a97a9ff8e9b1cd38b903cf654cff9d39-1350732.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2024/11/18/03a9b9a1a42bcf2ce1bbb94a8fa47224-1350731.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "spongebob-squarepants",
#                 channelName: "SpongeBob SquarePants",
#                 channelUrl: "https://10.com.au/live/spongebob-squarepants",
#                 channelCssClass: "spongebobsquarepants",
#                 channelColour: "#4ebecd",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2024/05/27/8882ec3454814fbb308dcab23bc40404-1316804.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2024/05/27/ee4d9694aa3f7a2fe97b6f18aa773b88-1316803.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "embarrassing-bodies",
#                 channelName: "Embarrassing Bodies",
#                 channelUrl: "https://10.com.au/live/embarrassing-bodies",
#                 channelCssClass: "embarrassing-bodies",
#                 channelColour: "#63c39a",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2024/10/21/d87954431824fdffefeb0c2e51d47a48-1345393.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2024/10/21/f315a8cda9494cc30e29fdba87430ff8-1345391.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "crime-time",
#                 channelName: "Crime Time",
#                 channelUrl: "https://10.com.au/live/crime-time",
#                 channelCssClass: "crime-time",
#                 channelColour: "#ff032d",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2024/09/25/73f13663d37d4a9adfeef8975485dc5b-1341001.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2024/09/25/c27b803a4128c5b097cd3a23e1be973c-1341004.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "nicktoons-90s",
#                 channelName: "NickToons 90s",
#                 channelUrl: "https://10.com.au/live/nicktoons-90s",
#                 channelCssClass: "nicktoons-90s",
#                 channelColour: "#ff6700",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2024/06/06/bb57f5de4d1132a019d25257eca9da2a-1318971.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2024/06/07/a1aaf63737e7d2076759dd850b58471a-1319376.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "crime-hunters",
#                 channelName: "Crime Hunters",
#                 channelUrl: "https://10.com.au/live/crime-hunters",
#                 channelCssClass: "crime-hunters",
#                 channelColour: "#ff2400",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2024/03/06/36e77ca26c7aa8a1522750c045db8469-1301821.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2024/03/06/cb69de15e7b8989a218ad25b7f6547ef-1301820.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#               {
#                 channelId: "nick-jr-club",
#                 channelName: "Nick Jr Club",
#                 channelUrl: "https://10.com.au/live/nick-jr-club",
#                 channelCssClass: "nick-jr",
#                 channelColour: "#ff6700",
#                 channelLogoUrl:
#                   "https://10.com.au/ip/s3/2024/06/06/86eda9b24c03f8501d5cbc932747c2b4-1319010.png",
#                 channelLogoDarkUrl:
#                   "https://10.com.au/ip/s3/2024/06/06/d14509f218578984e3a6f6f34f0ee12c-1319009.png",
#                 eventTitle: null,
#                 eventStartDate: null,
#                 eventEndDate: null,
#                 eventRating: null,
#                 eventIsWebLive: null,
#               },
#             ],
#             cacheKeys: ["content"],
#           },
#           newsMenu: {
#             localisedNewsFirst: {
#               text: "Sydney",
#               url: "/news/sydney",
#               external: false,
#             },
#             tenSportsLinks: [
#               {
#                 subText: "Sport",
#                 imageUrl:
#                   "https://10.com.au/ip/s3/2024/01/24/1a0ea465e95490832bff3cdd9306bfd4-1293803.jpg?image-profile=image_small\\u0026io=landscape",
#                 text: "Sport",
#                 url: "/sport",
#                 external: false,
#               },
#               {
#                 subText: "Football",
#                 imageUrl:
#                   "https://10.com.au/ip/s3/2023/04/06/9314307a0dd6eac0fe82bb016e2ef70a-1228528.jpg?image-profile=image_small\\u0026io=landscape",
#                 text: "Football",
#                 url: "/football",
#                 external: false,
#               },
#               {
#                 subText: "National Basketball League",
#                 imageUrl:
#                   "https://10.com.au/ip/s3/2024/09/10/e1da0ed669ef82952d70cf6b0a2b6db8-1338355.jpg?image-profile=image_small\\u0026io=landscape",
#                 text: "National Basketball League",
#                 url: "/national-basketball-league",
#                 external: false,
#               },
#               {
#                 subText: "A-League",
#                 imageUrl:
#                   "https://10.com.au/ip/s3/2025/10/07/cf8f955e59f6db3bb8e9b40e721cd910-1396416.jpg?image-profile=image_small\\u0026io=landscape",
#                 text: "A-League",
#                 url: "/a-league",
#                 external: false,
#               },
#               {
#                 subText: "Matildas",
#                 imageUrl:
#                   "https://10.com.au/ip/s3/2022/08/30/b39f406e02b17a633c8395b165eacfa8-1176163.jpg?image-profile=image_small\\u0026io=landscape",
#                 text: "Matildas",
#                 url: "/matildas",
#                 external: false,
#               },
#               {
#                 subText: "Roshn Saudi League",
#                 imageUrl:
#                   "https://10.com.au/ip/s3/2023/09/01/7341b93ebeb2acbaa65000554c43daff-1259572.jpg?image-profile=image_small\\u0026io=landscape",
#                 text: "Roshn Saudi League",
#                 url: "/roshn-saudi-league",
#                 external: false,
#               },
#             ],
#             trendingLinks: [
#               {
#                 contentType: "article",
#                 cardLink:
#                   "/the-amazing-race-australia/articles/meet-the-13-teams-tackling-the-amazing-race-australia-celebrity-edition-2025/tpa250319kjuoa",
#                 cardImage: {
#                   url: "https://10.com.au/ip/s3/2025/03/19/02e5b012b4e88494c7a6812960295d8c-1369426.png?image-profile=image_small\\u0026io=landscape",
#                   retinaUrl:
#                     "https://10.com.au/ip/s3/2025/03/19/02e5b012b4e88494c7a6812960295d8c-1369426.png?image-profile=image_small\\u0026io=landscape\\u0026dpr=2",
#                   lazyLoad: true,
#                   alt: "Meet The 13 Teams Tackling The Amazing Race Australia: Celebrity Edition 2025",
#                   placeholderUrl: "/images/Placeholder-Small-234x132.png",
#                 },
#                 cardTitle:
#                   "Meet The 13 Teams Tackling The Amazing Race Australia: Celebrity Edition 2025",
#                 cardDescription:
#                   "Melissa Leong, Gretel Killeen, Bronte Campbell, Ant Middleton,\xc2\xa0Ed Kavalee \\u0026 Tiffiny Hall\xc2\xa0join The Amazing Race Australia: Celebrity Edition.",
#                 videoLabel: null,
#                 videoDuration: null,
#                 datePublished: "2025-03-19T01:48:27",
#                 startDate: null,
#                 endDate: null,
#                 datePublishedString: null,
#                 urlCode: "tpa250319kjuoa",
#                 isLive: false,
#                 id: 1369420,
#                 tpId: "MTI0OTYzMA==",
#                 genre: "Reality",
#               },
#               {
#                 contentType: "article",
#                 cardLink:
#                   "/masterchef/articles/masterchef-australia-back-to-win-2025-meet-the-full-cast/tpa250312nmpld",
#                 cardImage: {
#                   url: "https://10.com.au/ip/s3/2025/03/13/5c02c9bda8577e653f94fce13f9c9c8f-1368510.png?image-profile=image_small\\u0026io=landscape",
#                   retinaUrl:
#                     "https://10.com.au/ip/s3/2025/03/13/5c02c9bda8577e653f94fce13f9c9c8f-1368510.png?image-profile=image_small\\u0026io=landscape\\u0026dpr=2",
#                   lazyLoad: true,
#                   alt: "MasterChef Australia Back To Win 2025: Meet The Full Cast",
#                   placeholderUrl: "/images/Placeholder-Small-234x132.png",
#                 },
#                 cardTitle:
#                   "MasterChef Australia Back To Win 2025: Meet The Full Cast",
#                 cardDescription:
#                   "For the 17th season, we\\u0027re welcoming back familiar faces to the MasterChef kitchen!",
#                 videoLabel: null,
#                 videoDuration: null,
#                 datePublished: "2025-03-15T23:14:55",
#                 startDate: null,
#                 endDate: null,
#                 datePublishedString: null,
#                 urlCode: "tpa250312nmpld",
#                 isLive: false,
#                 id: 1368180,
#                 tpId: "MTgxODYzMA==",
#                 genre: "Reality",
#               },
#               {
#                 contentType: "article",
#                 cardLink:
#                   "/australian-survivor/articles/australian-survivor-2025-brains-v-brawn-meet-the-full-cast/tpa250115ukfqa",
#                 cardImage: {
#                   url: "https://10.com.au/ip/s3/2025/01/19/5515bc0ad14d2d8ad018cfa1e7a4cbb3-1359810.png?image-profile=image_small\\u0026io=landscape",
#                   retinaUrl:
#                     "https://10.com.au/ip/s3/2025/01/19/5515bc0ad14d2d8ad018cfa1e7a4cbb3-1359810.png?image-profile=image_small\\u0026io=landscape\\u0026dpr=2",
#                   lazyLoad: true,
#                   alt: "Australian Survivor 2025: Brains V Brawn - Meet The Full Cast",
#                   placeholderUrl: "/images/Placeholder-Small-234x132.png",
#                 },
#                 cardTitle:
#                   "Australian Survivor 2025: Brains V Brawn - Meet The Full Cast",
#                 cardDescription:
#                   "It\\u0027s the rematch in the battle between mind and muscle, but who will be crowned Australia\\u0027s next Sole Survivor?",
#                 videoLabel: null,
#                 videoDuration: null,
#                 datePublished: "2025-01-19T23:00:00",
#                 startDate: null,
#                 endDate: null,
#                 datePublishedString: null,
#                 urlCode: "tpa250115ukfqa",
#                 isLive: false,
#                 id: 1359365,
#                 tpId: "MTYzOTUzNQ==",
#                 genre: "Reality",
#               },
#               {
#                 contentType: "article",
#                 cardLink:
#                   "/im-a-celebrity-get-me-out-of-here/articles/im-a-celebrity-get-me-out-of-here-2025-meet-the-celebrities/tpa250115choui",
#                 cardImage: {
#                   url: "https://10.com.au/ip/s3/2025/01/19/731306e1a5f79b797573ec22d263eee2-1359750.png?image-profile=image_small\\u0026io=landscape",
#                   retinaUrl:
#                     "https://10.com.au/ip/s3/2025/01/19/731306e1a5f79b797573ec22d263eee2-1359750.png?image-profile=image_small\\u0026io=landscape\\u0026dpr=2",
#                   lazyLoad: true,
#                   alt: "I\xe2\x80\x99m A Celebrity Get Me Out Of Here 2025: Meet The Celebrities",
#                   placeholderUrl: "/images/Placeholder-Small-234x132.png",
#                 },
#                 cardTitle:
#                   "I\xe2\x80\x99m A Celebrity Get Me Out Of Here 2025: Meet The Celebrities",
#                 cardDescription:
#                   "It\\u0027s time to welcome a whole new crew to the South African jungle!",
#                 videoLabel: null,
#                 videoDuration: null,
#                 datePublished: "2025-01-20T05:33:00",
#                 startDate: null,
#                 endDate: null,
#                 datePublishedString: null,
#                 urlCode: "tpa250115choui",
#                 isLive: false,
#                 id: 1359223,
#                 tpId: "MTIyOTUzMw==",
#                 genre: "Reality",
#               },
#             ],
#           },
#         },
#         isHubPage: false,
#         isHomePage: false,
#         isShowPage: false,
#         isDefaultPage: true,
#       };
#     </script>
#     \n\n \n\n
#     <main>
#       \n
#       <div class="content__wrapper">
#         \n
#         <div class="content__wrapper--inner">
#           \n \n
#           <div id="showLanding">
#             <section role="main" class="main__section">
#               <div class="page-title-bar">
#                 <div class="container">
#                   <div class="d-flex justify-between flex-no-wrap align-center">
#                     <h1>Browse Shows</h1>
#                   </div>
#                 </div>
#               </div>
#               <div class="content show__index">
#                 <div class="show__index--filters">
#                   <div class="container">
#                     <div class="d-flex justify-between align-center">
#                       <div class="dropdown">
#                         <div class="dropdown__title dropdown__filled">
#                           <span class="label">Movies</span
#                           ><span class="dropdown__icon icon-angle-down"></span>
#                         </div>
#                       </div>
#                       <div class="filters--genre hide-tablet">
#                         <span>Popular Genres</span
#                         ><input
#                           type="radio"
#                           name="genre"
#                           id="Comedy"
#                           value="23547"
#                         /><label for="Comedy">Comedy</label
#                         ><input
#                           type="radio"
#                           name="genre"
#                           id="Drama"
#                           value="23552"
#                         /><label for="Drama">Drama</label
#                         ><input
#                           type="radio"
#                           name="genre"
#                           id="Reality"
#                           value="23572"
#                         /><label for="Reality">Reality</label>
#                       </div>
#                       <div class="filters--sorting">
#                         <input
#                           type="radio"
#                           name="sorting"
#                           id="popular"
#                           value="popular"
#                           checked=""
#                         /><label for="popular">Popular</label
#                         ><input
#                           type="radio"
#                           name="sorting"
#                           id="latest"
#                           value="latest"
#                         /><label for="latest">Latest</label
#                         ><input
#                           type="radio"
#                           name="sorting"
#                           id="alphabetical"
#                           value="alphabetical"
#                         /><label for="alphabetical">A to Z</label
#                         ><input
#                           type="radio"
#                           name="sortingOrder"
#                           id="sort"
#                           value="sort"
#                         /><label for="sort" class="hide-mobile"
#                           ><span class="icon-sort-amount-down"></span
#                         ></label>
#                       </div>
#                     </div>
#                   </div>
#                 </div>
#                 <div class="show__index--list">
#                   <div class="container">
#                     <div class="loading-spinner__relative">
#                       <svg
#                         class="loading-spinner loading-spinner--blue"
#                         width="65px"
#                         height="65px"
#                         viewBox="0 0 66 66"
#                         xmlns="http://www.w3.org/2000/svg"
#                       >
#                         <circle
#                           class="loading-spinner__path"
#                           fill="none"
#                           stroke-width="6"
#                           stroke-linecap="round"
#                           cx="33"
#                           cy="33"
#                           r="30"
#                         ></circle>
#                       </svg>
#                     </div>
#                   </div>
#                 </div>
#               </div>
#             </section>
#           </div>
#           \n
#           <script>
#             const showsPageData = {
#               shows: [
#                 {
#                   id: 1388270,
#                   epgData: { seriesCridId: ["1855870"] },
#                   tpId: "MTcyODgzMA==",
#                   name: "BlackBerry",
#                   url: "https://10.com.au/blackberry",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2025/07/30/f3509d6b1dcceefcbaad7df915269af6-1388308.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2025/07/30/f3509d6b1dcceefcbaad7df915269af6-1388308.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "M",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: { showNameTargeting: "blackberry" },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   hasClosedCaptions: "yes",
#                   type: "standard",
#                 },
#                 {
#                   id: 1293279,
#                   epgData: { seriesCridId: ["680166"] },
#                   tpId: "MTcyMzkyOQ==",
#                   name: "Ghost",
#                   url: "https://10.com.au/ghost",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2024/01/28/7b89f5aa03cc2c99b0bdbad06dedf90c-1294461.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2024/01/28/7b89f5aa03cc2c99b0bdbad06dedf90c-1294461.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "M",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: { showNameTargeting: "ghost" },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   hasClosedCaptions: "yes",
#                   type: "standard",
#                 },
#                 {
#                   id: 1206518,
#                   epgData: { seriesCridId: ["996916"] },
#                   tpId: "MTE1NjAyOA==",
#                   name: "Tropic Thunder",
#                   url: "https://10.com.au/tropic-thunder",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2023/01/18/b81a3f52a9018c0fd01d09729aef8f61-1211494.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2023/01/18/b81a3f52a9018c0fd01d09729aef8f61-1211494.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "MA15+",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: { showNameTargeting: "tropic_thunder" },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   hasClosedCaptions: "yes",
#                   type: "movie",
#                 },
#                 {
#                   id: 1337231,
#                   epgData: { seriesCridId: ["1785377"] },
#                   tpId: "MTMyNzMzMQ==",
#                   name: "What Men Want",
#                   url: "https://10.com.au/what-men-want",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2024/09/02/9ec89759fb2e8053946d78338b8d515f-1337240.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2024/09/02/9ec89759fb2e8053946d78338b8d515f-1337240.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "M",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: { showNameTargeting: "what_men_want" },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   type: "movie",
#                 },
#                 {
#                   id: 1362252,
#                   epgData: { seriesCridId: ["1851402"] },
#                   tpId: "MTUyMjYzMg==",
#                   name: "She\\u0027s All That",
#                   url: "https://10.com.au/shes-all-that",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2025/02/05/dda58f41c14ba056c862493232ffae90-1362259.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2025/02/05/dda58f41c14ba056c862493232ffae90-1362259.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "None",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: { showNameTargeting: "shes_all_that" },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   hasClosedCaptions: "yes",
#                   type: "movie",
#                 },
#                 {
#                   id: 1306879,
#                   epgData: { seriesCridId: ["1733118", "1765842"] },
#                   tpId: "MTc4NjAzOQ==",
#                   name: "Sonic The Hedgehog 2",
#                   url: "https://10.com.au/sonic-the-hedgehog-2",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2024/04/04/3325c3306e9c3fe78e7233436db124c9-1306885.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2024/04/04/3325c3306e9c3fe78e7233436db124c9-1306885.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "PG",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: {
#                     showNameTargeting: "sonic_the_hedgehod_2",
#                   },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 1,
#                     otherCount: 0,
#                   },
#                   hasClosedCaptions: "yes",
#                   type: "movie",
#                 },
#                 {
#                   id: 1341886,
#                   epgData: { seriesCridId: ["785373"] },
#                   tpId: "MTg4MTQzNg==",
#                   name: "Bumblebee",
#                   url: "https://10.com.au/bumblebee",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2024/10/01/e6a9cde2d27da09006892f86ecbc5af4-1341896.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2024/10/01/e6a9cde2d27da09006892f86ecbc5af4-1341896.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "M",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: { showNameTargeting: "bumblebee" },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   hasClosedCaptions: "yes",
#                   type: "movie",
#                 },
#                 {
#                   id: 1397640,
#                   epgData: { seriesCridId: ["1875522"] },
#                   tpId: "MTQ2NzkzMA==",
#                   name: "A Really Haunted Loud House",
#                   url: "https://10.com.au/a-really-haunted-loud-house",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2025/10/20/804bef7c20b5e98e89106de9143a725e-1397653.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2025/10/20/804bef7c20b5e98e89106de9143a725e-1397653.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "PG",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: {
#                     showNameTargeting: "a_really_haunted_loud_house",
#                   },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   type: "standard",
#                 },
#                 {
#                   id: 1299991,
#                   epgData: { seriesCridId: ["1317795"] },
#                   tpId: "MTk5OTkyMQ==",
#                   name: "Cast Away",
#                   url: "https://10.com.au/cast-away",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2024/02/28/47751a90546d9bb7aef25de699944399-1300599.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2024/02/28/47751a90546d9bb7aef25de699944399-1300599.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "M",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: { showNameTargeting: "cast_away" },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   hasClosedCaptions: "yes",
#                   type: "movie",
#                 },
#                 {
#                   id: 1362986,
#                   epgData: { seriesCridId: ["1855867"] },
#                   tpId: "MTg5MjYzNg==",
#                   name: "Finding Neverland",
#                   url: "https://10.com.au/finding-neverland",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2025/02/10/a83f7774dfedecc4ea53dcfac595a75e-1362996.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2025/02/10/a83f7774dfedecc4ea53dcfac595a75e-1362996.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "PG",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: { showNameTargeting: "finding_neverland" },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   hasClosedCaptions: "yes",
#                   type: "standard",
#                 },
#                 {
#                   id: 1304290,
#                   epgData: { seriesCridId: ["241511"] },
#                   tpId: "MTkyNDAzMA==",
#                   name: "School Of Rock",
#                   url: "https://10.com.au/school-of-rock",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2024/03/20/65cd8d9009a518a19afeff268c035c24-1304299.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2024/03/20/65cd8d9009a518a19afeff268c035c24-1304299.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "PG",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: {
#                     showNameTargeting: "school_of_rock_movie",
#                   },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   hasClosedCaptions: "yes",
#                   type: "movie",
#                 },
#                 {
#                   id: 1364016,
#                   epgData: { seriesCridId: ["241509"] },
#                   tpId: "MTEwNDYzNg==",
#                   name: "Rat Race",
#                   url: "https://10.com.au/rat-race",
#                   genres: ["Movies"],
#                   genreDisplayNames: [""],
#                   secondaryGenres: [],
#                   poster: {
#                     url: "https://10.com.au/ip/s3/2025/02/13/a86ba9f7a0177774634e66e534c6126d-1364025.jpg?image-profile=image_poster\\u0026io=portrait",
#                     retinaUrl:
#                       "https://10.com.au/ip/s3/2025/02/13/a86ba9f7a0177774634e66e534c6126d-1364025.jpg?image-profile=image_poster\\u0026io=portrait\\u0026dpr=2",
#                     lazyLoad: true,
#                     alt: null,
#                     placeholderUrl: "/images/Placeholder-Poster-193x293.png",
#                   },
#                   landscape: null,
#                   showRatingClassification: "M",
#                   aliases: [],
#                   hiddenFeatures: {
#                     search: false,
#                     autoSurfacing: false,
#                     footerLinks: false,
#                     showsIndex: false,
#                   },
#                   adOpsInformation: { showNameTargeting: "rat_race" },
#                   videoCount: {
#                     episodesCount: 1,
#                     extrasCount: 0,
#                     otherCount: 0,
#                   },
#                   type: "movie",
#                 },
#               ],
#               genres: [
#                 {
#                   name: "Adventure",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23589,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329whm",
#                   identifier: "adventure",
#                 },
#                 {
#                   name: "Comedy",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23547,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329yzu",
#                   identifier: "comedy",
#                 },
#                 {
#                   name: "Crime",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: { displayName: "True Crime" },
#                   id: 23534,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329tfl",
#                   identifier: "crime",
#                 },
#                 {
#                   name: "Documentary",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23553,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329szw",
#                   identifier: "documentary",
#                 },
#                 {
#                   name: "Drama",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23552,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329stc",
#                   identifier: "drama",
#                 },
#                 {
#                   name: "Kids",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23833,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190401lfo",
#                   identifier: "kids",
#                 },
#                 {
#                   name: "Lifestyle",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23533,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329qom",
#                   identifier: "lifestyle",
#                 },
#                 {
#                   name: "Light Entertainment",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23539,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329dqr",
#                   identifier: "light-entertainment",
#                 },
#                 {
#                   name: "Movies",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 61761,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg211206rdcuy",
#                   identifier: "movie",
#                 },
#                 {
#                   name: "News",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23566,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329moj",
#                   identifier: "news",
#                 },
#                 {
#                   name: "Reality",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23572,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329tci",
#                   identifier: "reality",
#                 },
#                 {
#                   name: "Religious",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: { displayName: null },
#                   id: 86188,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg241010mnkti",
#                   identifier: "religious",
#                 },
#                 {
#                   name: "Sport",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23565,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329mnq",
#                   identifier: "sport",
#                 },
#               ],
#               selectedGenre: {
#                 name: "Movies",
#                 hiddenFromMegaMenu: false,
#                 genreInformation: null,
#                 id: 61761,
#                 datePublished: null,
#                 dateModified: null,
#                 status: "Publish",
#                 urlCode: "sg211206rdcuy",
#                 identifier: "movie",
#               },
#               popularGenres: [
#                 {
#                   name: "Comedy",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23547,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329yzu",
#                   identifier: "comedy",
#                 },
#                 {
#                   name: "Drama",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23552,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329stc",
#                   identifier: "drama",
#                 },
#                 {
#                   name: "Reality",
#                   hiddenFromMegaMenu: false,
#                   genreInformation: null,
#                   id: 23572,
#                   datePublished: null,
#                   dateModified: null,
#                   status: "Publish",
#                   urlCode: "sg190329tci",
#                   identifier: "reality",
#                 },
#               ],
#               sort: "popular",
#               sortDirection: "descending",
#               hasMore: true,
#               scriptFile: "ShowsIndex",
#               pageTitle: "Shows for Movies",
#               metaDescription: "Browse Movies Shows on 10",
#               metaKeywords: null,
#               hideFromSearchEngine: false,
#               hideHeaderFooter: false,
#               siteRoot: "https://10.com.au",
#               siteName: "10",
#               facebookAppId: "182472175873300",
#               url: null,
#               canonicalUrl: "https://10.com.au/shows/movies",
#               globalSettings: {
#                 playbackSettings: { consumerAdviceDisplayTime: 8 },
#                 experiments: {
#                   "Freewheel Enabled": {
#                     enabled: true,
#                     rolloutPercentage: 100,
#                   },
#                 },
#               },
#               bodyClass: "defaultpage",
#               pageType: "ShowsPage",
#               themeColor: "#0047f4",
#               turnOffAds: false,
#               cacheKeys: ["content"],
#             };
#           </script>
#           \n
#           <div id="quick-links">
#             <div class="content quicklinks">
#               <div class="container">
#                 <div class="row no-gutters">
#                   <header class="content__header"><h3>More from 10</h3></header>
#                   <div class="content__wrapper">
#                     <div class="row">
#                       <div class="col-12 col-md-6 col-lg-3">
#                         <div class="ql ql-1"></div>
#                       </div>
#                       <div class="col-12 col-md-6 col-lg-3">
#                         <div class="ql ql-2"></div>
#                       </div>
#                       <div class="col-12 col-md-6 col-lg-3">
#                         <div class="ql ql-3"></div>
#                       </div>
#                       <div class="col-12 col-md-6 col-lg-3">
#                         <div class="ql ql-4"></div>
#                       </div>
#                     </div>
#                   </div>
#                 </div>
#               </div>
#             </div>
#           </div>
#           \n\n
#         </div>
#         \n
#       </div>
#       \n
#     </main>
#     \n\n \n \n
#     <div id="footer">
#       <footer class="global-footer">
#         <div class="global-footer__navigation">
#           <div class="container">
#             <div class="row no-gutters">
#               <div class="col-md-6">
#                 <div class="global-footer__links-container">
#                   <h4 class="global-footer__headline">Featured TV Shows</h4>
#                   <input
#                     type="checkbox"
#                     class="global-footer__accordion-input"
#                     id="global-footer__accordionOne"
#                   /><label
#                     class="global-footer__accordion-label"
#                     for="global-footer__accordionOne"
#                     ><span class="global-footer__accordion-icon"></span
#                   ></label>
#                   <ul
#                     class="global-footer__links global-footer__links--columns"
#                   >
#                     <li>
#                       <a href="/australian-survivor" class="global-footer__link"
#                         >Australian Survivor</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/charmed" class="global-footer__link">Charmed</a>
#                     </li>
#                     <li>
#                       <a
#                         href="/days-of-our-lives-fast-tracked"
#                         class="global-footer__link"
#                         >Days of our Lives Fast-Tracked</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/deal-or-no-deal" class="global-footer__link"
#                         >Deal Or No Deal</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/dessert-masters" class="global-footer__link"
#                         >Dessert Masters</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/friends" class="global-footer__link">Friends</a>
#                     </li>
#                     <li>
#                       <a href="/general-hospital" class="global-footer__link"
#                         >General Hospital</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/hunted" class="global-footer__link">Hunted</a>
#                     </li>
#                     <li>
#                       <a
#                         href="/im-a-celebrity-get-me-out-of-here"
#                         class="global-footer__link"
#                         >I&#x27;m A Celebrity...Get Me Out Of Here!</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/masterchef" class="global-footer__link"
#                         >MasterChef</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/ncis" class="global-footer__link">NCIS</a>
#                     </li>
#                     <li>
#                       <a href="/ncis-sydney" class="global-footer__link"
#                         >NCIS: Sydney</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/neighbours" class="global-footer__link"
#                         >Neighbours</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/paw-patrol" class="global-footer__link"
#                         >Paw Patrol</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/prisoner" class="global-footer__link"
#                         >Prisoner</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="/survivor-new-zealand"
#                         class="global-footer__link"
#                         >Survivor New Zealand</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="/survivor-south-africa"
#                         class="global-footer__link"
#                         >Survivor South Africa</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/survivor-uk" class="global-footer__link"
#                         >Survivor UK</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/survivor-us" class="global-footer__link"
#                         >Survivor US</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/taskmaster" class="global-footer__link"
#                         >Taskmaster</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="/thank-god-youre-here"
#                         class="global-footer__link"
#                         >Thank God You&#x27;re Here</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="/the-amazing-race-australia"
#                         class="global-footer__link"
#                         >The Amazing Race Australia</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/the-big-bang-theory" class="global-footer__link"
#                         >The Big Bang Theory</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="/the-brokenwood-mysteries"
#                         class="global-footer__link"
#                         >The Brokenwood Mysteries</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/the-cheap-seats" class="global-footer__link"
#                         >The Cheap Seats</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="/the-dog-house-australia"
#                         class="global-footer__link"
#                         >The Dog House Australia</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="/the-inspired-unemployeds-impractical-jokers"
#                         class="global-footer__link"
#                         >The Inspired Unemployed&#x27;s (Impractical) Jokers</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="/the-young-and-the-restless-fast-tracked"
#                         class="global-footer__link"
#                         >The Young and the Restless Fast-Tracked</a
#                       >
#                     </li>
#                   </ul>
#                 </div>
#               </div>
#               <div class="col-md-3 col-middle">
#                 <div class="global-footer__links-container">
#                   <h4 class="global-footer__headline">Sport</h4>
#                   <input
#                     type="checkbox"
#                     class="global-footer__accordion-input"
#                     id="global-footer__accordion_mid_index0"
#                   /><label
#                     class="global-footer__accordion-label"
#                     for="global-footer__accordion_mid_index0"
#                     ><span class="global-footer__accordion-icon"></span
#                   ></label>
#                   <ul class="global-footer__links">
#                     <li>
#                       <a href="/sport" class="global-footer__link"
#                         >Sport Home</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/football" class="global-footer__link"
#                         >Football Home</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/socceroos" class="global-footer__link"
#                         >Socceroos</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/matildas" class="global-footer__link"
#                         >Matildas</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="/national-basketball-league"
#                         class="global-footer__link"
#                         >National Basketball League</a
#                       >
#                     </li>
#                   </ul>
#                 </div>
#                 <div class="global-footer__links-container">
#                   <h4 class="global-footer__headline">Apps</h4>
#                   <input
#                     type="checkbox"
#                     class="global-footer__accordion-input"
#                     id="global-footer__accordion_mid_index1"
#                   /><label
#                     class="global-footer__accordion-label"
#                     for="global-footer__accordion_mid_index1"
#                     ><span class="global-footer__accordion-icon"></span
#                   ></label>
#                   <ul class="global-footer__links">
#                     <li>
#                       <a
#                         href="https://itunes.apple.com/au/app/10-play/id409289742?mt=8"
#                         class="global-footer__link"
#                         target="_blank"
#                         rel="noopener noreferrer"
#                         >iOS</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://play.google.com/store/apps/details?id=au.com.tenplay"
#                         class="global-footer__link"
#                         target="_blank"
#                         rel="noopener noreferrer"
#                         >Android</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://10.com.au/apps"
#                         class="global-footer__link"
#                         >Apple TV</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://10.com.au/apps"
#                         class="global-footer__link"
#                         >FreeviewPlus</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://10.com.au/apps"
#                         class="global-footer__link"
#                         >Samsung TV</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://10.com.au/apps"
#                         class="global-footer__link"
#                         >Android TV</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://10.com.au/apps"
#                         class="global-footer__link"
#                         >Fetch TV</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://10.com.au/apps"
#                         class="global-footer__link"
#                         >Foxtel iQ</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://10.com.au/apps"
#                         class="global-footer__link"
#                         >LG TV</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://10.com.au/apps"
#                         class="global-footer__link"
#                         >Hisense</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://10.com.au/apps"
#                         class="global-footer__link"
#                         >Xbox</a
#                       >
#                     </li>
#                   </ul>
#                 </div>
#                 <div class="global-footer__links-container">
#                   <h4 class="global-footer__headline">News</h4>
#                   <input
#                     type="checkbox"
#                     class="global-footer__accordion-input"
#                     id="global-footer__accordion_mid_index2"
#                   /><label
#                     class="global-footer__accordion-label"
#                     for="global-footer__accordion_mid_index2"
#                     ><span class="global-footer__accordion-icon"></span
#                   ></label>
#                   <ul class="global-footer__links">
#                     <li>
#                       <a href="/news/national" class="global-footer__link"
#                         >10 News</a
#                       >
#                     </li>
#                   </ul>
#                 </div>
#               </div>
#               <div class="col-md-3">
#                 <div class="global-footer__links-container">
#                   <h4 class="global-footer__headline">About Network 10</h4>
#                   <input
#                     type="checkbox"
#                     class="global-footer__accordion-input"
#                     id="global-footer__accordionFive"
#                   /><label
#                     class="global-footer__accordion-label"
#                     for="global-footer__accordionFive"
#                     ><span class="global-footer__accordion-icon"></span
#                   ></label>
#                   <ul class="global-footer__links">
#                     <li>
#                       <a
#                         href="https://careers.paramount.com/"
#                         class="global-footer__link"
#                         target="_blank"
#                         rel="noopener noreferrer"
#                         >Careers</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://www.paramountanz.com.au/"
#                         class="global-footer__link"
#                         target="_blank"
#                         rel="noopener noreferrer"
#                         >Corporate</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         href="https://www.paramountplus.com/?ftag=IPP-06-10aag2h"
#                         class="global-footer__link"
#                         target="_blank"
#                         rel="noopener noreferrer"
#                         >Paramount Plus</a
#                       >
#                     </li>
#                     <li>
#                       <a
#                         target="_self"
#                         rel="noopener noreferrer"
#                         href="https://10.com.au/podcasts"
#                         class="global-footer__link"
#                         >Podcasts</a
#                       >
#                     </li>
#                   </ul>
#                 </div>
#                 <div class="global-footer__links-container">
#                   <h4 class="global-footer__headline">Help</h4>
#                   <input
#                     type="checkbox"
#                     class="global-footer__accordion-input"
#                     id="global-footer__accordionSix"
#                   /><label
#                     class="global-footer__accordion-label"
#                     for="global-footer__accordionSix"
#                     ><span class="global-footer__accordion-icon"></span
#                   ></label>
#                   <ul class="global-footer__links">
#                     <li>
#                       <a
#                         href="https://helpdesk.tenplay.com.au/support/home"
#                         class="global-footer__link"
#                         target="_blank"
#                         rel="noopener noreferrer"
#                         >10 Support</a
#                       >
#                     </li>
#                   </ul>
#                 </div>
#                 <div class="global-footer__links-container">
#                   <h4 class="global-footer__headline">On Network 10</h4>
#                   <input
#                     type="checkbox"
#                     class="global-footer__accordion-input"
#                     id="global-footer__accordionEight"
#                   /><label
#                     class="global-footer__accordion-label"
#                     for="global-footer__accordionEight"
#                     ><span class="global-footer__accordion-icon"></span
#                   ></label>
#                   <ul class="global-footer__links">
#                     <li>
#                       <a href="/shows" class="global-footer__link"
#                         >10, 10 Comedy, Nickelodeon &amp; 10 Drama TV Shows</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/tv-guide" class="global-footer__link"
#                         >Check TV Guide</a
#                       >
#                     </li>
#                     <li>
#                       <a href="/live" class="global-footer__link">Watch LIVE</a>
#                     </li>
#                     <li>
#                       <a
#                         href="/10-trending/articles"
#                         class="global-footer__link"
#                         >10 Trending</a
#                       >
#                     </li>
#                   </ul>
#                 </div>
#                 <div class="global-footer__links-container">
#                   <h4 class="global-footer__headline">Social</h4>
#                   <input
#                     type="checkbox"
#                     class="global-footer__accordion-input"
#                     id="global-footer__accordionNine"
#                   /><label
#                     class="global-footer__accordion-label"
#                     for="global-footer__accordionNine"
#                     ><span class="global-footer__accordion-icon"></span
#                   ></label>
#                   <ul class="global-footer__links">
#                     <li>
#                       <a
#                         href="/social-community-guidelines"
#                         class="global-footer__link"
#                         >Social Community Guidelines</a
#                       >
#                     </li>
#                     <li class="social__links social__links--horizontal">
#                       <a
#                         class="icon-facebook"
#                         href="https://www.facebook.com/Channel10"
#                         rel="noopener noreferrer"
#                         target="_blank"
#                         aria-label="Visit us on Facebook"
#                       ></a
#                       ><a
#                         class="icon-x"
#                         href="https://twitter.com/channel10au"
#                         rel="noopener noreferrer"
#                         target="_blank"
#                         aria-label="Visit us on X"
#                       ></a
#                       ><a
#                         class="icon-instagram"
#                         href="https://www.instagram.com/channel10au/"
#                         rel="noopener noreferrer"
#                         target="_blank"
#                         aria-label="Visit us on Instagram"
#                       ></a>
#                     </li>
#                   </ul>
#                 </div>
#               </div>
#             </div>
#           </div>
#         </div>
#         <div class="global-footer__logos-container">
#           <ul class="global-footer__logos">
#             <li>
#               <a class="global-footer__logos-link" href="https://10.com.au/"
#                 ><img
#                   src="/images/10-Logo-Blue.png"
#                   alt="10"
#                   class="global-footer__logo"
#               /></a>
#             </li>
#             <li>
#               <a
#                 class="global-footer__logos-link"
#                 href="https://10.com.au/live/bold"
#                 ><img
#                   src="/images/10-Drama-Logo-Red.png"
#                   alt="10 Drama"
#                   class="global-footer__logo"
#               /></a>
#             </li>
#             <li>
#               <a
#                 class="global-footer__logos-link"
#                 href="https://10.com.au/live/peach"
#                 ><img
#                   src="/images/10-Comedy-Logo-Purple.png"
#                   alt="10 Comedy"
#                   class="global-footer__logo"
#               /></a>
#             </li>
#             <li>
#               <a
#                 class="global-footer__logos-link"
#                 href="https://10.com.au/live/nickelodeon"
#                 ><img
#                   src="/images/nick_logo-dark.png"
#                   alt="Nickelodeon"
#                   class="global-footer__logo nickelodeon"
#               /></a>
#             </li>
#             <li>
#               <a
#                 class="global-footer__logos-link"
#                 href="https://www.paramountplus.com/?ftag=IPP-06-10aag2h"
#                 target="_blank"
#                 rel="noopener noreferrer"
#                 ><img
#                   src="/images/PPlus-Logo.png"
#                   alt="Paramount Plus"
#                   class="global-footer__logo"
#               /></a>
#             </li>
#           </ul>
#         </div>
#         <div class="global-footer__boilerplate">
#           <ul class="global-footer__boilerplate-links">
#             <li>
#               <a
#                 href="https://www.paramountanz.com.au/advertise/why-10/"
#                 class="global-footer__boilerplate-link"
#                 >Advertise with Us</a
#               >
#             </li>
#             <li>
#               <a href="/terms-of-use" class="global-footer__boilerplate-link"
#                 >Terms of Use</a
#               >
#             </li>
#             <li>
#               <a
#                 rel="noopener noreferrer"
#                 target="_blank"
#                 href="https://privacy.paramount.com/policy"
#                 class="global-footer__boilerplate-link"
#                 >Privacy Policy</a
#               >
#             </li>
#             <li>
#               <a
#                 href="https://helpdesk.tenplay.com.au/support/solutions/folders/16000017381"
#                 class="global-footer__boilerplate-link"
#                 >FAQs</a
#               >
#             </li>
#             <li>
#               <a
#                 href="https://careers.paramount.com/"
#                 class="global-footer__boilerplate-link"
#                 >Careers</a
#               >
#             </li>
#             <li>
#               <a
#                 href="https://www.paramountanz.com.au/"
#                 class="global-footer__boilerplate-link"
#                 >Corporate</a
#               >
#             </li>
#             <li>
#               <a href="/contact-us" class="global-footer__boilerplate-link"
#                 >Contact Us</a
#               >
#             </li>
#           </ul>
#           <p class="global-footer__boilerplate-text acknowledgement-text">
#             We acknowledge the Aboriginal and Torres Strait Islander peoples as
#             the First Australians and the Traditional Custodians of the lands
#             and waterways on which we live, work and play. We pay our respects
#             to Elders past and present.
#           </p>
#           <p class="global-footer__boilerplate-text">
#             \xc2\xa9
#             <!-- -->2025<!-- -->
#             Network Ten Pty Limited
#           </p>
#         </div>
#       </footer>
#     </div>
#     \n\n \n\n
#     <script src="/js/Vendor.compiled.js?buildId=1761261624" hot-reload></script>
#     \n\n
#     <script
#       src="/js/MyAccountManager.compiled.js?buildId=1761261624"
#       hot-reload
#     ></script>
#     \n
#     <script
#       src="/js/ShowsIndex.compiled.js?buildId=1761261624"
#       hot-reload
#     ></script>
#     \n
#     <script>
#       \n    try {\n        const indexMod = Object.keys(TenPlay).find(function(prop){return prop.indexOf("ndex") > 0});\n        TenPlay.Page = TenPlay[indexMod].Page;\n        TenPlay.Page.init();\n    } catch (err) {\n        console.error("Could not init page", err);\n    }\n
#     </script>
#     \n\n\n
#     <script
#       type="text/javascript"
#       src="//secure-au.imrworldwide.com/v60.js"
#     ></script>
#     \n
#     <script type="text/javascript">
#       \n    var pvar = { cid: "network-ten", content: "0", server: "secure-gl" };\n    var trac = nol_t(pvar);\n    trac.record().post();\n
#     </script>
#     \n<noscript
#       >\n
#       <div>
#         \n
#         <img
#           src="//secure-au.imrworldwide.com/cgi-bin/m?ci=network-ten&amp;cg=0&amp;cc=1&amp;ts=noscript"
#           width="1"
#           height="1"
#           alt=""
#         />\n
#       </div>
#       \n</noscript
#     >\n\n
#   </body>
#   \n
# </html>
