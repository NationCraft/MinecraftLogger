from datetime import datetime
from mcstatus import MinecraftServer
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
db = client.minecraft_logger
session_log = db.session_log
# player_dict_list = []


def main():
    beta_online_players = []
    play_online_players = []
    dev_online_players = []
    beta_player_dict = []
    play_player_dict = []
    dev_player_dict = []

    while True:
        try:
            beta_online_players = get_query('beta.nationmc.net', 25565)
        except Exception as e:
            print('beta', e)
        # run_logout(beta_online_players)
        for pdict in beta_player_dict:
            result = exist_in_list(pdict, beta_online_players)
            if result is False:
                # This adds the logout info, inserts player into mongodb and removes player from list
                pdict['logout'] = datetime.utcnow()
                session_log.insert(pdict)
                beta_player_dict.remove(pdict)
            else:
                continue

        # run_login('beta', beta_online_players)
        for p in beta_online_players:
            result = exist_in_dict(p, beta_player_dict)
            if result is False:  # Add Player to the beta_player_dict
                beta_player_dict.append({'username': p, 'server': 'beta', 'login': datetime.utcnow()})
# ***************************************************************************************
        try:
            play_online_players = get_query('play.nationmc.net', 25565)
        except Exception as e:
            print('play', e)
        # run_logout(play_online_players)
        for pdict in play_player_dict:
            result = exist_in_list(pdict, play_online_players)
            if result is False:
                # This adds the logout info, inserts player into mongodb and removes player from list
                pdict['logout'] = datetime.utcnow()
                session_log.insert(pdict)
                play_player_dict.remove(pdict)
            else:
                continue

        # run_login('play', play_online_players)
        for p in play_online_players:
            result = exist_in_dict(p, play_player_dict)
            if result is False:  # Add Player to the play_player_dict
                play_player_dict.append({'username': p, 'server': 'play', 'login': datetime.utcnow()})
# ****************************************************************************************
        try:
            dev_online_players = get_query('dev.nationmc.net', 25565)
        except Exception as e:
            print('dev', e)
        # run_logout(dev_online_players)
        for pdict in dev_player_dict:
            result = exist_in_list(pdict, dev_online_players)
            if result is False:
                # This adds the logout info, inserts player into mongodb and removes player from list
                pdict['logout'] = datetime.utcnow()
                session_log.insert(pdict)
                dev_player_dict.remove(pdict)
            else:
                continue

        # run_login('dev', dev_online_players)
        for p in dev_online_players:
            result = exist_in_dict(p, dev_player_dict)
            if result is False:  # Add Player to the dev_player_dict
                dev_player_dict.append({'username': p, 'server': 'dev', 'login': datetime.utcnow()})

        time.sleep(60)


def get_query(mc_server, port=25565):
    mc = MinecraftServer(mc_server, port)
    query = mc.query()
    return query.players.names

'''
def run_logout(server_name, online_players):
    for pdict in player_dict_list:
        result = exist_in_list(pdict, online_players)
        if result is False:
            # This adds the logout info, inserts player into mongodb and removes player from list
            pdict['logout'] = datetime.utcnow()
            session_log.insert(pdict)
            player_dict_list.remove(pdict)
        else:
            continue


def run_login(server_name, online_players):
    global player_dict_list
    for p in online_players:
        result = exist_in_dict(p)
        if result is False:  # Add Player to the player_dict_list
            player_dict_list.append({'username': p, 'server': server_name, 'login': datetime.utcnow()})
'''


# check if the player from the dictionary list exists in online players list
def exist_in_list(playerdict, online_players):
    for p in online_players:
        if p == playerdict['username']:
            return True
    return False


# check if player from online list exists in player dictionary
def exist_in_dict(player, dictionary):
    for p in dictionary:
        if p['username'] == player:
            return True
    return False


if __name__ == '__main__':
    main()