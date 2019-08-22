import os
from decouple import config
from flask import (Flask, request, abort)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
import json
from linebot.models import (
    MessageEvent, 
    TextMessage, 
    TextSendMessage,
    SourceUser,
    SourceGroup,
    SourceRoom,
    MessageAction,
    LeaveEvent,
    JoinEvent
)
import requests
import time
import re

# DEFINE GLOBAL VARIABLES
msg_join = 'Congratulations!! You are joining the Werewolf Game'
str_curr = 'Current players: \n'
players_arr = []
displayname = []
userid = []
state = config('state')

'''
0. Join state
1. startgame stat
2. endgame
'''

##############################################################################

def main(event, line_bot_api, handler, incoming_msg): 
    if state == 0:
        if incoming_msg == '/join': # If user type '/join'
            if isinstance(event.source, SourceGroup): # If eventnya dari group
                profile = line_bot_api.get_profile(event.source.user_id)

                print('Num of userid: ' + str(len(userid)))

                if len(userid) == 0: # If players is still null
                    userid.append(profile.user_id) 
                    displayname.append(profile.display_name)
                    print('Add user ID: ' + profile.user_id)
                    line_bot_api.push_message(profile.user_id, TextSendMessage(msg_join))
                    
                    # Announce who are the players
                    players_arr.append(str(len(userid)) + '. ' + profile.display_name)
                    print(players_arr)
                    players = '\n'.join(players_arr)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(str_curr + players))

                elif len(userid) > 0: # If players more than 0
                    if profile.user_id not in userid: # If he/she is a new player
                        userid.append(profile.user_id) 
                        displayname.append(profile.display_name)
                        print('Add user ID: ' + profile.user_id)    
                        line_bot_api.push_message(profile.user_id, TextSendMessage(msg_join))

                        # Announce who are the players
                        players_arr.append(str(len(userid)) + '. ' + profile.display_name)
                        print(players_arr)          
                        players = '\n'.join(players_arr)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(str_curr + players))
                    else:  # If not a new player
                        print('Not a new player')
                        line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you are already in the game'))

                print('PLAYERS: ' + str(players_arr))

    if incoming_msg == '/startgame' and state == 0: # Kasih role ke masing" orang, randomize depends on the num of players
        if len(userid) >= 4 and len(userid) <= 6: # If total players antara 4-6
            state = 1
            print('Game has started | 4-6 players')
            line_bot_api.reply_message(event.reply_token, TextSendMessage('The game has started!! \nAuuuuuuuwwww!! Who is the werewolf here? Let\'s find out!'))
        elif len(userid) >= 7 and len(userid) <= 12: # If total players antara 7-12
            state = 1
            print('Game has started | 7-12 players')
            line_bot_api.reply_message(event.reply_token, TextSendMessage('The game has started!! \nAuuuuuuuwwww!! Who are the werewolves here? Let\'s find out!'))
        elif len(userid) < 4: # If players kurang dari 4
            line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you are too lonely (min 4 ppl)'))
        elif len(userid) > 12:  # If players lebih dari 12
            line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you guys are too crowded (max 12 ppl)'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('Werewolf is under maintenance :)'))


    # if incoming_msg == '/leave':
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage('See you next game, '))
    

                