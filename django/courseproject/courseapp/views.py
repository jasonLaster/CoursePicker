from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers

from models import *

def get_search(request):
    # we assume that it was a POST request made all ajaxey-like
    results = Course.objects
    if 'professor' in request.POST:
        prof = request.POST['professor']
        results = results.filter(courseoffering__professors__contains=prof)
        
    mimetype = 'application/javascript'
    format = 'json'
    results = results.all()
    data = serializers.serialize(format, results)
    return HttpResponse(data,mimetype)

def populate_medians(request):
    import medians
    records = medians.load()

    for record in records:
        # medians correspond to offerings

        # Course
        c = Course.objects.get_or_create(dept=record['dept'], number=record['number'])
        c.dept = record['dept']
        c.number = record['number']
        c.put()

        # Course offering
        o = CourseOffering.objects.get_or_create(course=c, term=record['term'], section=record['section'])

        o.median = record['median']
        o.term = record['term']
        o.section = record['section']
        o.enrollment = record['enrollment']

        o.course = c
        o.put()
