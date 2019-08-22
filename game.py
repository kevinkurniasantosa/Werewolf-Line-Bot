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

########################################kek###############################

def main(event, line_bot_api, handler, incoming_msg, num): 
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
                players_arr.append(str(num) + '. ' + profile.display_name)
                players = '\n'.join(players_arr)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(str_curr + players))

            elif len(userid) > 0: # If players more than 0
                for x in range(len(userid)): 
                    print('Checking if he/she is a new user')
                    if profile.user_id != userid[x]: # If ada player baru
                        userid.append(profile.user_id)  
                        displayname.append(profile.display_name)
                        print('Add user ID: ' + profile.user_id)    
                        line_bot_api.push_message(profile.user_id, TextSendMessage(msg_join))

                        # Announce who are the players
                        # num = num + 1
                        players_arr.append(str(x+1) + '. ' + profile.display_name)
                        players = '\n'.join(players_arr)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(str_curr + players))
                        
                    elif profile.user_id == userid[x]:
                        print('Not a new player')
                        break
                    else: # If not a new player
                        print('?????')


            print('PLAYERS: ' + str(players_arr))

    
    if incoming_msg == '/startgame':
        if len(userid) >= 4 and len(userid) <= 6: # If total players antara 4-6
            print('player antara 4-6 players')
        elif len(userid) >= 7 and len(userid) <= 12: # If total players antara 7-12
            print('player antara 7-12 players')

        elif len(userid) < 4: # If players kurang dari 4
            line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you are too lonely (min 4 ppl)'))

        elif len(userid) > 12:  # If players lebih dari 12
            line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you guys are too crowded (max 12 ppl)'))
        
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('Werewolf is under maintenance :)'))



    # if incoming_msg == '/quit':

                