(function(m){var l=window.AmazonUIPageJS||window.P,r=l._namespace||l.attributeErrors,e=r?r("TwisterCoreAsset"):l;e.guardFatal?e.guardFatal(m)(e,window):e.execute(function(){m(e,window)})})(function(m,l,r){m.when("twister-variation-matrix","twister-dim-util","twister-state-machine","twister-metadata","twister-view-controller","twister-dispatcher","twister-actions","twister-slots-dimsum","twister-dimsum").register("TwisterCore",function(e,h,g,d,a,c,k,f,b){function m(k,l){this.tvm=new e(k);this.util=
new h(this.tvm);this.tsm=new g(this.tvm,this.util,k.initDimCombination);this.dimSum=new b(k.config.ajaxTimeout,k.config.ajaxUrlParams,k.config.deviceType,l);this.slotsDimSum=new f(k.config.ajaxTimeout,k.config.ajaxUrlParams,k.config.deviceType);var p=this;c.registerStore("twister-state-machine",function(b,c){p.tsm.accept(b,c).THEN(function(c){a.publishView(b,c)}).ELSE()});var q=new d;c.registerStore("twister-metadata",function(b,c){q.process(b,c,function(c){a.publishView(b,c)})})}function q(a,b){var d=
a.viewAttribution+"_"+a.viewName+"_"+b;return function(a){try{var e=k.create(b,a);c.dispatch(b,e)}catch(f){l.ueLogError&&l.ueLogError(f,{logLevel:"ERROR",attribution:"Twister_view_"+d,message:"This error is caused by the Twister view - "+d+" while updating the TwisterCore"})}}}m.prototype={registerActive:function(b,c){a.register(b.viewAttribution+"_"+b.viewName,!0,c.updateView);return{dimensionChanged:q(b,"VARIATION_CHANGE"),dimensionPeek:q(b,"VARIATION_PEEK"),metaData:q(b,"METADATA")}},registerPassive:function(b,
c){a.register(b.viewAttribution+"_"+b.viewName,!1,c.updateView);return{metaData:q(b,"METADATA")}},state:function(){return this.tsm.currentState().selected().selectionInfo()}};return m});m.when("A").register("twister-actions",function(e){var h=e.$,g={VARIATION_CHANGE:function(d){return d=h.isArray(d)?d:[d]},VARIATION_PEEK:function(d){return d},METADATA:function(d){return d}};return{create:function(d,a){return g[d]?g[d](a):!1}}});m.when("A","publisherSubscriber").register("twister-dispatcher",
function(e,h){function g(){g=1;return this}var d=e.$,a=new h,g=0,c=[];return{registerStore:function(c,d){a.register(c,d);return this},deregisterStore:function(c){a.deRegister(c);return this},dispatch:function(d,e){g?c.push(arguments):a.publish(d,e);return this},hold:g,release:function(){d.each(c,function(c,d){a.publish.apply(a,d)});g=0;return this}}});m.when("A","publisherSubscriber").register("twister-view-controller",function(e,h){function g(){d?a.push(arguments):(d=1,c.publish.apply(c,
arguments),k.publish.apply(k,arguments),d=0,a.length&&g.apply(this,a.shift()));return this}var d=0,a=[],c=new h,k=new h;return{register:function(a,b,d){b?c.register(a,d):k.register(a,d);return this},deRegister:function(a,b){b?c.deRegister(a):k.deRegister(a);return this},publishView:g}});m.when("A").register("twister-dimsel-api",function(e){function h(d){var a=this;this.dimSelectionMap={};this.selInfo=d;g.each(d,function(c,d){a.dimSelectionMap[d.dimKey]=d.val})}var g=e.$;h.prototype={matches:function(d){d=
d.selectionInfo();for(var a=0;a<d.length;a++){var c=d[a].dimKey;if(!(c in this.dimSelectionMap)||this.dimSelectionMap[c]!==d[a].val)return!1}return!0},selectionInfo:function(){return e.copy(this.selInfo)}};return h});m.when("A","twister-dimsel-api").register("twister-dim-util",function(e,h){function g(a){this.tvm=a;this.dimensionMetaData={};var c=[];a=a.dimensionInfo;for(var d=0;d<a.length;d++){c.push(a[d].dimKey);var e={};e.isRequired=a[d].isRequired;e.isSingleton=a[d].isSingleton;e.dimOrder=
d;e.size=a[d].size;this.dimensionMetaData[a[d].dimKey]=e}}var d=e.$;g.prototype={createSelectionInfo:function(a){return new h(a)},extendSelectionInfo:function(a,c,e){var f=e||0===e,b={},g=[];d.each(c.selectionInfo(),function(a,c){b[c.dimKey]=c.val});d.each(a.selectionInfo(),function(a,c){var d=c.dimKey,h=f?e:c.val;d in b&&(h=b[d]);g.push({dimKey:d,val:h})});return new h(g)},createNextDimSelection:function(a,c){var e=[],f=c.selectionInfo(),b=this;d.each(a.split(":"),function(a,c){var d=f[a].dimKey,
g=parseInt(c,10);b.dimensionMetaData[d].isRequired&&g!==f[a].val&&(g=-1);e.push({dimKey:d,val:g})});return new h(e)},getDimScore:function(a,c){var e=0,f=a.split(":"),b=this;d.each(c.selectionInfo(),function(a,c){var d=c.dimKey,g=c.val,h=parseInt(f[a],10),l=f.length-a;g===h?(e+=200*l,b.dimensionMetaData[d].isRequired&&(e+=2E4)):(g=Math.abs(g-h),d=Math.round(g/b.dimensionMetaData[d].size*100),e+=100-d)});return e},isSingletonDim:function(a){return this.dimensionMetaData[a]?this.dimensionMetaData[a].isSingleton:
!1},isRequiredDim:function(a){return this.dimensionMetaData[a]?this.dimensionMetaData[a].isRequired:!1},getDimensionInfo:function(){return this.tvm.dimensionInfo},getDimAvailability:function(a,c){c=c.selectionInfo?c:this.createSelectionInfo(c);var e=[],f=[],b=this.tvm.dimensionList,g=this.tvm.dimtoValueMap[a],h=this.createSelectionInfo([{dimKey:a,val:-1}]),h=this.tvm.fetch(this.extendSelectionInfo(c,h).selectionInfo()),l={},m=this;d.each(h,function(c,d){l[d.split(":")[b.indexOf(a)]]=m.tvm.dimCombinations[d]});
d.each(g,function(a,b){a in l?e.push({index:a,asin:l[a],label:b}):f.push({index:a,label:b})});return{available:e,unavailable:f}},getUnselectedDims:function(a){var c={};d.each(a,function(a,b){c[b.dimKey]=b.val});a=[];var e=this.tvm.dimensionList,f;for(f in e)if(e.hasOwnProperty(f)){var b=e[f];if(c[b]===r||-1===c[b])this.isSingletonDim(b)?c[b]=0:a.push(b)}return a},showDimSum:function(a,c){var d=this.getUnselectedDims(c);return!d||0===d.length||1===d.length&&d[0]===a?1:0},isFullySelected:function(a){var c=
!0;"string"===typeof a&&(a=this.getSelectionInfoFromDimComb(a));a=a.selectionInfo?a.selectionInfo():a;if(a.length!=this.tvm.dimensionList.length)return!1;d.each(a,function(a,d){-1===d.val&&(c=!1)});return c},createDimensionSelectionMap:function(a){var c={},d;for(d in a)if(a.hasOwnProperty(d)){var e=a[d];c[e.dimKey]=e.val}return c},getSelectedDimKeys:function(a){var c=this.tvm.dimensionList,d=[],e;for(e in c)if(c.hasOwnProperty(e)){var b=a[c[e]];"undefined"===typeof b||-1==b?d.push("*"):d.push(b)}return d},
getValidDimCombination:function(a,c){var e,f,b=this,g=0,h=0;f=this.tvm.fetch(a);d.each(f,function(a,d){h=b.getDimScore(d,c);h>g&&(e=a,g=h)});return f[e]},getAsinFromSelectionInfo:function(a,c){var g,f;"undefined"==typeof c||c?g=this.createDimensionSelectionMap(a):(f=e.copy(a),g=this.getValidDimCombination(f,this.createSelectionInfo(a)),d.each(g.split(":"),function(a,c){var d=parseInt(c,10);f[a].val=d}),g=this.createDimensionSelectionMap(f));g=this.getSelectedDimKeys(g).join(":");return this.tvm.dimCombinations[g]},
getSelectionInfoFromSelectedVariationValuesMap:function(a){var c=[],d;for(d in this.tvm.dimensionList){var e={},b=this.tvm.dimensionList[d];e.dimKey=b;e.val=a[b];c.push(e)}return c},getSelectionInfoFromDimComb:function(a){var c=[];a=a.split("_");for(var d in this.tvm.dimensionList){var e={},b=a[d];e.dimKey=this.tvm.dimensionList[d];e.val="X"===b||"*"===b?-1:parseInt(b,10);c.push(e)}return c},getDimensionDisplayText:function(a){return this.tvm.dimensionDisplayText[a]},getDimensionValueFromIndex:function(a,
c){return(this.tvm.dimtoValueMap[a]||[])[c]},getSelectionInfoFromDimIndexAndValue:function(a,c){var d=[],e={};e.dimKey=this.tvm.dimensionList[a];e.val="X"===c||"*"===c?-1:parseInt(c,10);d.push(e);return d},predictNextState:function(a,c){var e=this.extendSelectionInfo(a,c);if(function(a){var b;d.each(a.selectionInfo(),function(a,c){b=-1===c.val});return b}(c)||this.tvm.exists(e.selectionInfo()))return e;for(var f=this.extendSelectionInfo(a,c,-1),f=this.tvm.fetch(f.selectionInfo()),b=0,g=0,h,l=0;l<
f.length;l++)g=this.getDimScore(f[l],e),g>b&&(h=l,b=g);return this.createNextDimSelection(f[h],e)}};return g});m.when("A","url-builder").register("twister-dimsum",function(e,h){function g(a,c,d,f){this.cache;f&&(this.cache=new f);this.ajaxTimeout=a;this.batchLimit=10;this.ajaxUrl="/gp/twister/dimension?asinList=###asinString###&vs=1"+(c||"");d&&(this.ajaxUrl+="&deviceType="+d);(a=e.state("pwState"))&&a.isTryState&&(this.ajaxUrl=h.addUrlParams(this.ajaxUrl,{isTryState:"true"}))}var d=
e.$;g.prototype={get:function(a,c,g){function f(a){var c=a-this.batchLimit,d="";0<c&&f.call(this,c);if(d=m.slice(0>c?0:c,a).join(","))a=this.ajaxUrl.replace("###asinString###",d),e.ajax(a,{chunk:b,timeout:this.ajaxTimeout})}function b(a){if(a)for(var b in a)if(a.hasOwnProperty(b)){var d=a[b];if(d&&d.asin){if(l){var e=h(d.asin,g);l.put(e,d)}c&&c(d)}}}function h(a,b){var c=a;e.objectIsEmpty(b)||(c={asin:a},d.extend(!0,c,b));return c}var l=this.cache,m=[],r={};d.each(a,function(a,b){var d=h(b,g);l&&
l.get(d)?c?c(l.get(d)):r[b]=l.get(d):m.push(b)});if(!c)return r;f.call(this,m.length)}};return g});m.when("A").register("twister-slots-dimsum",function(e){function h(a,e,f){this.cache=d;this.ajaxTimeout=a;this.batchLimit=8;this.ajaxUrl="/gp/twister/dimension?isDimensionSlotsAjax=1&asinList=###asinString###&vs=1"+(e||"");f&&(this.ajaxUrl+="&deviceType="+f);this.defaultQuerryParamsObj={};this.defaultAddedQueryParamString=""}var g=e.$,d={},a={};h.prototype={get:function(c,d){function f(a){var c=
a-this.batchLimit,d="",g=[];0<c&&f.call(this,c);g=m.slice(0>c?0:c,a);if(d=g.join(","))a=this.ajaxUrl.replace("###asinString###",d),a+="&"+this.defaultAddedQueryParamString,e.ajax(a,{chunk:h,timeout:this.ajaxTimeout,cache:!0,error:b.apply(null,g)})}function b(){var b=arguments;return function(){e.each(b,function(b){delete a[b]})}}function h(b){if(b&&b.ASIN){var c=b.ASIN;l[c]=b;for(d&&d(b);a[c]&&a[c].length;)a[c].pop()(b);delete a[c]}}var l=this.cache,m=[],r={};g.each(c,function(b,c){l[c]?d?d(l[c]):
r[c]=l[c]:a[c]&&d?a[c].push(d):d&&(m.push(c),a[c]=[])});if(!d)return r;m.length&&f.call(this,m.length)},addDefaultQueryParameter:function(a,d){var e=!1;d!==r&&(this.defaultQuerryParamsObj[a]=d,this.defaultAddedQueryParamString=g.param(this.defaultQuerryParamsObj),e=!0);return e}};return h});m.register("twister-metadata",function(){function e(){this.config={}}e.prototype={process:function(e,g,d){"METADATA"===e&&d(g)}};return e});m.when("A").register("publisherSubscriber",
function(e){function h(){this.Subscribers=[];this.Names=[]}var g=e.$;h.prototype={register:function(d,a){if(-1<e.indexOfArray(this.Names,d))return!1;this.Names.push(d);this.Subscribers.push({name:d,handler:a})},deRegister:function(d){var a=e.indexOfArray(this.Names,d),c=this,h=function(a,b){if(a.name===d)return c.Subscribers.splice(b,1),!0};return-1<a?(this.Names.splice(a,1),[].some?this.Subscribers.some(h):g.each(this.Subscribers,function(a,b){h(b,a)}),!0):!1},publish:function(){var d=arguments;
g.each(this.Subscribers,function(a,c){setTimeout(function(){c.handler.apply(null,d)},0)})}};return h});m.when("jQuery").register("twister-state-machine",function(e){return function(e,g,d){function a(a,c){this.selected=function(){return a};this.peek=function(){return c}}function c(a,c){return{THEN:function(d){a&&d&&d(c());return this},ELSE:function(d){a||d&&d(c());return this}}}var k,f;this.accept=function(b,d){var e;switch(b){case "VARIATION_PEEK":var h=g.createSelectionInfo(d);e=k();
e.peek().matches(h)?e=!1:(-1===d.val?e=new a(k.selected(),k.selected()):(h=g.predictNextState(e.peek(),h),e=new a(e.selected(),h)),f=e,e=!0);e=c(e,this.currentState);break;case "VARIATION_CHANGE":e=k();var h=g.createSelectionInfo(d),l=g.getDimensionInfo();e.selected().matches(h)?e=!1:(e=h.selectionInfo().length!==l.length?g.predictNextState(e.selected(),h):h,f=new a(e,e),e=!0);e=c(e,this.currentState);break;default:e=c(!1)}return e};k=this.currentState=function(){return f};(function(a){f=a})(new a(g.createSelectionInfo(d),
g.createSelectionInfo(d)))}});m.when("A").register("twister-variation-matrix",function(e){function h(c){c=e.copy(c);var d=this;this.dimCombinations=c.dimCombinations;this.validCombinatonString=" "+e.keys(c.dimCombinations).join("  ")+" ";this.dimensionInfo=c.dimensionInfo;this.dimensionList=c.dimensionList;this.dimensionDisplayText=c.dimensionDisplayText;this.config=c.config;this.dimInfoMap={};a.each(this.dimensionInfo,function(a,b){var c=b.dimKey,e={};e.size=b.size;e.dimOrder=a;d.dimInfoMap[c]=
e});this.dimtoValueMap=c.dimtoValueMap}function g(c){c=a.map(c,function(a){a=a.val;return-1===a?"\\d+":""+a}).join(":");return new RegExp("\\s"+c+"\\s","gm")}function d(c){return a.map(c,function(a){return""+a.val}).join(":")}var a=e.$;h.prototype={fetch:function(c){c=g(c);c=this.validCombinatonString.match(c);return c=a.map(c,function(c){return a.trim(c)})},exists:function(a){return d(a)in this.dimCombinations}};return h});m.when("A","jQuery").register("url-builder",function(e,h){function g(a,
d){var f;if(a&&d&&"object"==typeof d){f=a;var b="?";e.each(d,function(a,c){a=d[c];f+=b+c+"="+a;b="&"})}return f}function d(a){var d;a&&(d=a.split("?")[0]);return d}function a(a){var d={};a&&(a=a.split("?"),1<a.length&&(a=a[1].split("&"),e.each(a,function(a,b){var c=a.split("=");d[c[0]]=c[1]})));return d}return{addUrlParams:function(c,e){var f=c;if(c&&e&&"object"==typeof e)var f=d(c),b=a(c),b=h.extend(b,e),f=g(f,b);return f},removeUrlParams:function(c,h){var f=c;if(c&&h&&"object"==typeof h){var f=
d(c),b=a(c);e.each(h,function(a,c){delete b[a]});f=g(f,b)}return f}}})});