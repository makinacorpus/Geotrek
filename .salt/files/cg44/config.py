# -*- coding: utf-8 -*-
from .prod import *  # NOQA


# Necessary block of config when maps are not from Geotrek Tilecache :
LEAFLET_CONFIG['SRID'] = 3857
LEAFLET_CONFIG['TILES'] = [
    # *** SCAN ***
    # (gettext_noop('Scan Express Standard'), 'http://gpp3-wxs.ign.fr/hqsgqtv0l9d8a2k2ene94fdq/geoportail/wmts?LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}', '&copy; IGN - GeoPortail'),
    # (gettext_noop('Scan Express Classique'), 'http://gpp3-wxs.ign.fr/hqsgqtv0l9d8a2k2ene94fdq/geoportail/wmts?LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.CLASSIQUE&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}', '&copy; IGN - GeoPortail'),
    (gettext_noop('Scan Express Standard'), 'http://gpp3-wxs.ign.fr/158os34s66xqcvdwzyivp1m0/geoportail/wmts?LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}', '&copy; IGN - GeoPortail'),
    (gettext_noop('Scan Express Classique'), 'http://gpp3-wxs.ign.fr/158os34s66xqcvdwzyivp1m0/geoportail/wmts?LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.CLASSIQUE&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}', '&copy; IGN - GeoPortail'),
    # *** ORTHO ***
    # (gettext_noop('Orthophoto'), 'http://gpp3-wxs.ign.fr/hqsgqtv0l9d8a2k2ene94fdq/geoportail/wmts?LAYER=ORTHOIMAGERY.ORTHOPHOTOS&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}', '&copy; IGN - GeoPortail'),
    (gettext_noop('Orthophoto'), 'http://gpp3-wxs.ign.fr/158os34s66xqcvdwzyivp1m0/geoportail/wmts?LAYER=ORTHOIMAGERY.ORTHOPHOTOS&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}', '&copy; IGN - GeoPortail'),
    # *** Ortho vuduciel CG44 (problème avec les tuiles png transparentes pour le découpage) ***
    # (gettext_noop('Ortho'), 'http://{s}.tiles.cg44.makina-corpus.net/ortho-2012/{z}/{x}/{y}.jpg', {'attribution': 'Source: Département de Loire-Atlantique', 'tms': True}),
]

MOBILE_TILES_URL = LEAFLET_CONFIG['TILES'][0][1]
MOBILE_TILES_GLOBAL_ZOOMS = range(6, 13)

TREKKING_TOPOLOGY_ENABLED = False
TRAIL_MODEL_ENABLED = False

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.remove('geotrek.land')
INSTALLED_APPS.remove('geotrek.maintenance')
INSTALLED_APPS.remove('geotrek.infrastructure')

SPLIT_TREKS_CATEGORIES_BY_PRACTICE = True
HIDE_PUBLISHED_TREKS_IN_TOPOLOGIES = True
ZIP_TOURISTIC_CONTENTS_AS_POI = True

TOURISM_INTERSECTION_MARGIN = 2000

THUMBNAIL_ALIASES['']['print'] = {'size': (800, 600), 'crop': 'smart'}
EXPORT_HEADER_IMAGE_SIZE = {
    'trek': (10.7, 8.025),
    'poi': (10.7, 8.025),
    'touristiccontent': (10.7, 8.025),
    'touristicevent': (10.7, 8.025),
}

MAILALERTSUBJECT = u"Votre signalement sur rando.loire-atlantique.fr"
MAILALERTMESSAGE = u"""Bonjour,

Nous accusons bonne réception de votre message et vous remercions de l’intérêt porté à notre site.

Bien cordialement,

Département de Loire-Atlantique
http://rando.loire-atlantique.fr
http://www.loire-atlantique.fr"""
