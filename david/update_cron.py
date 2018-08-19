from django_cron import CronJobBase, Schedule
from david.models import Standing
from david.models import Fixture
from datetime import datetime
import httplib
import json
import os

class UpdateCron(CronJobBase):
    RUN_AT_TIMES = ['21:55', '22:40']  # every 2 hours

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'david.update_cron'    # a unique code

    def do(self):

        connection = httplib.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': os.environ['FOOTBALL_API_KEY'], 'X-Response-Control': 'minified'}
        connection.request('GET', '/v2/teams/73/fixtures', None, headers)
        response = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v2/teams/73/matches?season=2017', None, headers)
        response17 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v2/teams/73/matches?season=2016', None, headers)
        response16 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v2/teams/73/matches?season=2015', None, headers)
        response15 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v2/competitions/2021/standings', None, headers)
        response_table = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v2/teams/73/matches?season=2014', None, headers)
        response14 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v2/teams/73/matches?season=2013', None, headers)
        response13 = json.loads(connection.getresponse().read().decode())

        fixtures = response['matches']
        fixtures17 = response17['matches']
        fixtures16 = response16['matches']
        fixtures15 = response15['matches']
        fixtures14 = response14['matches']
        fixtures13 = response13['matches']

        Fixture.objects.all().delete()
        Standing.objects.all().delete()

        def addseason(fix, resp):
            for i, val in enumerate(fix):

                if fix[i]['homeTeam']['name'] == 'Tottenham Hotspur FC':
                    opponent = fix[i]['awayTeam']['name']
                else:
                    opponent = fix[i]['homeTeam']['name']
                if fix[i]['homeTeam']['name'] == 'Tottenham Hotspur FC':
                    gameType = 'Home'
                else:
                    gameType = 'Away'
                if fix[i]['status'] != 'FINISHED':
                    result = 'Not Played'
                elif fix[i]['score']['fullTime']['awayTeam'] == fix[i]['score']['fullTime']['homeTeam']:
                    result = 'Draw'
                elif fix[i]['score']['fullTime']['homeTeam'] > fix[i]['score']['fullTime']['awayTeam'] and gameType == 'Home':
                    result = 'Win'
                elif fix[i]['score']['fullTime']['awayTeam'] > fix[i]['score']['fullTime']['awayTeam'] and gameType == 'Away':
                    result = 'Win'
                else:
                    result = 'Loss'
                Fixture.objects.create(status=fix[i]['status'],
                                       matchday=fix[i]['matchday'],
                                       homeTeamName=fix[i]['homeTeam']['name'],
                                       awayTeamName=fix[i]['awayTeam']['name'],
                                       goalsAwayTeam=fix[i]['score']['fullTime']['awayTeam'],
                                       goalsHomeTeam=fix[i]['score']['fullTime']['homeTeam'],
                                       competitionId=fix[i]['season']['id'],
                                       name=fix[i]['homeTeam']['name'] + " " + fix[i]['awayTeam']['name'],
                                       opponent=opponent,
                                       gameType=gameType,
                                       result=result,
                                       date=fix[i]['utcDate'],
                                       season=datetime.strptime(fix[i]['season']['startDate'], '%Y-%m-%d').year)

                print(fix[i]['matchday'])

        print('fixtures updated')

        addseason(fixtures, response)
        addseason(fixtures17, response17)
        addseason(fixtures16, response16)
        addseason(fixtures15, response15)
        addseason(fixtures14, response14)
        addseason(fixtures13, response13)

        tabstand = response_table['standings'][0]['table']

        for i, val in enumerate(tabstand):
            Standing.objects.create(teamName=tabstand[i]['team']['name'],
                                    position=tabstand[i]['position'],
                                    goalDifference=tabstand[i]['goalDifference'],
                                    points=tabstand[i]['points'],
                                    crestURL=tabstand[i]['team']['crestUrl'],
                                    matchesPlayed=tabstand[i]['playedGames'])

        print('standing updated')
