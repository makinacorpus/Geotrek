# -*- encoding: utf-8 -*-

from datetime import date
import io
import json
import mock
import os

from django.test import TestCase
from django.core.management import call_command

from geotrek.common.factories import RecordSourceFactory, TargetPortalFactory
from geotrek.common.models import Attachment, FileType
from geotrek.common.tests import TranslationResetMixin
from geotrek.tourism.factories import (TouristicContentCategoryFactory, TouristicContentType1Factory,
                                       TouristicContentType2Factory, TouristicEventTypeFactory)
from geotrek.tourism.models import TouristicContent, TouristicEvent
from geotrek.tourism.parsers import (TouristicContentApidaeParser, EspritParcParser,
                                     TouristicContentTourInSoftParser, TouristicEventTourInSoftParser)


class EauViveParser(TouristicContentApidaeParser):
    category = "Eau vive"
    type1 = ["Type A", "Type B"]
    type2 = []


class EspritParc(EspritParcParser):
    category = "Miels et produits de la ruche"
    type1 = ["Miel", "Pollen", "Gelée royale, propolis et pollen"]
    type2 = ["Hautes Alpes Naturellement", "Bienvenue à la ferme", "Agriculture biologique"]


class HOT28(TouristicContentTourInSoftParser):
    url = "http://wcf.tourinsoft.com/Syndication/cdt28/xxx/Objects"
    source = "CDT 28"
    category = "Où dormir"
    type1 = "Hôtels"
    type2 = "****"
    portal = "Itinérance"


class FMA28(TouristicEventTourInSoftParser):
    url = "http://wcf.tourinsoft.com/Syndication/cdt28/xxx/Objects"
    source = "CDT 28"
    type = "Agenda rando"
    portal = "Itinérance"


class ParserTests(TranslationResetMixin, TestCase):
    @mock.patch('requests.get')
    def test_create_content_apidae(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeContent.json')
            with io.open(filename, 'r', encoding='utf8') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b''
        FileType.objects.create(type="Photographie")
        category = TouristicContentCategoryFactory(label="Eau vive")
        TouristicContentType1Factory(label="Type A")
        TouristicContentType1Factory(label="Type B")
        call_command('import', 'geotrek.tourism.tests.test_parsers.EauViveParser', verbosity=0)
        self.assertEqual(TouristicContent.objects.count(), 1)
        content = TouristicContent.objects.get()
        self.assertEqual(content.eid, "479743")
        self.assertEqual(content.name, "Quey' Raft")
        self.assertEqual(content.description[:27], "Au pied du château médiéval")
        self.assertEqual(content.description_teaser[:24], "Des descentes familiales")
        self.assertEqual(content.contact[:24], "Château Queyras<br>05350")
        self.assertEqual(content.email, "info@queyraft.com")
        self.assertEqual(content.website, "http://www.queyraft.com")
        self.assertEqual(round(content.geom.x), 1000157)
        self.assertEqual(round(content.geom.y), 6413576)
        self.assertEqual(content.practical_info[:39], "<b>Ouverture:</b><br>Du 01/05 au 31/10.")
        self.assertTrue("<br><b>Capacité totale:</b><br>10<br>" in content.practical_info)
        self.assertTrue("><br><b>Services:</b><br>Test, Test2, Test3, Test4<br>" in content.practical_info)
        self.assertTrue(content.published)
        self.assertEqual(content.category, category)
        self.assertQuerysetEqual(
            content.type1.all(),
            ['<TouristicContentType1: Type A>', '<TouristicContentType1: Type B>']
        )
        self.assertQuerysetEqual(content.type2.all(), [])
        self.assertEqual(Attachment.objects.count(), 3)
        self.assertEqual(Attachment.objects.first().content_object, content)

    @mock.patch('requests.get')
    def test_filetype_structure_none(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeContent.json')
            with io.open(filename, 'r', encoding='utf8') as f:
                return json.load(f)

        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        FileType.objects.create(type="Photographie", structure=None)
        TouristicContentCategoryFactory(label="Eau vive")
        TouristicContentType1Factory(label="Type A")
        TouristicContentType1Factory(label="Type B")
        call_command('import', 'geotrek.tourism.tests.test_parsers.EauViveParser', verbosity=0)
        self.assertEqual(TouristicContent.objects.count(), 1)

    @mock.patch('requests.get')
    def test_create_event_apidae(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeEvent.json')
            with io.open(filename, 'r', encoding='utf8') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        FileType.objects.create(type="Photographie")
        self.assertEqual(TouristicEvent.objects.count(), 0)
        output = io.BytesIO()
        call_command('import', 'geotrek.tourism.parsers.TouristicEventApidaeParser', verbosity=2, stdout=output)
        self.assertEqual(TouristicEvent.objects.count(), 1)
        event = TouristicEvent.objects.get()
        self.assertEqual(event.eid, "323154")
        self.assertEqual(event.name, "Cols Réservés 2019 : Montée de Chabre (Laragne)")
        self.assertEqual(event.description[:31], "Le département des Hautes-Alpes")
        self.assertEqual(event.description_teaser[:18], "Une des ascensions")
        self.assertEqual(event.contact[:21], "Châteauneuf de Chabre")
        self.assertEqual(event.email, "LeGrandTim@mail.fr")
        self.assertEqual(event.website, "http://www.LeGrandTim.fr")
        self.assertEqual(round(event.geom.x), 922920)
        self.assertEqual(round(event.geom.y), 6357103)
        self.assertEqual(event.practical_info[:38], "<b>Ouverture:</b><br>Mardi 6 août 2019")
        self.assertIn("><br><b>Services:</b><br>Le plus grand des services, Un autre grand service<br>",
                      event.practical_info)
        self.assertTrue(event.published)
        self.assertEqual(event.organizer, 'Toto')
        self.assertEqual(str(event.meeting_time), '09:00:00')
        self.assertEqual(event.type.type, 'Sports')
        self.assertQuerysetEqual(
            event.themes.all(),
            ['<Theme: Cyclisme>', '<Theme: Sports cyclistes>']
        )
        self.assertEqual(Attachment.objects.count(), 3)

    @mock.patch('requests.get')
    def test_create_esprit(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'espritparc.json')
            with io.open(filename, 'rb') as f:
                return json.load(f)

        filename = os.path.join(os.path.dirname(__file__), 'data', 'espritparc.json')
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b''
        FileType.objects.create(type="Photographie")
        category = TouristicContentCategoryFactory(label="Miels et produits de la ruche")
        TouristicContentType1Factory(label="Miel", category=category)
        TouristicContentType1Factory(label="Gelée royale, propolis et pollen", category=category)
        TouristicContentType1Factory(label="Pollen", category=category)
        TouristicContentType1Factory(label="Cire", category=category)
        TouristicContentType2Factory(label="Hautes Alpes Naturellement", category=category)
        TouristicContentType2Factory(label="Bienvenue à la ferme", category=category)
        TouristicContentType2Factory(label="Agriculture biologique", category=category)
        call_command('import', 'geotrek.tourism.tests.test_parsers.EspritParc', filename, verbosity=0)
        self.assertEqual(TouristicContent.objects.count(), 24)
        content = TouristicContent.objects.all()
        eid = [
            "PDT44", "PDT46", "PDT47", "PDT48", "PDT51", "PDT52", "PDT53", "PDT93", "PDT94", "PDT95",
            "PDT186", "PDT260", "PDT261", "PDT842", "PDT471", "PDT503", "PDT504", "PDT505", "PDT506",
            "PDT795", "PDT797", "PDT799", "PDT836", "PDT837"
        ]
        name = [
            "miel de montagne", "miel de haute montagne", "miel de printemps d'embrun",
            "gel\xe9e royale de montagne", "pollen de montagne", "miel de haute montagne bio", "miel de for\xeat",
            "miel de pissenlit", "miel de haute montagne du valgaudemar", "pollen frais de montagne",
            "miel de printemps de l'embrunais", "pollen de fleurs de montagne", "pain de cire",
            "miel de montagne toutes fleurs", "miel cuv\xe9e sp\xe9ciale d'ancelle", "miel des ecrins"

        ]
        for one in content:
            self.assertIn(one.eid, eid)
            self.assertIn(one.name.lower(), name)
            self.assertEqual(one.category, category)

    @mock.patch('requests.get')
    def test_create_content_tourinsoft(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'tourinsoftContent.json')
            with io.open(filename, 'r', encoding='utf8') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        FileType.objects.create(type="Photographie")
        category = TouristicContentCategoryFactory(label="Où dormir")
        source = RecordSourceFactory(name="CDT 28")
        portal = TargetPortalFactory(name="Itinérance")
        call_command('import', 'geotrek.tourism.tests.test_parsers.HOT28', verbosity=0)
        self.assertEqual(TouristicContent.objects.count(), 1)
        content = TouristicContent.objects.get()
        self.assertEqual(content.eid, "HOTCEN0280010001")
        self.assertEqual(content.name, "Hôtel du Perche")
        self.assertEqual(content.description[:27], "")
        self.assertEqual(content.description_teaser[:26], "A deux pas du centre ville")
        self.assertEqual(content.contact[:73], "<strong>Adresse :</strong><br>Rue de la Bruyère<br>28400 NOGENT-LE-ROTRO")
        self.assertEqual(content.email, "hotelduperche@brithotel.fr")
        self.assertEqual(content.website, "http://www.hotel-du-perche.com")
        self.assertEqual(round(content.geom.x), 537329)
        self.assertEqual(round(content.geom.y), 6805504)
        self.assertEqual(content.practical_info[:49], "<strong>Langues parlées :</strong><br>Anglais<br>")
        self.assertIn("du 01/01/2019 au 21/07/2019", content.practical_info)
        self.assertIn("<strong>Équipements :</strong><br>Bar<br>Parking<br>", content.practical_info)
        self.assertTrue(content.published)
        self.assertEqual(content.source.get(), source)
        self.assertEqual(content.portal.get(), portal)
        self.assertEqual(content.category, category)
        self.assertEqual(content.type1.get().label, "Hôtels")
        self.assertEqual(content.type2.get().label, "****")
        self.assertEqual(Attachment.objects.count(), 3)
        self.assertEqual(Attachment.objects.first().content_object, content)

    @mock.patch('requests.get')
    def test_create_event_tourinsoft(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'tourinsoftEvent.json')
            with io.open(filename, 'r', encoding='utf8') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        FileType.objects.create(type="Photographie")
        type = TouristicEventTypeFactory(type="Agenda rando")
        source = RecordSourceFactory(name="CDT 28")
        portal = TargetPortalFactory(name="Itinérance")
        call_command('import', 'geotrek.tourism.tests.test_parsers.FMA28', verbosity=0)
        self.assertEqual(TouristicEvent.objects.count(), 1)
        event = TouristicEvent.objects.get()
        self.assertEqual(event.eid, "FMACEN0280060359")
        self.assertEqual(event.name, "Moto cross de Bro")
        self.assertEqual(event.description, "")
        self.assertEqual(event.description_teaser, "")
        self.assertEqual(event.contact[:69], "<strong>Adresse :</strong><br>Circuit des Tonnes<br>28160 DAMPIERRE-S")
        self.assertEqual(event.email, "moto-club.brou@orange.fr")
        self.assertEqual(event.website, "http://www.mxbrou.com")
        self.assertEqual(round(event.geom.x), 559796)
        self.assertEqual(round(event.geom.y), 6791765)
        self.assertEqual(event.practical_info[:61], "<strong>Langues parlées :</strong><br>Anglais<br>Allemand<br>")
        self.assertIn("<strong>Équipements :</strong><br>Restauration sur place<br>Sanitaires", event.practical_info)
        self.assertTrue(event.published)
        self.assertEqual(event.source.get(), source)
        self.assertEqual(event.portal.get(), portal)
        self.assertEqual(event.type, type)
        self.assertEqual(Attachment.objects.count(), 9)
        self.assertEqual(Attachment.objects.first().content_object, event)
        self.assertEqual(event.begin_date, date(2100, 6, 1))
        self.assertEqual(event.end_date, date(2100, 6, 2))
