# coding: utf-8

from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Product, Comment, Like
from .forms import CommentForm


@login_required
@require_POST
def send_like(request):
    if request.is_ajax():
        product_id = request.POST.get('productId')
        like = Like()
        like.user = request.user
        like.product = get_object_or_404(Product, id=product_id)
        like.save()
        return JsonResponse(
            {'message': 'Thanks for your feedback'}, status=201)
    return HttpResponseForbidden()


class ProductListView(ListView):
    model = Product
    template_name = 'products/products_list.html'

    def get_queryset(self):
        return Product.prefetch_products.all()


class ProductDetailView(SingleObjectMixin, FormView):
    template_name = 'products/product_detail.html'
    form_class = CommentForm

    def get_object(self, queryset=None):
        return Product.prefetch_products.get(slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProductDetailView, self).post(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'products:product_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        comment = Comment()
        comment.product = self.object
        comment.text = form.cleaned_data.get('text')
        comment.created_at = timezone.now()
        if self.request.user.is_authenticated():
            comment.user = self.request.user
        comment.save()
        messages.add_message(
            self.request, messages.SUCCESS, 'Your comment saved')
        return redirect(self.get_success_url())


