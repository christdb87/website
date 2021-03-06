from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, **options):
        import httplib
        import json
        from datetime import datetime
        from david.models import Fixture
        from david.models import Standing

        connection = httplib.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': os.environ['FOOTBALL_API_KEY'], 'X-Response-Control': 'minified'}
        connection.request('GET', '/v2/teams/73/matches', None, headers)
        response = json.loads(connection.getresponse().read())
        connection.request('GET', '/v1/teams/73/fixtures?season=2017', None, headers)
        response17 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v1/teams/73/fixtures?season=2016', None, headers)
        response16 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v1/teams/73/fixtures?season=2015', None, headers)
        response15 = json.loads(connection.getresponse().read().decode())
        connection.request('GET', '/v2/competitions/2021/standings', None, headers)
        response_table = json.loads(connection.getresponse().read().decode())

        fixtures = response['matches']
        fixtures17 = response17['fixtures']
        fixtures16 = response16['fixtures']
        fixtures15 = response15['fixtures']

        Fixture.objects.all().delete()
        Standing.objects.all().delete()

        def addseason_hist(fix, resp):
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

                print(fix[i]['status'], " ",
                      fix[i]['matchday'], " ",
                      fix[i]['homeTeamName'], " ",
                      fix[i]['awayTeamName'], " ",
                      fix[i]['result']['goalsAwayTeam'], " ",
                      fix[i]['result']['goalsHomeTeam'])

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
                elif fix[i]['score']['fullTime']['awayTeam'] > fix[i]['score']['fullTime']['homeTeam'] and gameType == 'Away':
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

        addseason(fixtures, response)
        addseason_hist(fixtures16, response16)
        addseason_hist(fixtures15, response15)
        addseason_hist(fixtures17, response17)

        tabstand = response_table['standings'][0]['table']

        for i, val in enumerate(tabstand):
            Standing.objects.create(teamName=tabstand[i]['team']['name'],
                                    position=tabstand[i]['position'],
                                    goalDifference=tabstand[i]['goalDifference'],
                                    points=tabstand[i]['points'],
                                    crestURL=tabstand[i]['team']['crestUrl'],
                                    matchesPlayed=tabstand[i]['playedGames'])

            # code to use pyton 3 to get data
            #
            # import http.client
            # import json
            #
            # connection = http.client.HTTPConnection('api.football-data.org')
            # headers = {'X-Auth-Token': '495fc1f2cf2e4dc5a83fb3dc6d3bfcd1', 'X-Response-Control': 'minified'}
            # connection.request('GET', '/v1/competitions/445/leagueTable', None, headers)
            # response = json.loads(connection.getresponse().read().decode())
            #
            # print(response)
