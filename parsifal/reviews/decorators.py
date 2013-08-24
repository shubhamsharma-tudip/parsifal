from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from reviews.models import Review
from functools import wraps

def author_required(f):
    def wrap(request, *args, **kwargs):
        try:
            review_id = request.POST['review-id']
        except:
            try:
                review_id = request.GET['review-id']
            except:
                return HttpResponseBadRequest()

        review = Review.objects.get(pk=review_id)
        if review.is_author_or_coauthor(request.user):
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap