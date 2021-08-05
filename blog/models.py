from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class BlogIndexPage(Page):
    """
        Page to list all blog posts
    """

    max_count = 1
    template = "blog/blog-list.html"
    parent_page_types = ["home.HomePage"]

    intro = RichTextField("Intro Text")


    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full")
    ]