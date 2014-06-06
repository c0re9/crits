import json

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from crits.core.user_tools import user_can_view_data
from crits.screenshots.handlers import get_screenshots_for_id, get_screenshot
from crits.screenshots.handlers import add_screenshot

@user_passes_test(user_can_view_data)
def get_screenshots(request):
    """
    Get screenshots for a top-level object. Should be an AJAX POST.

    :param request: The Django request.
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    if request.method == 'POST' and request.is_ajax():
        analyst = request.user.username
        type_ = request.POST.get('type', None)
        _id = request.POST.get('id', None)
        buckets = request.POST.get('buckets', False)
        result = get_screenshots_for_id(type_, _id, analyst, buckets)
        return HttpResponse(json.dumps(result),
                            mimetype="application/json")
    else:
        error = "Expected POST"
        return render_to_response("error.html",
                                  {"error" : error },
                                  RequestContext(request))

@user_passes_test(user_can_view_data)
def find_screenshot(request):
    """
    Find a screenshot by tag or ObjectId.

    :param request: The Django request.
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    analyst = request.user.username
    if request.method == 'POST':
        _id = request.POST.get('id', None)
        tag = request.POST.get('tag', None)
    if request.method == 'GET':
        _id = request.GET.get('id', None)
        tag = request.GET.get('tag', None)
        result = get_screenshot(_id, tag, analyst)
        return HttpResponse(json.dumps(result),
                            mimetype="application/json")
    else:
        error = "Could not get screenshot."
        return render_to_response("error.html",
                                  {"error" : error },
                                  RequestContext(request))

@user_passes_test(user_can_view_data)
def render_screenshot(request, _id, thumb=None):
    """
    Get a screenshot by ObjectId.

    :param request: The Django request.
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    analyst = request.user.username
    result = get_screenshot(_id=_id, analyst=analyst, thumb=thumb)
    if not result:
        return HttpResponse(json.dumps(''),
                            mimetype="application/json")
    else:
        return result

@user_passes_test(user_can_view_data)
def add_new_screenshot(request):
    """
    Add a new screenshot.

    :param request: The Django request.
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    analyst = request.user.username
    description = request.POST.get('description', None)
    reference = request.POST.get('reference', None)
    method = request.POST.get('method', None)
    tags = request.POST.get('tags', None)
    source = request.POST.get('source', None)
    oid = request.POST.get('oid', None)
    otype = request.POST.get('otype', None)
    screenshot_id = request.POST.get('screenshot_id', None)
    screenshot = request.FILES.get('screenshot', None)

    result = add_screenshot(description, tags, source, method, reference,
                            analyst, screenshot, screenshot_id, oid, otype)

    return HttpResponse(json.dumps(result),
                        mimetype="application/json")
