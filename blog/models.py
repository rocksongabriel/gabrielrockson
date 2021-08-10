from django.db import models
from django.db.models.fields import Field

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from django.utils.translation import gettext_lazy as _
from wagtail.snippets.models import register_snippet
from django.utils import timezone
from django.utils.text import slugify


# ------------------------------------------------------------- SNIPPETS ----------------------------------------------------------------
@register_snippet
class BlogAuthor(models.Model):
    """Snippet for a Blog Author"""

    full_name = models.CharField(_("Full Name"), max_length=50, null=False, blank=False, help_text="Enter the full name of the author")
    avatar = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        help_text="Upload an image of the author",
        related_name="+"
    )
    description = RichTextField(_("Description of Author"), help_text="Enter a brief description about the author")
    date_joined = models.DateField(_("Date Joined"), help_text="Which date did this author join the team?", default=timezone.now)
    twitter = models.URLField("Twitter Handle", help_text="Input the the link to the author's twitter handle", null=False, blank=False)
    email = models.EmailField("Email Address", help_text="Enter the email address of the author", max_length=500)


    panels = [
        FieldPanel("full_name"),
        ImageChooserPanel("avatar"),
        FieldPanel("description"),
        FieldPanel("date_joined"),
        FieldRowPanel([
            FieldPanel("twitter"),
            FieldPanel("email")
        ])
    ]

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


@register_snippet
class BlogCategory(models.Model):
    """Snippet for a Blog Category"""

    name = models.CharField(_("Name of Category"), max_length=100, help_text="Enter the name of the Category", null=False, blank=False)
    slug = models.SlugField(_("Slug"), max_length=100, null=False, blank=False)

    panels = [
        FieldPanel("name")
    ]

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) # slugify the name field
        return super().save(kwargs)
    
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"


# ----------------------------------------------- PAGES ------------------------------------------------------------------------
class BlogIndexPage(Page):
    """
        Page to list all blog posts
    """

    max_count = 1
    template = "blog/blog-list.html"
    parent_page_types = ["home.HomePage"]
    subpages_types = ["blog.BlogDetailPage"]

    intro = RichTextField("Intro Text")


    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["categories"] = BlogCategory.objects.all()
        return context

# class BlogDetailPage(Page):

#     template = "blog/blog-detail.html"
#     parent_page_types = ["blog.BlogIndexPage"]

#     """
#         - blog title
#         - featured_image
#         - author *
#         - date published
#         - upvotes *
#         - times read *
#         - read time *
#         - blog category
#         - blog tags
#         - programming quote
#         - main content
#             - titles
#             - paragraphs
#             - code blocks
#             - images


#     """
#     image = models.ForeignKey(
#         _("Featured Image"),
#         "wagtailimages.Image",
#         null=False,
#         blank=False,
#         related_name="+",
#         help_text="Select an image to use on the post's page"
#     )
#     date_published = models.DateTimeField(auto_now_add=True)
#     quote = models.TextField(_("A Programming Quote"), help_text="Enter some programming quote", blank=False, null=False)



#     content_panels = Page.content_panels + [
#         ImageChooserPanel("image"),
#         FieldPanel("quote"),
#     ]