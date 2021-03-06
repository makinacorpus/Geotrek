Leaflet.Control.FullScreen
============

Downloads
------

[v1.1.1](https://github.com/brunob/leaflet.fullscreen/releases/tag/1.1.0) for Leaflet stable release

[v1.0.0](https://github.com/brunob/leaflet.fullscreen/archive/1.0.0.zip) for Leaflet < 0.6

What ?
------

Simple plugin for Leaflet that adds fullscreen button to your maps.

Inspired by http://elidupuis.github.com/leaflet.zoomfs/

Use the native javascript fullscreen API http://johndyer.name/native-fullscreen-javascript-api-plus-jquery-plugin/

Released under the MIT License http://opensource.org/licenses/mit-license.php

How ?
------

Include Control.FullScreen.js and Control.FullScreen.css in your page:

``` html
 <link rel="stylesheet" href="Control.FullScreen.css" />
 <script src="Control.FullScreen.js"></script>
```

Add the fullscreen control to the map:

``` js
var map = new L.Map('map', {
  fullscreenControl: true,
  fullscreenControlOptions: {
    position: 'topleft'
  }
});
```

If your map have a zoomControl the fullscreen button will be added at the bottom of this one.

If your map doesn't have a zoomContron the fullscreen button will be added to topleft corner of the map (same as the zoomcontrol).

__Events and options__:

``` js
// create a fullscreen button and add it to the map
L.control.fullscreen({
  position: 'topleft', // change the position of the button can be topleft, topright, bottomright or bottomleft, defaut topleft
  title: 'Show me the fullscreen !', // change the title of the button, default Full Screen
  forceSeparateButton: true, // force seperate button to detach from zoom buttons, default false
  forcePseudoFullscreen: true // force use of pseudo full screen even if full screen API is available, default false
}).addTo(map);

// events are fired when entering or exiting fullscreen.
map.on('enterFullscreen', function(){
  console.log('entered fullscreen');
});

map.on('exitFullscreen', function(){
  console.log('exited fullscreen');
});
```

Where ?
------

Source code : https://github.com/brunob/leaflet.fullscreen

Demo : http://brunob.github.com/leaflet.fullscreen/
