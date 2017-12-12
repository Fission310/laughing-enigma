import requests

from config import BASE_URL, HEADERS, SEASON, QUAL_CRITERIA


def get_results(team_num):
    url = BASE_URL + '/apiv2/team/%s/%s/results' % (team_num, SEASON)
    return requests.get(url, headers = HEADERS).json()

def get_event(event_id):
    url = BASE_URL + '/apiv2/event/%s' % (event_id)
    return requests.get(url, headers = HEADERS).json()[0]

def get_match(match_id):
    url = BASE_URL + '/apiv2/match/%s' % (match_id)
    return requests.get(url, headers = HEADERS).json()[0]

def get_match_stations(match_id):
    url = BASE_URL + '/apiv2/match/%s/stations' % (match_id)
    return requests.get(url, headers = HEADERS).json()

def get_high_score():
    url = BASE_URL + '/apiv2/matches/%s/high-scores/elim-no-penalty' % (SEASON)
    return requests.get(url, headers = HEADERS).json()

def get_awards(event_id):
    url = BASE_URL + '/apiv2/event/%s/awards' % (event_id)
    return requests.get(url, headers = HEADERS).json()

def get_award_at_event(event_id, award_id):
    awards = get_awards(event_id)
    for award in awards:
        if award['award_key'] == award_id:
            return award
    return -1

def get_team(team_num):
    url = BASE_URL + '/apiv2/team/%s' % (team_num)
    return requests.get(url, headers = HEADERS).json()[0]

def qualified_teams(event_id, num_spots):
    teams_qualified = []
    teams = []
    for qual in QUAL_CRITERIA:
        if len(teams) >= num_spots:
            break;
        award = get_award_at_event(event_id, qual)
        if award['team_key'] not in teams:
            team = get_team(award['team_key'])
            teams.append(award['team_key'])
            teams_qualified.append((award['award_name'], award['team_key'], team['team_name_short']))

    return teams_qualified

def get_team_results(team_num):
    url = BASE_URL + '/apiv2/team/%s/%s/results' % (team_num, SEASON)
    return requests.get(url, headers = HEADERS).json()

def get_team_results_at_event(team_num, event_id):
    results = get_team_results(team_num)
    for result in results:
        if result['event_key'] == event_id:
            return result
    return -1

def get_matches(event_id):
    url = BASE_URL + '/apiv2/event/%s/matches' % (event_id)
    return requests.get(url, headers = HEADERS).json()

def get_match_details(match_id):
    url = BASE_URL + '/apiv2/match/%s/details' % (match_id)
    return requests.get(url, headers = HEADERS).json()[0]

def get_stations(event_id):
    url = BASE_URL + '/apiv2/event/%s/matches/stations' % (event_id)
    return requests.get(url, headers = HEADERS).json()

def get_matches_for_team(team_num, event_id):
    team_matches = []
    stations = get_stations(event_id)
    matches = get_matches(event_id)

    for station in stations:
        if team_num in station['teams']:
            teams = station['teams'].split(',')
            is_red = (team_num in teams[:len(teams)/2])
            for match in matches:
                if match['match_key'] == station['match_key']:
                    details = get_match_details(match['match_key'])
                    team_matches.append((station, match, details, is_red))
                    break

    return team_matches

def get_team_basic_stats_at_event(team_num, event_id):
    stats = {}
    matches = get_matches_for_team(team_num, event_id)
    event = get_event(event_id)

    average = 0.0
    average_tele = 0.0
    average_auto = 0.0
    average_end = 0.0
    average_pen = 0.0
    count = 0
    for match in matches:
        if match[3]:
            average += match[0]['red_score']
            average_tele += match[1]['red_tele_score']
            average_auto += match[1]['red_auto_score']
            average_end += match[1]['red_end_score']
            average_pen += match[1]['red_penalty']
        else:
            average += match[0]['blue_score']
            average_tele += match[1]['blue_tele_score']
            average_auto += match[1]['blue_auto_score']
            average_end += match[1]['blue_end_score']
            average_pen += match[1]['blue_penalty']
        count += 1

    stats['team_num'] = team_num
    stats['event_name'] = event['event_name']
    stats['avg_score'] = round(average / count, 1)
    stats['avg_tele'] = round(average_tele / count, 1)
    stats['avg_auto'] = round(average_auto / count, 1)
    stats['avg_end'] = round(average_end / count, 1)
    stats['avg_pen'] = round(average_pen / count, 1)

    return stats

def get_team_detailed_stats_at_event(team_num, event_id):
    stats = {}
    matches = get_matches_for_team(team_num, event_id)
    event = get_event(event_id)

    avg_auto_glyphs = 0.0
    avg_auto_jewel = 0.0
    avg_auto_park = 0.0
    avg_tele_glyphs = 0.0
    count = 0
    for match in matches:
        if match[3]:
            avg_auto_glyphs += match[2]['red_auto_glyphs']
            avg_auto_jewel += match[2]['red_auto_jewel']
            avg_auto_park += match[2]['red_auto_park']
            avg_tele_glyphs += match[2]['red_tele_glyphs']
        else:
            avg_auto_glyphs += match[2]['blue_auto_glyphs']
            avg_auto_jewel += match[2]['blue_auto_jewel']
            avg_auto_park += match[2]['blue_auto_park']
            avg_tele_glyphs += match[2]['blue_tele_glyphs']
        count += 1

    stats['team_num'] = team_num
    stats['event_name'] = event['event_name']
    stats['avg_auto_glyphs'] = round(avg_auto_glyphs / count, 1)
    stats['avg_auto_jewel'] = round(avg_auto_jewel / count, 1)
    stats['avg_auto_park'] = round(avg_auto_park / count, 1)
    stats['avg_tele_glyphs'] = round(avg_tele_glyphs / count, 1)

    return stats
