from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms.widgets import RadioSelect

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    PageChooserPanel,
    InlinePanel,
    MultiFieldPanel,
    HelpPanel,
    StreamFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey

class TestOrderable(Orderable):

    page = ParentalKey("testpage.TestPage", related_name="test_ord")
    sub_page = models.ForeignKey(
        'testpage.TestSubPage',
        on_delete=models.PROTECT,
    )
    datetime_field = models.DateTimeField(
        help_text="Date and Time the test commences"
    )
    time_field = models.TimeField(
        blank=True,
        null=True,
        help_text="Time the test commences"
    )
    message = RichTextField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Message needs to have been approved"
    )

    panels = [
        FieldPanel('sub_page'),
        FieldPanel('datetime_field'),
        FieldPanel('time_field'),
        FieldPanel('message'),
    ]

class TestPage(Page):

    time_field = models.DateTimeField(
        help_text="Date and Time the event commences."
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        related_name='+',
        help_text="Hero image, at least 800x375, requires landscape crop"
    )
    char_field_1 = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Short line describing any event organiser"
    )
    char_field_2 = models.CharField(
        max_length=128,
        help_text="Very short one-liner describing the event"
    )
    introduction = RichTextField(
        max_length=1500,
        features=['bold', 'italic', 'link'],
        blank=True,
        null=True,
        help_text="Event Introduction"
    )
    duration = models.IntegerField(
        default=120,
        help_text="Nominal duration of the event in minutes"
    )
    char_field_3 = models.CharField(
        max_length=128,
        help_text="Very short one-liner describing the event"
    )
    char_field_4 = models.CharField(
        max_length=128,
        help_text="Very short one-liner describing the event"
    )
    sub_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Info page related to the event"
    )

    # Editor panels configuration
    principal_panels = Page.content_panels + [
        FieldPanel('time_field'),
        ImageChooserPanel('hero_image'),
        FieldPanel('char_field_1'),
        FieldPanel('introduction'),
    ]

    ord_panels = [
        MultiFieldPanel(
            [
                InlinePanel('test_ord', label="Orderables")
            ],
            heading="Orderables List",
            help_text="List Ords in the required order"
        ),
        FieldPanel('duration'),
    ]

    event_panels = [
        FieldPanel('char_field_2'),
        PageChooserPanel('sub_page', 'testpage.TestSubPage'),
    ]

    sponsor_panels = [
        MultiFieldPanel(
            [
                FieldPanel('char_field_3'),
                FieldPanel('char_field_4'),
            ],
            heading="Multifield Panel",
            help_text="A couple of random strings",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(principal_panels, heading="Title & Introduction"),
            ObjectList(ord_panels, heading="Event Details"),
            ObjectList(event_panels, heading="More Details"),
            ObjectList(sponsor_panels, heading="Sponsor Details"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings"),
        ]
    )


class TestSubPage(Page):
    pass