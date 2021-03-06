# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings

from customers.models import CustomerPolygons

class Command(BaseCommand):
    def handle(self, *args, **options):
        for cp in CustomerPolygons.objects.all():
            if not cp.kml_url:
                if '/data/work/virtualenvs' in cp.kml_path:
                    cp.kml_url = 'http://127.0.0.1:8000/' + settings.KML_DIRECTORY + '/' + cp.kml_name
                    cp.save()
                else:
                    cp.kml_url = 'http://indy4.epcc.ed.ac.uk/' + settings.KML_DIRECTORY + '/' + cp.kml_name
                    cp.save()
