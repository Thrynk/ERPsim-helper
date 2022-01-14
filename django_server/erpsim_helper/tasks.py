from huey import crontab
from huey.contrib.djhuey import task

@task()
def get_game_latest_data(game_id, odata_flow, game_set, team):
    print('-- game_id : {} flow : {} set : {} team : {}--'.format(game_id, odata_flow, game_set, team))
    return '-- game_id : {} flow : {} set : {} team : {}--'.format(game_id, odata_flow, game_set, team)