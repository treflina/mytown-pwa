from django.utils.translation import gettext as _
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

custom_table_options = {
    "renderer": "html",
    "contextMenu": {
        "items": {
            "row_above": {
                "name": _("Insert row above"),
            },
            "row_below": {
                "name": _("Insert row below"),
            },
            "col_left": {
                "name": _("Insert column left"),
            },
            "col_right": {
                "name": _("Insert column right"),
            },
            "remove_row": {
                "name": _("Remove row"),
            },
            "remove_col": {
                "name": _("Remove column"),
            },
            "---------": {
                "name": "---------",
            },
            "undo": {
                "name": _("Undo"),
            },
            "redo": {
                "name": _("Redo"),
            },
            "copy": {
                "name": _("Copy"),
            },
            "cut": {"name": _("Cut")},
            "---------": {
                "name": "---------",
            },
            "alignment": {"name": _("Alignment")},
        }
    },
}


class ImageWithAltAttr(blocks.StructBlock):
    img = ImageChooserBlock(blank=True, null=True, label=_("Image"))
    alt_attr = blocks.CharBlock(
        label=_("Alternative text"),
        help_text=_("Image description for visually impaired users & search engines."),
    )

    class Meta:
        label = _("Image")


class BodyBlock(blocks.StreamBlock):
    text = blocks.RichTextBlock(
        features=[
            "bold",
            "italic",
            "ol",
            "ul",
            "hr",
            "link",
            "document-link",
        ],
        label="Text",
        blank=True,
        null=True,
    )
    image = ImageWithAltAttr(
        template="news/image_block.html",
    )
    table = TableBlock(
        required=False,
        label=_("Table"),
        template="news/table_block.html",
        table_options=custom_table_options,
    )
    docs = blocks.ListBlock(
        DocumentChooserBlock(),
        required=False,
        label=_("Documents to download"),
        template="news/document_link_block.html",
    )
