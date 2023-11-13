from django.db import models


class SEO(models.Model):
    class Meta:
        abstract = True

    seo_title = models.CharField('seo_title', max_length=255, blank=True, null=True)
    seo_description = models.CharField('seo_description', max_length=255, blank=True, null=True)
    seo_keywords = models.CharField('seo_keywords', max_length=255, blank=True, null=True)
    og_title = models.CharField('seo og:title', max_length=64, blank=True, null=True)
    og_image = models.ImageField('seo og:image', upload_to='seo', blank=True, null=True)
    og_description = models.TextField('seo og:description', max_length=300, blank=True, null=True)
