import api

#qualified = api.qualified_teams('1718-NYC-MCSM', 5)
#for award in qualified:
#    print award
#    print api.get_team_stats_at_event(award[1], '1718-NYC-MCSM')

#print api.get_team_basic_stats_at_event('9371', '1718-NYC-MCSM')
print api.get_team_detailed_stats_at_event('9371', '1718-NYC-MCSM')

print api.get_match_details('1718-NYC-MCSM-E001-1')
