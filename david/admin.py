# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Fixture
from .models import Standing

admin.site.register(Fixture)
admin.site.register(Standing)