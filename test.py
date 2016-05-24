from datetime import datetime, timedelta, tzinfo
from pymongo import MongoClient
import time
import timeconverter

client = MongoClient('localhost', 27017)
db = client.minecraft_logger
session_log = db.session_log
player_dict_list = []
online_players = ['littledan45', 'aflame13']

def main():
    try:
        get_query('dev.nationmc.net', 25565)
    except Exception as e:
        print('beta', e)

    print('It continues')

'''
def main():
    global online_players
    print('online 1', online_players)
    print('dict 1', player_dict_list)
    run_logout()
    print('online 2', online_players)
    print('dict 2', player_dict_list)
    run_login('beta')
    print('online 3', online_players)
    print('dict 3', player_dict_list)
    online_players.remove('littledan45')
    run_logout()
    print('online 4', online_players)
    print('dict 4', player_dict_list)
'''

def get_query(mcserver, port=25565):
    global online_players
    mc = MinecraftServer(mcserver, port)
    query = mc.query()
    online_players = query.players.names


def run_logout():
    global player_dict_list
    for pdict in player_dict_list:
        result = exist_in_list(pdict)
        if result is False:
            # This adds the logout info, inserts player into mongodb and removes player from list
            pdict['logout'] = datetime.utcnow()
            session_log.insert(pdict)
            player_dict_list.remove(pdict)
        else:
            continue


def run_login(server_name):
    global online_players
    global player_dict_list
    for p in online_players:
        result = exist_in_dict(p)
        if result is False:  # Add Player to the player_dict_list
            player_dict_list.append({'username': p, 'server': server_name, 'login': datetime.utcnow()})


# check if the player from the dictionary list exists in online players list
def exist_in_list(playerdict):
    for p in online_players:
        if p == playerdict['username']:
            return True
    return False


# check if player from online list exists in player dictionary
def exist_in_dict(player):
    for p in player_dict_list:
        if p['username'] == player:
            return True
    return False

if __name__ == '__main__':
    main()
