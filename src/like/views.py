from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.http.response import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Like
# Create your views here.
from django.views.generic import View


class LikeView(View):
    def dispatch(self, request, content_type_id=None, pk=None, value=False, *args, **kwargs):
        content_type = get_object_or_404(ContentType, id=content_type_id)
        model_class = content_type.model_class()
        self.object = get_object_or_404(model_class, id=pk)
        self.is_ajax_request = request.is_ajax()
        self.value = value
        self.user = request.user
        return super(LikeView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

    def post(self, *args, **kwargs):
        like = Like.objects.filter(user=self.user,
                                   item_type=ContentType.objects.get_for_model(self.object.__class__),
                                   item_id=self.object.pk).first()
        if like:
            like.value = self.value
        else:
            like = Like(item_type=ContentType.objects.get_for_model(self.object.__class__),
                        item_id=self.object.pk,
                        user=self.user,
                        value=self.value)
        like.save()

        likes = Like.objects.all().filter(item_type=ContentType.objects.get_for_model(self.object.__class__),
                                          item_id=self.object.pk,
                                          value=True).count()
        dislikes = Like.objects.all().filter(item_type=ContentType.objects.get_for_model(self.object.__class__),
                                             item_id=self.object.pk,
                                             value=False).count()
        rating = likes - dislikes

        if self.is_ajax_request:
            return JsonResponse({'like': like.value, 'rating': rating})
        else:
            return redirect(self.object)
