# coding: utf-8

from decimal import Decimal
from datetime import timedelta

from uuslug import uuslug

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import signals
from django.dispatch import receiver


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().prefetch_related(
            models.Prefetch(
                'likes', queryset=Like.prefetch_likes.all()),
            models.Prefetch(
                'comments', queryset=Comment.latest_comments.all())).all()


class Product(models.Model):
    name = models.CharField(u"Product's name", max_length=255)
    slug = models.SlugField(blank=True)
    description = models.TextField(verbose_name=u"Item's description")
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                default=Decimal('0.00'),
                                max_length=255,
                                verbose_name=u'Price',
                                blank=True, null=True)

    created_at = models.DateTimeField(null=True, blank=True,
                                      auto_now_add=True,
                                      verbose_name=u'Creation date')
    modified_at = models.DateTimeField(null=True, blank=True,
                                       auto_now=True,
                                       verbose_name=u'Update date')

    objects = models.Manager()
    prefetch_products = ProductManager()

    def __unicode__(self):
        return u'%s: %s' % (self.name, self.price)

    class Meta:
        verbose_name = u'Product'
        verbose_name_plural = u'Products'

    def clean(self):
        if self.price < Decimal('0.00'):
            raise ValidationError('Price must be greater than zero')
        super(Product, self).clean()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.name, instance=self)
        super(Product, self).save(*args, **kwargs)


@receiver(signals.pre_save, sender=Product)
def validate_price(sender, instance=None, created=False, **kwargs):
    instance.clean()


class LatestCommentManager(models.Manager):
    def get_queryset(self):
        time_threshold = timezone.now() - timedelta(hours=24)
        return super(LatestCommentManager, self).get_queryset().filter(
            created_at__gt=time_threshold).select_related('user')


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments')
    user = models.ForeignKey(User, blank=True, null=True)
    text = models.TextField(verbose_name=u"Comment's body")
    created_at = models.DateTimeField(null=True, blank=True,
                                      verbose_name=u'Creation date')

    objects = models.Manager()
    latest_comments = LatestCommentManager()

    def __unicode__(self):
        if not self.created_at:
            return 'Empty date'
        return u'%s' % self.created_at.strftime('%d.%m.%Y')

    class Meta:
        ordering = ['-created_at']
        verbose_name = u'Comment'
        verbose_name_plural = u'Comments'


class LikeManager(models.Manager):
    def get_queryset(self):
        return super(LikeManager, self).get_queryset().select_related('user')


class Like(models.Model):
    product = models.ForeignKey(Product, related_name='likes')
    user = models.ForeignKey(User)

    objects = models.Manager()
    prefetch_likes = LikeManager()

    def __unicode__(self):
        return u'%s' % self.product.name

    class Meta:
        unique_together = ('product', 'user')
        verbose_name = u'Like'
        verbose_name_plural = u'Likes'


