# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from david.models import Fixture
from david.models import Standing
from django.template.defaulttags import register
import pygal
from pygal.style import DarkStyle;

def index(request):

    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    fixtures18 = dict(Fixture.objects.values_list('matchday', 'result').filter(competitionId=151))
    fixtures17 = dict(Fixture.objects.values_list('matchday', 'result').filter(competitionId=445))
    fixtures16 = dict(Fixture.objects.values_list('matchday', 'result').filter(competitionId=426))
    fixtures15 = dict(Fixture.objects.values_list('matchday', 'result').filter(competitionId=398))
    point_total_17 = 0
    points_17 = {}
    point_total_16 = 0
    points_16 = {}
    point_total_15 = 0
    points_15 = {}
    point_total_18 = 0
    points_18 = {}

    def getpoints(fix, pts, total):
        for i, val in fix.iteritems():
            if fix[i] == 'Win':
                total = total + 3
                pts.update({i: total})
            elif fix[i] == 'Draw':
                total = total + 1
                pts.update({i: total})
            elif fix[i] == 'Not Played':
                pts.update({i: None})
            else:
                pts.update({i: total})

    getpoints(fixtures17, points_17, point_total_17)
    getpoints(fixtures16, points_16, point_total_16)
    getpoints(fixtures15, points_15, point_total_15)
    getpoints(fixtures18, points_18, point_total_18)

    chart = pygal.Line(style=DarkStyle,
                       x_title="Matchday",
                       height=500)
    chart.title = "Spurs points over past 4 seasons"
    chart.add("2018", points_18.values())
    chart.add("2017", points_17.values())
    chart.add("2016", points_16.values())
    chart.add("2015", points_15.values())
    chart.x_labels = range(1, 39)
    pts_chart = chart.render_data_uri()

    matches18 = Fixture.objects.filter(competitionId=151).order_by('matchday')
    last_three = matches18.filter(status='FINISHED').order_by('-matchday')[:3]
    last_three_asc = reversed(last_three)

    if matches18.filter(status='TIMED').count() > 0:
        next_game = matches18.filter(status='TIMED')[0]
    elif matches18.filter(status='SCHEDULED').count() > 0:
        next_game = matches18.filter(status='SCHEDULED').order_by('matchday')[0]
    else:
        next_game = None

    spurspos = Standing.objects.filter(teamName='Tottenham Hotspur FC')[0].position
    table = Standing.objects.filter(position__in=range(spurspos - 3, spurspos + 4))

    return render(request, 'david/spurscontent.html', {'last_three': last_three_asc,
                                                       'next': next_game,
                                                       'chart': pts_chart,
                                                       'table': table})


def monster(request):

    return render(request, 'david/monster.html', {})
