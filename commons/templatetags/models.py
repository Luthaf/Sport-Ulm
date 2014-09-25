# -*- coding: utf-8 -*-
from django import template, forms
from django.db import models
register = template.Library()

def get_meta_model_attr(value, attr):
    if isinstance(value, forms.ModelForm):
        u = getattr(value._meta.model._meta, attr)
    elif isinstance(value, models.Model):
        u = getattr(value._meta, attr)
    else:
        raise template.TemplateSyntaxError(
                    "Could not find the model name here, sorry.")
    return u

@register.filter
def model_name(value):
    return get_meta_model_attr(value, "verbose_name")

@register.filter
def plural_model_name(value):
    return get_meta_model_attr(value, "verbose_name_plural")

@register.filter
def english_model_name(value):
    if isinstance(value, forms.ModelForm):
        u = value._meta.model.__name__.lower()
    elif isinstance(value, models.Model):
        u = value.__class__.__name__.lower()
    else:
        raise template.TemplateSyntaxError(
                    "Could not find the model name here, sorry.")
    return u

@register.tag(name="model_url")
def create_url_from_model(parser, token):
    try:
        _, url_name, instance, suffix = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
                    "{} tag three arguments".format(token.contents.split()[0]))
    return UrlFromModel(url_name, instance, suffix)


class UrlFromModel(template.Node):
    '''
    Template tag for rendering custom url names with the form
        {{model_name}}{{suffix}}

    Usage :
        {% model_url url_name model_instance suffix %}
        {% url url_name *args **kwargs %}
    '''
    def __init__(self, url_name, instance, suffix):
        self.url_name = url_name
        self.instance = instance
        self.suffix = suffix

    def render(self, context):
        model = english_model_name(context[self.instance])
        name = model + self.suffix
        if not context.has_key(self.url_name):
            context[self.url_name] = name
        else:
            raise template.TemplateSyntaxError(
                            "Name {url_name} already defined in "
                            "context".format(url_name=self.url_name)
                            )
        return ""
