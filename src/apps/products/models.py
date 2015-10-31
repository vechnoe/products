# coding: utf-8

from decimal import Decimal
from datetime import timedelta

from pytils import translit

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(u"Product's name", max_length=255)
    slug = models.SlugField(blank=True)
    description = models.TextField(verbose_name=u"Item's description")
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                default=Decimal('0.00'),
                                validators=[
                                    MinValueValidator(Decimal('0.00'))],
                                max_length=255,
                                verbose_name=u'Price',
                                blank=True, null=True)

    created_at = models.DateTimeField(null=True, blank=True,
                                      auto_now_add=True,
                                      verbose_name=u'Creation date')
    modified_at = models.DateTimeField(null=True, blank=True,
                                       auto_now=True,
                                       verbose_name=u'Update date')

    def __unicode__(self):
        return u'%s: %s' % (self.name, self.price)

    class Meta:
        ordering = ['name']
        verbose_name = u'Product'
        verbose_name_plural = u'Products'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = translit.slugify(self.name.decode('utf-8'))
        super(Product, self).save(*args, **kwargs)

    @property
    def likes(self):
        return Like.objects.filter(product__id=self.id).count()

    def can_like(self, user):
        return not Like.objects.filter(user=user, product__id=self.id).exists()

    def get_last_comments(self):
        time_threshold = timezone.now() - timedelta(hours=24)
        return Comment.objects.filter(
            product__id=self.id, created_at__gt=time_threshold)


class Comment(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User, blank=True, null=True)
    text = models.TextField(verbose_name=u"Comment's body")
    created_at = models.DateTimeField(null=True, blank=True,
                                      auto_now_add=True,
                                      verbose_name=u'Creation date')

    def __unicode__(self):
        return u'%s' % self.created_at.strftime('%d.%m.%Y')

    class Meta:
        ordering = ['-created_at']
        verbose_name = u'Comment'
        verbose_name_plural = u'Comments'


class Like(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s %s' % (self.product, self.user)

    class Meta:
        unique_together = ('product', 'user')
        verbose_name = u'Like'
        verbose_name_plural = u'Likes'

