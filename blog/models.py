from django.db import models
from django.db.models.fields import Field
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel, StreamFieldPanel)
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock
# from wagtailcodeblock.blocks import CodeBlock
from .blocks import CodeBlock


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

        posts = BlogDetailPage.objects.child_of(self).live()

        # Filter the blog posts by tags
        tag = request.GET.get("tag")
        # Filter by categories
        category = request.GET.get("category")

        if tag:
            context["tag"] = tag
            posts = BlogDetailPage.objects.filter(tags__name=tag)
        elif category:
            context["category"] = category
            posts = BlogDetailPage.objects.filter(category__name=category)

        context["posts"] = posts
        context["latest_posts"] = BlogDetailPage.objects.all().order_by("-date_published")[:10]
        # TODO - add latest blog posts context
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey("blog.BlogDetailPage", on_delete=models.CASCADE, related_name="tagged_items")


class RelatedBlogPost(Orderable):
    """Model for related blog posts"""
    page = ParentalKey("blog.BlogDetailPage", related_name="related_posts")
    blog_post = models.ForeignKey(
        "blog.BlogDetailPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        PageChooserPanel("blog_post")
    ]


class BlogDetailPage(Page):
    """Blog Detail Page"""

    template = "blog/blog-detail.html"
    parent_page_types = ["blog.BlogIndexPage"]

    """
        - upvotes *
        - times read *
        - read time *
    """
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.PROTECT,
        related_name="+",
        help_text="Select the author of this blog post"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Select an image to use on the post's page"
    )
    date_published = models.DateTimeField(auto_now_add=True)
    quote = models.TextField(_("A Programming Quote"), help_text="Enter some programming quote", blank=False, null=False)
    category = models.ForeignKey(
        "blog.BlogCategory",
        on_delete=models.PROTECT,
        related_name="+",
        help_text="Select the category of this blog post"
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    content = StreamField([
        ("heading", blocks.CharBlock()),
        ("text", blocks.TextBlock()),
        ("paragraph", blocks.RichTextBlock(
            template="blocks/rich-text-block.html",
            features=['h1', 'h2', 'h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'image', 'code', 'blockquote']
            )
        ),
        ("code", CodeBlock()),
        ("image", ImageChooserBlock()),
    ])

    def get_context(self, request, *args, **kwargs):
        context =  super().get_context(request, *args, **kwargs)
        context["posts_from_author"] = BlogDetailPage.objects.live().filter(author__full_name=self.author.full_name).exclude(title=self.title)[:5]
        return context

    content_panels = Page.content_panels + [
        ImageChooserPanel("image"),
        MultiFieldPanel([
            FieldRowPanel([
                SnippetChooserPanel("author"),
                SnippetChooserPanel("category")
            ]),
        ], heading="Author and Category"),
        FieldPanel("tags"),
        FieldPanel("quote"),
        MultiFieldPanel([
            StreamFieldPanel("content"),
        ], heading="Blog Content", classname="collapse collapsed"),
        MultiFieldPanel([
            InlinePanel("related_posts", max_num=10, min_num=1, heading="Related Post")
        ], heading="Related Blog Posts")
    ]

"""
TODO
todo - add related blog posts ( at most 5 of them)
todo - add other posts by author ( at most 5 of them )
"""