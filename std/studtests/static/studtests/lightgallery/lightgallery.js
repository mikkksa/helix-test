/**
* LightGallery v1.3
* Author: Dmitri Ischenko - ischenkodv@gmail.com
* Freely distributable under MIT-style license
*/
var lightgallery = (function(){

// local variables
var dx,
	dy,
	minContainerWidth,
	readyBound,
	isReady,
	bInProgress,

	// Library options
	options = {
		showOverlay		: true,
		overlayColor	: '#000',
		overlayOpacity	: .85,
		zoomStep		: .2,
		animate			: true,
		framesNumber	: 20,
		speed			: 30,
		resizeSync		: false,	// resize container both vertically and horizontally at the same time
		enableZoom		: true,
		fadeImage		: true,
		alias			: 'lightgallery',
		fullSize		: false,
		minPadding		: 15		// minimal distance between container and window
	},

	// Language variables
	langVars = {
		next	: 'Next',
		prev	: 'Previous',
		zoomIn	: 'Zoom In',
		zoomOut	: 'Zoom Out',
		fullSize: 'Full Size',
		fitScreen: 'Fit screen',
		close	: 'Close',
		image	: 'Image',
		of	: 'of'
	},

	// If Internet Explorer
	isIE,

	/* container and its elements */
	container,		// container which holds image;
	titleBar,		// title bar
	prevBtn,		// "previous" button
	nextBtn,		// "next" button
	imgIndex,		// index of images
	fullSizeBtn,	// button which show image full size

	loaderImage,	// image loader
	picture,		// image
	gallery,
	isOpen,			// if gallery open?
	current,		// index of the current image showing
	oThrobber,		// Throbber
	
	/* Reference to overlay */
	overlay,
	
	/* constants */
	HIDDEN		= 'hidden',
	VISIBLE		= 'visible',
	BLOCK		= 'block',
	NONE		= 'none',
	OPACITY		= 'opacity',
	LEFT		= 'left',
	TOP			= 'top',
	WIDTH		= 'width',
	HEIGHT		= 'height',
	PX			= 'px',
	DIV			= 'div',
	WND			= window,
	DOC			= document,

	images;	// list of images

var G = {

	/**
	 * Set language variables
	 * @param {Object} vars - language variables
	 */
	setLangVars : function(vars){
		extend(langVars, vars);
	},


	/**
	 * Initialize gallery
	 * @param {object} opts - gallery options
	 */
	init : function(opts){

		if (opts) {
			extend(options, opts);
		}
		options.fullSize = options.fullSize ? 1:0;

		if (!readyBound) return bindReady();

		// detect engine
		if (/MSIE ([^;]+)/.test(navigator.userAgent)) {
			isIE = parseFloat( RegExp["$1"] );
		}


		// get images
		images = [];
		var	imgs = DOC.getElementsByTagName('a'),
			regx = new RegExp('^'+options.alias+'\\[([a-zA-Z]+)\\]|'+options.alias+'$'),
			r;		// variable to hold RegEx matches
		
		// filter images that match specified RegEx expression
		for (var i=0, len=imgs.length; i<len; i++) {
			if(imgs[i].rel && (r = imgs[i].rel.match(regx))){
				addEvent(imgs[i],'click', G.showImage);
				if(r = r[1]){
					// save gallery name in image
					imgs[i].__gallery__ = r;

					if(!images[r]) {
						images[r] = [];
					}

					imgs[i].__index__ = images[r].push(imgs[i]) - 1;
				}
			}
		}

		// create overlay and container and add it to body
		var b=DOC.getElementsByTagName('body')[0];
		
		b.appendChild( overlay = _(DIV,{
			id:'LG_overlay',
			events:{click: G.close}
			})
		);
		
		b.appendChild( container = createContainer() );
		innerCont = container.lastChild;

		addEvent(
			(b.attachEvent) ? b : WND,
			'keypress',
			keyPressHandler
		);

		// create new Image element to load images
		(loaderImage = _('img')).onload=function(){
			hideLoadingIcon();

			picture.setAttribute("src", loaderImage.src);
			setContPos(options.fullSize, true);
			preload();
		}

		// define the difference between container and image size
		dy = container.offsetHeight;
		minContainerWidth = isIE ? 200 : container.offsetWidth;
		dx = 0;
		
		// set default color and opacity for overlay
		css(overlay, {
			background:(options.overlayColor),
			display:NONE
		});
		setOpacity(overlay, options.overlayOpacity);
	},

	/**
	 * Open (show) gallery
	 */
	open : function(){
		if (isOpen) return;

		showOverlay();

		// display container
		picture.style.display=BLOCK;
		setContPos();
		css(container, {visibility: VISIBLE, display: BLOCK});
		isOpen = 1;
	},

	/**
	 * Close gallery
	 */
	close : function(){
		hideOverlay();
		css(container, {visibility:HIDDEN,display:NONE});
		isOpen = 0;

		loaderImage.src=picture.src='';
	},

	zoomIn : function(){
		G.Zoom(1 + options.zoomStep);
	},

	zoomOut : function(){
		G.Zoom(1 - options.zoomStep);
	},

	zoomNormal : function(){
		if(this.$disabled)
			return;

		G.Zoom(
			picture.width == loaderImage.width && picture.height == loaderImage.height ? 0 : 1
		);
	},

	Zoom : function(coef){
		hideContent();
		setContPos(coef)
	},

	/**
	 * Shows image when user click it
	 * @param {Object} e - event object
	 */
	showImage : function(e){
		var i = this.__index__;
		stopDefault(e || WND.event);

		if (this.__gallery__ && i > -1) {
			gallery = this.__gallery__;
			G.show(i);
		} else {
			G.showSingle(this);
		}
	},

	/**
	 * Show single image
	 * @param {Element} elem - reference to element
	 */
	showSingle : function(elem){
		G.open();

		// Hide content and show loading icon
		hideContent();
		showLoadingIcon();

		loaderImage.src = elem.href;

		titleBar.innerHTML = elem.title;
		imgIndex.innerHTML = '';
		prevBtn.style.visibility = nextBtn.style.visibility = HIDDEN;
	},

	/**
	 * Show image from the gallery
	 * @param {Number} index - index of the image
	 */
	show : function(index){
		if (index < 0 || index > images[gallery].length-1 || (options.animate && bInProgress))
			return;

		G.open();

		var gal = images[gallery],
			ns = nextBtn.style,
			ps = prevBtn.style;

		hideContent();
		showLoadingIcon();

		bInProgress = 1;
		
		loaderImage.src=gal[index].href;
		titleBar.innerHTML = gal[index].title;
		imgIndex.innerHTML = langVars.image+' '+(index+1)+' '+langVars.of+' '+gal.length;

		current = index;
		
		// show or hide prev/next buttons depending on image index
		hasNext() ? ns.visibility = VISIBLE : ns.visibility = HIDDEN;
		hasPrev() ? ps.visibility = VISIBLE : ps.visibility = HIDDEN;

		WND.focus();
	},

	// show next image
	next : function(){
		G.show(current + 1);
	},

	// show previous image
	prev : function(){
		G.show(current - 1);
	}
}

/**
 * Detects if gallery has next image after current
 */
function hasNext() {
	return (current < (images[gallery].length - 1)) ? true : false;
}

/**
 * Detects if gallery has previous image before current
 */
function hasPrev() {
	return (current) ? true : false;
}

/**
 * Preload adjacent images
 */
function preload(){
	var gal = images[gallery];
	if(!gal) return;
	if (gal[current+1]) (new Image).src = gal[current+1].href;
	if (gal[current-1]) (new Image).src = gal[current-1].href;
}


/**
 * Set the size and position of the container
 * @param callback {Function}
 */
function showOverlay(callback){
	if (options.showOverlay){

		// set overlay size
		var ar = getPageSize();
		css(overlay, {
			width: ar[0] + "px",
			height: ar[1] + "px"
		});

		// show overlay if it's not shown already
		if (overlay.style.display != BLOCK) {
			css(overlay, {display:BLOCK});
			fadeIn(overlay, {end: options.overlayOpacity*100, onend: callback});
		}
	} else {
		if (typeof callback == 'function') {
			callback.call(this);
		}
	}
}

/**
 * Hides overlay
 */
function hideOverlay(){
	fadeOut(overlay, {
		start: options.overlayOpacity*100,
		onEnd : function(){
			overlay.style.display = NONE;
		}
	});
}

/**
 * Set container position
 * @param {number} vScale
 * @param {boolean} bIsOnload - show if function is called from whithin onload event
 */
function setContPos(vScale, bIsOnload){
	// define references and variables
	var	notFitScreen, fsTitle,
		w,h,	// width and height of the container
		padding = options.minPadding*2,
		framesNumber = options.framesNumber,

		// size of the container plus padding
		dLoadWidth = loaderImage.width,
		dLoadHeight = loaderImage.height,

		// size of the viewport and the space available to the container
		ar = getPageSize(),
		dScreenWidth = ar[2],
		dScreenHeight = ar[3],
		dAvailableWidth =  dScreenWidth - padding - dx,
		dAvailableHeight =  dScreenHeight - padding - dy;

	// *****************************************
	// define width and height of the container
	if (vScale == 0 || (bIsOnload && !vScale)) {
		// set size of the container according to the size of the viewport
		if (dLoadWidth > dAvailableWidth || dLoadHeight > dAvailableHeight) {
			var newWidth = dAvailableWidth,
				newHeight = dAvailableWidth * dLoadHeight / dLoadWidth;

			if (newHeight > dAvailableHeight) {
				newHeight = dAvailableHeight;
				newWidth = dAvailableHeight * dLoadWidth / dLoadHeight;
			}

			w = (picture.width = newWidth) + dx;
			h = (picture.height = newHeight) + dy;
		} else {
			w = (picture.width = dLoadWidth) + dx;
			h = (picture.height = dLoadHeight) + dy;
		}

	} else if (vScale==1) {
		// show image in real size
		w = (picture.width = dLoadWidth) + dx;
		h = (picture.height = dLoadHeight) + dy;
	} else if (vScale < 1 || vScale > 1) {
		// zoom image according to vScale
		w = (picture.width *= vScale) + dx;
		h = (picture.height *= vScale) + dy;
	}else{
		w = h = 300;	// default size
		var disableAnimate = true;
	}

	// enable/disable the full size button
	if (notFitScreen = ( w > (dAvailableWidth + dx) || h > (dAvailableHeight + dy) )) {
		fsTitle = langVars.fitScreen;
		fsClass = 'LG_fitScreen';
	} else if (picture.width != dLoadWidth || picture.height != dLoadHeight) {
		fsTitle = langVars.fullSize;
		fsClass = 'LG_zoomNormal';
	}

	fullSizeBtn.$disabled = false;
	if (picture.width == dLoadWidth) {
		// it is real size of the image
		if (notFitScreen) {
			fullSizeBtn.id = fsClass;
			fullSizeBtn.setAttribute('title', fsTitle);
		} else {
			fullSizeBtn.id = 'LG_zoom_disabled';
			fullSizeBtn.$disabled = true;
		}
	} else {
		fullSizeBtn.id = 'LG_zoomNormal';
		fullSizeBtn.setAttribute('title', langVars.fullSize);
	}

	// here we set the minimal width of the container
	w = Math.max(w, minContainerWidth);

	// correct coords according to scroll bars position
	var	scr = getScrollXY(),
		y = (dScreenHeight > h ? (dScreenHeight - h)/2 : options.minPadding) + scr[1],
		x = (dScreenWidth > w ? (dScreenWidth - w)/2 : options.minPadding) + scr[0],

		// set the width of the prev/next buttons as 1/3 of the picture width
		dBtnWidth = (w/3) + 'px',
		dBtnHeight = (h - dy - 10) + 'px';

	css(nextBtn, {width: dBtnWidth, height: dBtnHeight});
	css(prevBtn, {width: dBtnWidth, height: dBtnHeight});

	if(options.animate && !disableAnimate){
		var anime = new Movie(container, framesNumber, options.speed);
		if (options.resizeSync) {
			anime.addThread(WIDTH, 0, w, 0, framesNumber)
				.addThread(LEFT, 0, x, 0, framesNumber)
				.addThread(HEIGHT, 0, h, 0, framesNumber)
				.addThread(TOP, 0, y, 0, framesNumber);
		} else {
			var middle = Math.ceil(framesNumber / 2);
			anime.addThread(WIDTH, 0, w, 0, middle)
				.addThread(LEFT, 0, x, 0, middle)
				.addThread(HEIGHT, 0, h, middle, framesNumber)
				.addThread(TOP, 0, y, middle, framesNumber);
		}
		anime.onEnd = function(){
			showOverlay();
			showContent();
		};
		anime.run();
	}else{
		css(container, {top: y + PX, left: x + PX, width: w + PX, height: h + PX});
		showOverlay();
		showContent();
	}
}

/**
 * Show container content
 */
function showContent(){
	innerCont.style.display = BLOCK;

	if(options.fadeImage){
		fadeIn(picture, {
			frames: 8,
			speed: options.speed,
			onEnd: function(){
				bInProgress = 0;
			}
		});
	} else {
		setOpacity(picture, 100);
		bInProgress = 0;
	}
}

/**
 * Hide container content
 */
function hideContent(){
	innerCont.style.display = NONE;
}

function showLoadingIcon(){
	oThrobber.style.display = BLOCK;
}

function hideLoadingIcon(){
	oThrobber.style.display = NONE;
}

/**
 * Create container
 */
function createContainer(){
	var zoomIn, zoomOut;
	if (options.enableZoom) {
		zoomIn = _(DIV, {
			id: 'LG_zoomIn',
			title: langVars.zoomIn,
			events: {
				click: G.zoomIn
			}
		});
		zoomOut = _(DIV, {id:'LG_zoomOut',title:langVars.zoomOut,
			events:{click:G.zoomOut}
		})
	}
	return _(DIV, {id:'LG_container'},
			oThrobber = _(DIV,{id:'LG_loading'}),
			_(DIV,{id:'LG_innerCont'},
				_(DIV, {id:'LG_panel'},
						zoomIn, zoomOut,
						fullSizeBtn = _(DIV, {id: 'LG_zoomNormal',title: langVars.fullSize,
								events: {click: G.zoomNormal}
							}),
						imgIndex = _(DIV, {id:'LG_imgIndex'}, langVars.image + ' 20 ' + langVars.of + ' 20 '),
						_(DIV,{id:'LG_closeBtn',title:langVars.close,
								events:{click:G.close}
							}),_(DIV,{style:'clear:both'})
					),
					picture = _('img', {id:'LG_pic',width:300,height:300}),
					titleBar = _(DIV, {id:'LG_titleBar'}),
					prevBtn = _(DIV, {id:'LG_prevLink',title:langVars.prev,
										events:{
											click:G.prev,
											mouseover:showBtn,
											mouseout:hideBtn
										}
									}),
					nextBtn = _(DIV,{id:'LG_nextLink',title:langVars.next,
										events:{
											click:G.next,
											mouseover:showBtn,
											mouseout:hideBtn
										}
									})
		)
	)
}

function keyPressHandler(e){
	if(!isOpen)
		return;
	var e = e || WND.event,
		code = e.keyCode ? e.keyCode : (e.which ? e.which : e.charCode);

	switch(code){
		case 110	: G.next();break;		// n key
		case 98		: G.prev();break;		// b key
		case 102	: G.zoomNormal();break;	// f key
		case 43		: G.zoomIn();break;		// +
		case 45		: G.zoomOut();break;	// -
		case 27		: G.close();			// Esc key
		default		: return;
	}

	stopDefault(e);
}

function showBtn(){
	fadeIn(this);
}

function hideBtn(){
	fadeOut(this);
}

function fadeIn(elem, opts){
	opts = opts || {};
	opts.start = opts.start || 0;
	opts.end = opts.end || 100;
	fade(elem, opts);
}
function fadeOut(elem, opts){
	opts = opts || {};
	opts.start = opts.start || 100;
	opts.end = opts.end || 0;
	fade(elem, opts);
}
function fade(elem, opts) {
	if (options.animate){
		var a = new Movie(elem, opts.frames || 5, opts.speed || 40);
		a.addThread(OPACITY, opts.start, opts.end);
		a.onStart = opts.onStart;
		a.onEnd = opts.onEnd;
		a.run();
	}
	else {
		setOpacity(elem, opts.end);
		if (typeof opts.onEnd == 'function') opts.onEnd();
	}
}

/**
 * Prevent default browser action
 * @param e {event}
 */
function stopDefault(e){
	if(e.preventDefault)
		e.preventDefault();
	else
		e.returnValue=false;
}

/**
 * Add event listener
 */
function addEvent(el, type, fn) {
	if (WND.addEventListener) {
		addEvent = function(el, type, fn) {
			el.addEventListener(type, fn, false);
		}
	} else if (WND.attachEvent) {
		addEvent = function(el, type, fn) {
			var f = function() {
				fn.call(el, WND.event);
			}
			el.attachEvent('on' + type, f);
		}
	}
	return addEvent(el,type,fn);
}

/**
 * Extends object with properties of another object
 * @param {object} target
 * @param {object} source
 */
function extend(target, source) {
	for (var i in source)
		target[i] = source[i];
}

/**
* Set CSS style of the element
* @param {object} elem
* @param {object} styles
*/
function css(elem, styles){
	if (elem){
		extend(elem.style, styles);
	}
}

/**
 * Get the page and viewport size
 * @return {Array}
 */
function getPageSize(){
	var xScroll, yScroll, windowWidth, windowHeight, b = DOC.body, de = DOC.documentElement;
	if (WND.innerHeight && WND.scrollMaxY) {
		xScroll = b.scrollWidth;
		yScroll = WND.innerHeight + WND.scrollMaxY;
	} else if (b.scrollHeight > b.offsetHeight){ // all but Explorer Mac
		xScroll = b.scrollWidth;
		yScroll = b.scrollHeight;
	} else if (de && de.scrollHeight > de.offsetHeight){ // Explorer 6 strict mode
		xScroll = de.scrollWidth;
		yScroll = de.scrollHeight;
	} else { // Explorer Mac...would also work in Mozilla and Safari
		xScroll = b.offsetWidth;
		yScroll = b.offsetHeight;
	}

	if (WND.innerHeight) { // all except Explorer
		windowWidth = WND.innerWidth;
		windowHeight = WND.innerHeight;
	} else if (de && de.clientHeight) { // Explorer 6 Strict Mode
		windowWidth = de.clientWidth;
		windowHeight = de.clientHeight;
	} else if (b) { // other Explorers
		windowWidth = b.clientWidth;
		windowHeight = b.clientHeight;
	}


	return [
		// Viewport height. For small pages with total width less then width of the viewport
		xScroll < windowWidth? windowWidth : xScroll,

		// Viewport height. For small pages with total height less then height of the viewport
		yScroll < windowHeight? windowHeight : yScroll,

		windowWidth,
		windowHeight
	]
}

/**
 * Get coords of scroll bars
 * @return {Array} - [coord horizontal, coord vertical]
 */
function getScrollXY() {
	var scrOfX = 0, scrOfY = 0, b = DOC.body, de = DOC.documentElement;
	if( typeof( WND.pageYOffset ) == 'number' ) {
		//Netscape compliant
		scrOfY = WND.pageYOffset;
		scrOfX = WND.pageXOffset;
	} else if( b && ( b.scrollLeft || b.scrollTop ) ) {
		//DOM compliant
		scrOfY = b.scrollTop;
		scrOfX = b.scrollLeft;
	} else if( de && ( de.scrollLeft || de.scrollTop ) ) {
		//IE6 Strict
		scrOfY = de.scrollTop;
		scrOfX = de.scrollLeft;
	}
	return [ scrOfX, scrOfY ];
}

/**
 * Get elements style
 * @param {Object} elem - element
 * @param {Object} name - name of the style to get
 */
function getStyle(elem, name) {
	var d = DOC.defaultView;
	if (elem.style[name])
		return elem.style[name];	

	else if (elem.currentStyle)
		return elem.currentStyle[name];

	else if (d && d.getComputedStyle) {
		name = name.replace(/([A-Z])/g,"-$1");

		var s = d.getComputedStyle(elem,"");
		return s && s.getPropertyValue(name.toLowerCase());
	}
	return null;
}

/**
 * Cross-browser function to set element opacity
 * @param {Element} elem - element
 * @param {Number} level - level of opacity, percent
 */
function setOpacity() {
	setOpacity = arguments[0].filters ?
		function(elem,level){elem.style.filter = "alpha(opacity="+level+")"} :
		function(elem,level){elem.style.opacity = level / 100}
	setOpacity(arguments[0],arguments[1]);
}

/**
 * Create HTML element
 * @param {String} tag - tag name
 * @param {Object} attr - attributes to set, ex: {'name':'someClass',value:'the value'}
 */
function _(tag, attr){

	var elem = DOC.createElement(tag);

	if (attr){
		for (var name in attr){
			if(name == 'events'){
				for(var j in attr[name])
					addEvent(elem, j, attr[name][j]);
			}else{
				var value = attr[name];
				if ( typeof value != "undefined" ) {
					if (name == 'class'){
						elem.className = value;
					} else {
						elem.setAttribute(name, value);
					}

				}
			}
		}
	}

	for (var i=2, len=arguments.length; i<len; i++){
		switch (typeof arguments[i]) {
			case 'string': elem.innerHTML += arguments[i]; break;
			case 'object': elem.appendChild(arguments[i]);
		}
	}

	return elem;
}

/**
 * ondomready functionality from jQuery framework:
 */
function ready() {
	if (!isReady) {
		if (!DOC.body) {
			return setTimeout(ready, 13);
		}

		isReady = true;

		G.init();
	}
}

function bindReady() {
	if (readyBound) return;
	readyBound = true;

	if (DOC.readyState === "complete" ) {
		return ready();
	}

	if (DOC.addEventListener) {
		DOC.addEventListener( "DOMContentLoaded", function DOMContentLoaded() {
			DOC.removeEventListener( "DOMContentLoaded", DOMContentLoaded, false );
			ready();
		}, false);

	// If IE event model is used
	} else if (DOC.attachEvent) {
		DOC.attachEvent("onreadystatechange", function onreadystatechange() {
			if ( document.readyState === "complete" ) {
				DOC.detachEvent("onreadystatechange", onreadystatechange);
				ready();
			}
		});

		// If IE and not a frame
		// continually check to see if the document is ready
		var toplevel = false;

		try {
			toplevel = WND.frameElement == null;
		} catch(e){}

		if (DOC.documentElement.doScroll && toplevel) {

			function doScrollCheck() {
				if (isReady) {
					return;
				}

				try {
					// If IE is used, use the trick by Diego Perini
					// http://javascript.nwbox.com/IEContentLoaded/
					DOC.documentElement.doScroll("left");
				} catch(e) {
					setTimeout( doScrollCheck, 1 );
					return;
				}

				// and execute any waiting functions
				ready();
			}

			doScrollCheck();
		}
	}
}

/**
 * Class which makes and run animations
 * @param {Element} oElem - target element
 * @param {Number} dNumFrames - number of frames
 * @param {Number} dSpeed - time between each frame, msec
 * @constructor
 */
function Movie(oElem, dNumFrames, dSpeed){
	if (!oElem)
		return null;

	this.elem = oElem;
	this.numFrames = dNumFrames || 0;
	this.frames = [];		// frames array
	this.speed = dSpeed || 10;
}


Movie.prototype = {

	/**
	 * Add thread - the chain of actions to do on the element
	 * @param {String} style - style name
	 * @param {Number} startValue - value at the beginning of animation
	 * @param {Number} endValue - end value
	 * @param {Number} startFrame - frame, from which the animation of thread begin
	 * @param {Number} endFrame - frame, which ends the animation
	 */
	addThread : function(style, startValue, endValue, startFrame, endFrame){
		if (!style || endValue === undefined || endValue === null) return;

		if(style != OPACITY)
			startValue = parseFloat(getStyle(this.elem, style));

		startFrame = startFrame || 0;
		endFrame = endFrame || this.numFrames;

		var	F = this.frames,						// reference to frames collection
			count = (endFrame - startFrame) || 1,	// number of frames, should be at least 1
			step = (startValue - endValue)/count;

		for (; startFrame<endFrame; startFrame++){
			if (!F[startFrame])
				F[startFrame] = {};
			F[startFrame][style] = (startValue -= step);
		}

		return this;
	},

	/**
	 * The step - run the next frame
	 */
	step : function(){
		var frame = this.frames.shift(),
			styles = [],
			bIsIE = isIE;

		if (frame) {

			for (var i in frame) {
				styles.push(
					i == 'opacity' ?
							( bIsIE ? 'filter: alpha(opacity=' + frame[i] + ')' : 'opacity: ' + frame[i]/100)
						:	i + ': ' + frame[i] + 'px'
					);
			}

			this.elem.style.cssText += '; ' + styles.join('; ');

		} else {
			if (typeof this.onEnd == 'function')
				this.onEnd();

			clearInterval(this.interval);
		}
	},

	/**
	 * Show the animation
	 */
	run : function(){
		clearInterval(this.interval);

		this.step();

		if (typeof this.onStart == 'function')
			this.onStart();

		var that = this;
		if (this.numFrames > 1) {
			this.interval = setInterval(function(){
				that.step();
			}, this.speed);
		}
	}

}

return G;
})();