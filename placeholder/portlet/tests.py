# coding: utf-8

from __future__ import unicode_literals

from django.test import TestCase
from django import forms

from .utils import declare_form, extract_form_declaration


class EasyPortletTestCase(TestCase):

    def setUp(self):
        self.data_yaml = {
            'title': {'CharField': {'required': True}},
            'url': {'URLField': {'required': False}},
            'text': {'CharField': {'required': True, 'widget': "Textarea"}},
        }
        self.data_helper = [
            {'title': {'CharField': {'required': True}}},
            {'url': {'URLField': {'required': False}}},
            {'text': {'CharField': {'required': True, 'widget': "Textarea"}}},
        ]
        self.portlet_yaml_source = u"""

<!--PORTLET:YAML:

portlet:
    title:
        CharField:
            required: true
    url:
        URLField:
            required: false
    text:
        CharField:
            required: true
            widget: Textarea

-->
<div></div>

        """
        self.portlet_helper_source = u"""

<!--PORTLET:HELPER:Title,UrlOptional,Text-->

<div></div>

        """

    def test_extract_form_declaration(self):
        self.assertEqual(
            extract_form_declaration(self.portlet_yaml_source),
            {'portlet': self.data_yaml})

        self.assertEqual(
            extract_form_declaration(self.portlet_helper_source),
            {'portlet': self.data_helper})

        self.assertEqual(
            extract_form_declaration("<div></div>"),
            {})

    def test_declare_form_yaml(self):
        form = declare_form(self.data_yaml)
        self.assertIn('title', form.base_fields)
        self.assertEquals(type(form.base_fields['title']), forms.CharField)
        self.assertEquals(form.base_fields['title'].required, True)
        self.assertIn('url', form.base_fields)
        self.assertEquals(type(form.base_fields['url']), forms.URLField)
        self.assertEquals(form.base_fields['url'].required, False)
        self.assertIn('text', form.base_fields)
        self.assertEquals(type(form.base_fields['text']), forms.CharField)
        self.assertEquals(
            type(form.base_fields['text'].widget), forms.Textarea)
        self.assertEquals(form.base_fields['url'].required, False)

    def test_declare_form_helper(self):
        form = declare_form(self.data_helper)
        self.assertIn('title', form.base_fields)
        self.assertEquals(type(form.base_fields['title']), forms.CharField)
        self.assertEquals(form.base_fields['title'].required, True)
        self.assertIn('url', form.base_fields)
        self.assertEquals(type(form.base_fields['url']), forms.URLField)
        self.assertEquals(form.base_fields['url'].required, False)
        self.assertIn('text', form.base_fields)
        self.assertEquals(type(form.base_fields['text']), forms.CharField)
        self.assertEquals(
            type(form.base_fields['text'].widget), forms.Textarea)
        self.assertEquals(form.base_fields['url'].required, False)
