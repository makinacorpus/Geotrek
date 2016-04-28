from .prod import *


# Necessary block of config when maps are not from Geotrek Tilecache :
LEAFLET_CONFIG['SRID'] = 3857
LEAFLET_CONFIG['TILES'] = [
    (gettext_noop('Scan'), 'http://gpp3-wxs.ign.fr/u1v3m6passq1fujg84dme9ga/geoportail/wmts?LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.CLASSIQUE&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
     '&copy; IGN - GeoPortail'),
    (gettext_noop('Scan Express'), 'http://gpp3-wxs.ign.fr/u1v3m6passq1fujg84dme9ga/geoportail/wmts?LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
     '&copy; IGN - GeoPortail'),
    (gettext_noop('Ortho'), 'http://gpp3-wxs.ign.fr/u1v3m6passq1fujg84dme9ga/geoportail/wmts?LAYER=ORTHOIMAGERY.ORTHOPHOTOS&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
     '&copy; IGN - GeoPortail'),
    (gettext_noop('OSM'), 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', '(c) OpenStreetMap Contributors'),
    #(gettext_noop('Cadastre'), 'http://gpp3-wxs.ign.fr/u1v3m6passq1fujg84dme9ga/geoportail/wmts?LAYER=CADASTRALPARCELS.PARCELS&EXCEPTIONS=image/jpeg&FORMAT=image/png&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
    # '&copy; IGN - GeoPortail'),
]

SPLIT_TREKS_CATEGORIES_BY_PRACTICE = True

FORCED_LAYERS = [
    ('OSM',
     [(51.11041991029261, 2.548828125),
      (49.468124067331644, 6.35009765625),
      (49.475263243037986, 6.4324951171875),
      (49.41812070066643, 6.5533447265625),
      (49.163746759588975, 6.734619140625),
      (49.24987918000417, 6.83349609375),
      (49.18170338770663, 7.05322265625),
      (49.12062427498834, 7.042236328124999),
      (49.160154652338015, 7.124633789062499),
      (49.11343354595957, 7.305908203125),
      (49.146681929552095, 7.315521240234376),
      (49.1448852896622, 7.362213134765626,),
      (49.17182804827916, 7.3663330078125),
      (49.18708910605573, 7.4432373046875),
      (49.169134431937806, 7.44049072265625),
      (49.17182804827916, 7.491302490234375),
      (49.15296965617039, 7.505035400390625),
      (49.13410408228901, 7.494049072265625),
      (49.1233205296222, 7.516021728515624),
      (49.09814978542758, 7.529754638671874),
      (49.081062364320736, 7.566833496093749),
      (49.08466020484928, 7.606658935546874),
      (49.07206662261101, 7.63275146484375),
      (49.05407025156395, 7.634124755859376),
      (49.045969758350786, 7.680816650390624),
      (49.0558701819386, 7.697296142578124),
      (49.05407025156395, 7.730255126953124),
      (49.0477699820096, 7.750854492187499),
      (49.06486885623368, 7.794799804687499),
      (49.042369115505004, 7.8662109375),
      (49.05047019529436, 7.912902832031251),
      (49.057670047140604, 7.928009033203125),
      (49.01265386395502, 8.051605224609375),
      (48.98742700601184, 8.118896484375),
      (48.97390736160895, 8.238372802734375),
      (48.80505453139158, 8.062591552734375),
      (48.585692256886624, 7.80029296875),
      (48.04136507445029, 7.5750732421875),
      (47.96050238891509, 7.630004882812499),
      (47.68388118858139, 7.5146484375),
      (47.58764167941513, 7.5640869140625),
      (47.42065432071321, 7.344360351562499),
      (43.73935207915473, 7.66845703125),
      (42.07376224008719, 6.317138671875),
      (42.84375132629021, -5.064697265625),
      (48.99463598353408, -4.932861328124999),
      (51.17934297928927, 1.658935546875),
      (51.11041991029261, 2.548828125)
     ]
    ),
]
