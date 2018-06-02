from django_cron import CronJobBase, Schedule
from david.models import Standing
from david.models import Fixture
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
        connection.request('GET', '/v1/teams/73/fixtures', None, headers)
        response = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v1/teams/73/fixtures?season=2016', None, headers)
        response16 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v1/teams/73/fixtures?season=2015', None, headers)
        response15 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v1/competitions/445/leagueTable', None, headers)
        response_table = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v1/teams/73/fixtures?season=2014', None, headers)
        response14 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v1/teams/73/fixtures?season=2013', None, headers)
        response13 = json.loads(connection.getresponse().read().decode())

        fixtures = response['fixtures']
        fixtures16 = response16['fixtures']
        fixtures15 = response15['fixtures']
        fixtures14 = response14['fixtures']
        fixtures13 = response13['fixtures']

        Fixture.objects.all().delete()
        Standing.objects.all().delete()

        def addseason(fix, resp):
            for i, val in enumerate(fix):

                if fix[i]['homeTeamName'] == 'Tottenham Hotspur FC':
                    opponent = fix[i]['awayTeamName']
                else:
                    opponent = fix[i]['homeTeamName']
                if fix[i]['homeTeamName'] == 'Tottenham Hotspur FC':
                    gameType = 'Home'
                else:
                    gameType = 'Away'
                if fix[i]['status'] != 'FINISHED':
                    result = 'Not Played'
                elif fix[i]['result']['goalsAwayTeam'] == fix[i]['result']['goalsHomeTeam']:
                    result = 'Draw'
                elif fix[i]['result']['goalsHomeTeam'] > fix[i]['result']['goalsAwayTeam'] and gameType == 'Home':
                    result = 'Win'
                elif fix[i]['result']['goalsAwayTeam'] > fix[i]['result']['goalsHomeTeam'] and gameType == 'Away':
                    result = 'Win'
                else:
                    result = 'Loss'
                Fixture.objects.create(status=fix[i]['status'],
                                       matchday=fix[i]['matchday'],
                                       homeTeamName=fix[i]['homeTeamName'],
                                       awayTeamName=fix[i]['awayTeamName'],
                                       goalsAwayTeam=fix[i]['result']['goalsAwayTeam'],
                                       goalsHomeTeam=fix[i]['result']['goalsHomeTeam'],
                                       competitionId=fix[i]['competitionId'],
                                       name=fix[i]['homeTeamName'] + " " + fix[i]['awayTeamName'],
                                       opponent=opponent,
                                       gameType=gameType,
                                       result=result,
                                       date=fix[i]['date'],
                                       season=resp['season'])

        print('fixtures updated')

        addseason(fixtures, response)
        addseason(fixtures16, response16)
        addseason(fixtures15, response15)
        addseason(fixtures14, response14)
        addseason(fixtures13, response13)

        tabstand = response_table['standing']

        for i, val in enumerate(tabstand):
            Standing.objects.create(teamName=tabstand[i]['team'],
                                    position=tabstand[i]['rank'],
                                    goalDifference=tabstand[i]['goalDifference'],
                                    points=tabstand[i]['points'],
                                    crestURL=tabstand[i]['crestURI'],
                                    matchesPlayed=tabstand[i]['playedGames'])

        print('standing updated')
