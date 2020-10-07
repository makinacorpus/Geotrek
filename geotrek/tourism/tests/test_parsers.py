from datetime import date
import io
import json
import requests
from unittest import mock
import os

from django.test import TestCase, override_settings
from django.core.management import call_command
from django.core.management.base import CommandError

from geotrek.common.factories import RecordSourceFactory, TargetPortalFactory
from geotrek.common.models import Attachment, FileType
from geotrek.common.tests import TranslationResetMixin
from geotrek.tourism.factories import (TouristicContentCategoryFactory, TouristicContentType1Factory,
                                       TouristicContentType2Factory, TouristicEventTypeFactory)
from geotrek.tourism.models import TouristicContent, TouristicEvent
from geotrek.tourism.parsers import (TouristicContentApidaeParser, TouristicEventApidaeParser, EspritParcParser,
                                     TouristicContentTourInSoftParserV3, TouristicContentTourInSoftParser,
                                     TouristicEventTourInSoftParser)


class ApidaeConstantFieldContentParser(TouristicContentApidaeParser):
    category = "Constant Content"
    type1 = ["Type1 1", "Type1 2"]
    type2 = ["Type2 1", "Type2 2"]
    themes = ["Theme 1", "Theme 2"]
    source = ["Source 1", "Source 2"]
    portal = ["Portal 1", "Portal 2"]
    field_options = {'themes': {'create': True},
                     'category': {'create': True},
                     'type1': {'create': True, 'fk': 'category'},
                     'type2': {'create': True, 'fk': 'category'}}


class ApidaeConstantFieldEventParser(TouristicEventApidaeParser):
    type = "Constant Event"
    themes = ["Theme 1", "Theme 2"]
    source = ["Source 1", "Source 2"]
    portal = ["Portal 1", "Portal 2"]


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


class HOT28v3(TouristicContentTourInSoftParserV3):
    url = "http://wcf.tourinsoft.com/Syndication/3.0/cdt28/xxx/Objects"
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
    def test_create_content_apidae_failed(self, mocked):
        mocked.return_value.status_code = 404
        FileType.objects.create(type="Photographie")
        TouristicContentCategoryFactory(label="Eau vive")
        TouristicContentType1Factory(label="Type A")
        TouristicContentType1Factory(label="Type B")
        with self.assertRaises(CommandError):
            call_command('import', 'geotrek.tourism.tests.test_parsers.EauViveParser', verbosity=2)

    @mock.patch('requests.get')
    def test_create_content_espritparc_failed(self, mocked):
        mocked.return_value.status_code = 404
        FileType.objects.create(type="Photographie")
        category = TouristicContentCategoryFactory(label="Miels et produits de la ruche")
        TouristicContentType1Factory(label="Miel", category=category)
        TouristicContentType1Factory(label="Gelée royale, propolis et pollen", category=category)
        TouristicContentType1Factory(label="Pollen", category=category)
        TouristicContentType1Factory(label="Cire", category=category)
        TouristicContentType2Factory(label="Hautes Alpes Naturellement", category=category)
        TouristicContentType2Factory(label="Bienvenue à la ferme", category=category)
        TouristicContentType2Factory(label="Agriculture biologique", category=category)
        with self.assertRaises(CommandError):
            call_command('import', 'geotrek.tourism.tests.test_parsers.EauViveParser', verbosity=2)

    @mock.patch('requests.get')
    @override_settings(PARSER_RETRY_SLEEP_TIME=0)
    @mock.patch('geotrek.common.parsers.AttachmentParserMixin.download_attachments', False)
    def test_create_content_espritparc_retry(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeContent.json')
            with open(filename, 'r') as f:
                return json.load(f)

        def side_effect(url, params, auth, code):
            response = requests.Response()
            response.status_code = code
            response.url = url
            if code == 200:
                response.json = mocked_json
            return response

        mocked.side_effect = [side_effect(EauViveParser.url, None, None, 503),
                              side_effect(EauViveParser.url, None, None, 503),
                              side_effect(EauViveParser.url, None, None, 200)]

        FileType.objects.create(type="Photographie")
        TouristicContentCategoryFactory(label="Eau vive")
        TouristicContentType1Factory(label="Type A")
        TouristicContentType1Factory(label="Type B")
        call_command('import', 'geotrek.tourism.tests.test_parsers.EauViveParser')
        self.assertEqual(TouristicContent.objects.count(), 1)

    @mock.patch('requests.get')
    @override_settings(PARSER_RETRY_SLEEP_TIME=0)
    def test_create_content_espritparc_retry_fail(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeContent.json')
            with open(filename, 'r') as f:
                return json.load(f)

        def side_effect(url, allow_redirects, params):
            response = requests.Response()
            response.status_code = 503
            response.url = url
            return response

        mocked.side_effect = side_effect

        FileType.objects.create(type="Photographie")
        TouristicContentCategoryFactory(label="Eau vive")
        TouristicContentType1Factory(label="Type A")
        TouristicContentType1Factory(label="Type B")
        with self.assertRaisesRegex(CommandError, "Failed to download %s. HTTP status code 503" % EauViveParser.url):
            call_command('import', 'geotrek.tourism.tests.test_parsers.EauViveParser')

    @mock.patch('requests.get')
    def test_create_content_espritparc_not_fail_type1_does_not_exist(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'espritparc.json')
            with open(filename, 'r') as f:
                return json.load(f)

        filename = os.path.join(os.path.dirname(__file__), 'data', 'espritparc.json')
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        category = TouristicContentCategoryFactory(label="Miels et produits de la ruche")
        TouristicContentType2Factory(label="Hautes Alpes Naturellement", category=category)
        TouristicContentType2Factory(label="Bienvenue à la ferme", category=category)
        TouristicContentType2Factory(label="Agriculture biologique", category=category)
        output = io.StringIO()
        call_command('import', 'geotrek.tourism.tests.test_parsers.EspritParc', filename, verbosity=2, stdout=output)
        self.assertIn("Type 1 'Miel' does not exist for category 'Miels et produits de la ruche'. Please add it,",
                      output.getvalue())

    @mock.patch('requests.get')
    def test_create_content_espritparc_not_fail_type2_does_not_exist(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'espritparc.json')
            with open(filename, 'r') as f:
                return json.load(f)

        filename = os.path.join(os.path.dirname(__file__), 'data', 'espritparc.json')
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        category = TouristicContentCategoryFactory(label="Miels et produits de la ruche")
        TouristicContentType1Factory(label="Miel", category=category)
        TouristicContentType1Factory(label="Gelée royale, propolis et pollen", category=category)
        TouristicContentType1Factory(label="Pollen", category=category)
        TouristicContentType1Factory(label="Cire", category=category)
        output = io.StringIO()
        call_command('import', 'geotrek.tourism.tests.test_parsers.EspritParc', filename, verbosity=2, stdout=output)
        self.assertIn("Type 2 'Bienvenue à la ferme' does not exist for category 'Miels et produits de la ruche'. Please add it",
                      output.getvalue())

    @mock.patch('requests.get')
    def test_create_content_apidae(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeContent.json')
            with open(filename, 'r') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        category = TouristicContentCategoryFactory(label="Eau vive")
        TouristicContentType1Factory(label="Type A")
        TouristicContentType1Factory(label="Type B")
        call_command('import', 'geotrek.tourism.tests.test_parsers.EauViveParser', verbosity=0)
        self.assertEqual(TouristicContent.objects.count(), 1)
        content = TouristicContent.objects.get()
        self.assertEqual(content.eid, "479743")
        self.assertEqual(content.name_en, "Test EN")
        self.assertEqual(content.name_es, "Test ES")
        self.assertEqual(content.name_fr, "Quey' Raft")
        self.assertEqual(content.description_fr[:27], "Au pied du château médiéval")
        self.assertEqual(content.description_en, "Descriptif Détaillé EN")
        self.assertEqual(content.description_teaser_fr[:24], "Des descentes familiales")
        self.assertEqual(content.description_teaser_es, "Descriptif Court ES")
        self.assertEqual(content.description_teaser_en, "Descriptif Court EN")
        self.assertEqual(content.description_teaser_it, "Descriptif Court IT")
        self.assertEqual(content.contact[:24], "Château Queyras<br>05350")
        self.assertEqual(content.email, "info@queyraft.com")
        self.assertEqual(content.website, "http://www.queyraft.com")
        self.assertEqual(round(content.geom.x), 1000157)
        self.assertEqual(round(content.geom.y), 6413576)
        self.assertEqual(content.practical_info_fr[:39], "<b>Ouverture:</b><br>Du 01/05 au 31/10.")
        self.assertTrue("<br><b>Capacité totale:</b><br>10<br>" in content.practical_info_fr)
        self.assertTrue("><br><b>Services:</b><br>Test, Test2, Test3, Test4<br>" in content.practical_info_fr)
        self.assertIn("<b>Tarifs:</b><br>A partir de 30 € par personne<br>", content.practical_info_fr)
        self.assertIn("<b>Accès:</b><br>TestFr<br>", content.practical_info_fr)
        self.assertTrue("><br><b>Services:</b><br>Test EN, Test2 EN, Test3 EN, Test4 EN<br>"
                        in content.practical_info_en)
        self.assertTrue("><br><b>Services:</b><br>Test, Test2, Test3, Test4<br>" in content.practical_info_fr)
        self.assertIn("<b>Tarifs:</b><br>A partir de 30 € par personne<br>", content.practical_info_fr)
        self.assertIn("<b>Prices:</b><br>From 30 € per person<br>", content.practical_info_en)
        self.assertIn("<b>Accès:</b><br>TestFr<br>", content.practical_info_fr)
        self.assertIn("<b>Access:</b><br>TestEn<br>", content.practical_info_en)
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
            with open(filename, 'r') as f:
                return json.load(f)

        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie", structure=None)
        TouristicContentCategoryFactory(label="Eau vive")
        TouristicContentType1Factory(label="Type A")
        TouristicContentType1Factory(label="Type B")
        call_command('import', 'geotrek.tourism.tests.test_parsers.EauViveParser', verbosity=0)
        self.assertEqual(TouristicContent.objects.count(), 1)

    @mock.patch('requests.get')
    def test_no_event_apidae(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeNoEvent.json')
            with open(filename, 'r') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        output = io.StringIO()
        call_command('import', 'geotrek.tourism.parsers.TouristicEventApidaeParser', verbosity=2, stdout=output)
        self.assertEqual(TouristicEvent.objects.count(), 0)

    @mock.patch('requests.get')
    def test_create_event_apidae(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeEventFr.json')
            with open(filename, 'r') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        self.assertEqual(TouristicEvent.objects.count(), 0)
        output = io.StringIO()
        call_command('import', 'geotrek.tourism.parsers.TouristicEventApidaeParser', verbosity=2, stdout=output)
        self.assertEqual(TouristicEvent.objects.count(), 1)
        event = TouristicEvent.objects.get()
        self.assertEqual(event.eid, "323154")
        self.assertEqual(event.name_fr, "Cols Réservés 2019 : Montée de Chabre (Laragne)")
        self.assertEqual(event.name, '')
        self.assertEqual(event.description, '')
        self.assertEqual(event.description_fr[:31], "Le département des Hautes-Alpes")
        self.assertEqual(event.description_teaser_fr[:18], "Une des ascensions")
        self.assertEqual(event.description_teaser_en, None)
        self.assertEqual(event.description_teaser, '')
        self.assertEqual(event.contact[:21], "Châteauneuf de Chabre")
        self.assertEqual(event.email, "LeGrandTim@mail.fr")
        self.assertEqual(event.website, "http://www.LeGrandTim.fr")
        self.assertEqual(round(event.geom.x), 922920)
        self.assertEqual(round(event.geom.y), 6357103)
        self.assertEqual(event.practical_info_fr[:38], "<b>Ouverture:</b><br>Mardi 6 août 2019")
        self.assertIn("><br><b>Services:</b><br>Le plus grand des services, Un autre grand service<br>",
                      event.practical_info_fr)
        self.assertIn("<b>Ouverture:</b><br>Mardi 6 août 2019 de 9h à midi.<br>", event.practical_info_fr)
        self.assertIn("<b>Langues Parlées:</b><br>Français<br>", event.practical_info_fr)
        self.assertIn("<b>Accès:</b><br>TestFr<br>", event.practical_info_fr)
        self.assertIn("><br><b>Services:</b><br>Le plus grand des services, Un autre grand service<br>",
                      event.practical_info_fr)
        self.assertIn("><br><b>Services:</b><br>Le plus grand des services, Un autre grand service<br>",
                      event.practical_info_fr)
        self.assertIn("<b>Ouverture:</b><br>Mardi 6 août 2019 de 9h à midi.<br>", event.practical_info_fr)
        self.assertIn("<b>Langues Parlées:</b><br>Français<br>", event.practical_info_fr)
        self.assertIn("<b>Accès:</b><br>TestFr<br>", event.practical_info_fr)
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
    def test_create_event_apidae_empty_languagefr(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeEventEn.json')
            with open(filename, 'r') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        self.assertEqual(TouristicEvent.objects.count(), 0)
        output = io.StringIO()
        call_command('import', 'geotrek.tourism.parsers.TouristicEventApidaeParser', verbosity=2, stdout=output)
        self.assertEqual(TouristicEvent.objects.count(), 1)
        event = TouristicEvent.objects.get()
        self.assertEqual(event.eid, "323154")
        self.assertEqual(event.name_fr, None)
        self.assertEqual(event.name, "Nom EN")
        self.assertEqual(event.name_en, "Nom EN")
        self.assertEqual(event.description_en, "Descriptif Detaillé EN")
        self.assertEqual(event.description, "Descriptif Detaillé EN")
        self.assertEqual(event.description_fr, None)
        self.assertEqual(event.description_teaser_fr, None)
        self.assertEqual(event.description_teaser_en, "Descriptif Court EN")
        self.assertEqual(event.description_teaser, "Descriptif Court EN")
        self.assertEqual(event.contact[:21], "Châteauneuf de Chabre")
        self.assertEqual(event.email, "LeGrandTim@mail.fr")
        self.assertEqual(event.website, "http://www.LeGrandTim.fr")
        self.assertEqual(round(event.geom.x), 922920)
        self.assertEqual(round(event.geom.y), 6357103)
        self.assertNotIn("><br><b>Services:</b><br>Le plus grand des services, Un autre grand service<br>",
                         event.practical_info_fr)
        self.assertNotIn("<b>Langues Parlées:</b><br>Français<br>", event.practical_info_fr)

        self.assertIn("><br><b>Services:</b><br>English Service, Other Service<br>",
                      event.practical_info_en)
        self.assertIn("<b>Openning:</b><br>Tuesday, August 6, 2019 from 9am to noon.<br>", event.practical_info_en)
        self.assertIn("<b>Spoken languages:</b><br>French<br><br>", event.practical_info_en)
        self.assertIn("<b>Access:</b><br>TestEn<br>", event.practical_info_en)
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
    def test_create_event_apidae_constant_fields(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeEventFr.json')
            with open(filename, 'r') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        TargetPortalFactory(name='Portal 1')
        TargetPortalFactory(name='Portal 2')
        RecordSourceFactory(name='Source 1')
        RecordSourceFactory(name='Source 2')
        self.assertEqual(TouristicEvent.objects.count(), 0)
        output = io.StringIO()
        call_command('import', 'geotrek.tourism.tests.test_parsers.ApidaeConstantFieldEventParser', verbosity=2,
                     stdout=output)
        self.assertEqual(TouristicEvent.objects.count(), 1)
        event = TouristicEvent.objects.get()
        self.assertEqual(str(event.type), "Constant Event")
        self.assertQuerysetEqual(event.themes.all(), ["Theme 1", "Theme 2"], transform=str)
        self.assertQuerysetEqual(event.source.all(), ["Source 1", "Source 2"], transform=str)
        self.assertQuerysetEqual(event.portal.all(), ["Portal 1", "Portal 2"], transform=str)

    @mock.patch('requests.get')
    def test_create_content_apidae_constant_fields(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'apidaeContent.json')
            with open(filename, 'r') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        TargetPortalFactory(name='Portal 1')
        TargetPortalFactory(name='Portal 2')
        RecordSourceFactory(name='Source 1')
        RecordSourceFactory(name='Source 2')
        self.assertEqual(TouristicContent.objects.count(), 0)
        output = io.StringIO()
        call_command('import', 'geotrek.tourism.tests.test_parsers.ApidaeConstantFieldContentParser', verbosity=2,
                     stdout=output)
        self.assertEqual(TouristicContent.objects.count(), 1)
        content = TouristicContent.objects.get()
        self.assertEqual(str(content.category), "Constant Content")
        self.assertQuerysetEqual(content.type1.all(), ["Type1 1", "Type1 2"], transform=str)
        self.assertQuerysetEqual(content.type2.all(), ["Type2 1", "Type2 2"], transform=str)
        self.assertQuerysetEqual(content.themes.all(), ["Theme 1", "Theme 2"], transform=str)
        self.assertQuerysetEqual(content.source.all(), ["Source 1", "Source 2"], transform=str)
        self.assertQuerysetEqual(content.portal.all(), ["Portal 1", "Portal 2"], transform=str)

    @mock.patch('requests.get')
    def test_create_esprit(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'espritparc.json')
            with open(filename, 'r') as f:
                return json.load(f)

        filename = os.path.join(os.path.dirname(__file__), 'data', 'espritparc.json')
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
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
    def test_create_content_tourinsoft_v2(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'tourinsoftContent.json')
            with open(filename, 'r') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
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
        self.assertEqual(content.contact[:73], "<strong>Adresse :</strong><br>Rue de la Bruyère<br>28400 NOGENT-LE-ROTROU")
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
    def test_create_content_tourinsoft_v3(self, mocked):
        def mocked_json():
            filename = os.path.join(os.path.dirname(__file__), 'data', 'tourinsoftContentV3.json')
            with open(filename, 'r') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        category = TouristicContentCategoryFactory(label="Où dormir")
        source = RecordSourceFactory(name="CDT 28")
        portal = TargetPortalFactory(name="Itinérance")
        call_command('import', 'geotrek.tourism.tests.test_parsers.HOT28v3', verbosity=0)
        self.assertEqual(TouristicContent.objects.count(), 1)
        content = TouristicContent.objects.get()
        self.assertEqual(content.eid, "HOTCEN0280010001")
        self.assertEqual(content.name, "Hôtel du Perche")
        self.assertEqual(content.description[:27], "")
        self.assertEqual(content.description_teaser[:26], "A deux pas du centre ville")
        self.assertEqual(content.contact[:73], "<strong>Adresse :</strong><br>Rue de la Bruyère<br>28400 NOGENT-LE-ROTROU")
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
            with open(filename, 'r') as f:
                return json.load(f)
        mocked.return_value.status_code = 200
        mocked.return_value.json = mocked_json
        mocked.return_value.content = b'Fake image'
        FileType.objects.create(type="Photographie")
        type = TouristicEventTypeFactory(type="Agenda rando")
        source = RecordSourceFactory(name="CDT 28")
        portal = TargetPortalFactory(name="Itinérance")
        call_command('import', 'geotrek.tourism.tests.test_parsers.FMA28', verbosity=0)
        self.assertEqual(TouristicEvent.objects.count(), 1)
        event = TouristicEvent.objects.get()
        self.assertEqual(event.eid, "FMACEN0280060359")
        self.assertEqual(event.name, "Moto cross de Brou")
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
