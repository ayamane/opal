"""
Tests for our modal/form helpers
"""
from django.template import Template, Context
from django.test import TestCase

from opal.templatetags.forms import input, select, textarea, process_steps

class TextareaTest(TestCase):
    def setUp(self):
        self.template = Template('{% load forms %}{% textarea label="hai" model="bai"%}')

    def test_textarea(self):
        rendered = self.template.render(Context({}))
        self.assertIn('ng-model="bai"', rendered)
        self.assertIn('hai', rendered)


class InputTest(TestCase):

    def test_input(self):
        template = Template('{% load forms %}{% input label="hai" model="bai"%}')
        rendered = template.render(Context({}))
        self.assertIn('ng-model="bai"', rendered)
        self.assertIn('hai', rendered)

    def test_hide(self):
        tpl = Template('{% load forms %}{% input label="hai" model="bai" hide="status=\'reloading\'"%}')
        self.assertIn('ng-hide="status=\'reloading\'"', tpl.render(Context({})))

    def test_show(self):
        tpl = Template('{% load forms %}{% input label="hai" model="bai" show="status=\'loaded\'"%}')
        self.assertIn('ng-show="status=\'loaded\'"', tpl.render(Context({})))

    def test_show_hide(self):
        tpl = Template('{% load forms %}{% input label="hai" model="bai" hide="status=\'reloading\'" show="status=\'loaded\'" %}')
        self.assertIn('ng-show="status=\'loaded\'"', tpl.render(Context({})))
        self.assertIn('ng-hide="status=\'reloading\'"', tpl.render(Context({})))

    def test_fa_icon(self):
        tpl = Template('{% load forms %}{% input label="hai" model="bai" icon="fa-eye"%}')
        self.assertIn('<i class="fa fa-eye"></i>', tpl.render(Context({})))

    def test_glyph_icon(self):
        tpl = Template('{% load forms %}{% input label="hai" model="bai" icon="glyphicon-boat"%}')
        self.assertIn('<i class="glyphicon glyphicon-boat"></i>', tpl.render(Context({})))

    def test_unknown_icon(self):
        tpl = Template('{% load forms %}{% input label="hai" model="bai" icon="myicon"%}')
        self.assertIn('<i class="myicon"></i>', tpl.render(Context({})))

    def test_disabled(self):
        tpl = Template('{% load forms %}{% input label="hai" model="bai" disabled="status=\'reloading\'"%}')
        self.assertIn('ng-disabled="status=\'reloading\'"', tpl.render(Context({})))

    def test_required_no_formname(self):
        tpl = Template('{% load forms %}{% input label="hai" model="bai" required=True%}')
        with self.assertRaises(ValueError):
            tpl.render(Context({}))


class CheckboxTestCase(TestCase):

    def test_checkbox(self):
        template = Template('{% load forms %}{% checkbox label="hai" model="bai"%}')
        rendered = template.render(Context({}))
        self.assertIn('ng-model="bai"', rendered)
        self.assertIn('hai', rendered)


class DatepickerTestCase(TestCase):

    def test_datepicker(self):
        template = Template('{% load forms %}{% datepicker label="hai" model="bai" mindate="2013-12-22" %}')
        rendered = template.render(Context({}))
        self.assertIn('ng-model="bai"', rendered)
        self.assertIn('hai', rendered)
        self.assertIn('data-min-date="2013-12-22"', rendered)


class RadioTestCase(TestCase):

    def test_radio(self):
        template = Template('{% load forms %}{% radio label="hai" model="bai"%}')
        rendered = template.render(Context({}))
        self.assertIn('ng-model="bai"', rendered)
        self.assertIn('hai', rendered)


class SelectTestCase(TestCase):

    def test_select(self):
        template = Template('{% load forms %}{% select label="hai" model="bai" %}')
        rendered = template.render(Context({}))
        self.assertIn('ng-model="bai"', rendered)

        # remove white space
        cleaned = "".join([i.strip() for i in rendered.split("\n") if i.strip()])
        self.assertIn('<label class="control-label col-sm-3">hai</label>', cleaned)

    def test_select_lookuplist(self):
        template = Template('{% load forms %}{% select label="hai" model="bai" lookuplist="[1,2,3]" %}')
        rendered = template.render(Context({}))
        self.assertIn('ng-model="bai"', rendered)

        # remove white space
        cleaned = "".join([i.strip() for i in rendered.split("\n") if i.strip()])
        self.assertIn('<label class="control-label col-sm-3">hai</label>', cleaned)

    def test_required_no_formname(self):
        tpl = Template('{% load forms %}{% select label="hai" model="bai" required=True %}')
        with self.assertRaises(ValueError):
            tpl.render(Context({}))


class IconTestCase(TestCase):

    def test_fa_icon(self):
        tpl = Template('{% load forms %}{% icon "fa-eye" %}')
        self.assertIn('<i class="fa fa-eye"></i>', tpl.render(Context({})))

    def test_glyph_icon(self):
        tpl = Template('{% load forms %}{% icon "glyphicon-boat" %}')
        self.assertIn('<i class="glyphicon glyphicon-boat"></i>', tpl.render(Context({})))


class ProcessStepsTestCase(TestCase):

    def test_process_steps(self):
        ctx = process_steps(
            process_steps=1,
            complete=False,
            disabled=False,
            active=True,
            show_titles=True
        )
        expected = dict(
            process_steps=1,
            complete=False,
            disabled=False,
            active=True,
            show_index=False,
            show_titles=True
        )
        self.assertEqual(expected, ctx)
