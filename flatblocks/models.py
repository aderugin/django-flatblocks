from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from hvad.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField

from flatblocks.settings import CACHE_PREFIX


class FlatBlock(TranslatableModel):
    """
    Think of a flatblock as a flatpage but for just part of a site. It's
    basically a piece of content with a given name (slug) and an optional
    title (header) which you can, for example, use in a sidebar of a website.
    """
    slug = models.CharField(max_length=255, unique=True,
                verbose_name=_('Slug'),
                help_text=_("A unique name used for reference in the templates"))
    header = models.CharField(blank=True, null=True, max_length=255,
                verbose_name=_('Header'),
                help_text=_("An optional header for this content"))
    translations = TranslatedFields(
        content=RichTextField(verbose_name=_('Content'), blank=True,
                null=True)
    )

    def __unicode__(self):
        return u"%s" % (self.slug,)

    def save(self, *args, **kwargs):
        super(FlatBlock, self).save(*args, **kwargs)
        # Now also invalidate the cache used in the templatetag
        for lang in self.get_available_languages():
            cache.delete('%s%s%s' % (CACHE_PREFIX, self.slug, lang))

    class Meta:
        verbose_name = _('Flat block')
        verbose_name_plural = _('Flat blocks')
