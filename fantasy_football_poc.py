#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 10:26:30 2019

@author: Zach
"""

import requests
import csv

def get_data():
#    event_ids = ["401013357","401013096","401014972","401022510","401013437","401019470","401013328"]
    HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/45.0.2454.101 Safari/537.36'),
                   'referer': 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/'
    }
    event_ids = []
    data_validation = [["passing","6"],["rushing","5"],["receiving","5"],["fumbles","3"],["defensive","7"],["interceptions","3"],["kickReturns","5"],["puntReturns","5"],["kicking","5"],["punting","6"]]
    data_header1 = ["season","week","event ID","team ID","team name","rank","score","winInd","firstDowns","thirdDownEff","fourthDownEff","totalYards","netPassingYards","completionAttempts","yardsPerPass","rushingYards","rushingAttempts","yardsPerRushAttempt","totalPenaltiesYards","turnovers","fumblesLost","interceptions","possessionTime","passing_C/ATT","passing_YDS","passing_AVG","passing_TD","passing_INT","passing_QBR","rushing_CAR","rushing_YDS","rushing_AVG","rushing_TD","rushing_LONG","receiving_REC","receiving_YDS","receiving_AVG","receiving_TD","receiving_LONG","fumbles_FUM","fumbles_LOST","fumbles_REC","defensive_TOT","defensive_SOLO","defensive_SACKS","defensive_TFL","defensive_PD","defensive_QB HUR","defensive_TD","interceptions_INT","interceptions_YDS","interceptions_TD","kickReturns_NO","kickReturns_YDS","kickReturns_AVG","kickReturns_LONG","kickReturns_TD","puntReturns_NO","puntReturns_YDS","puntReturns_AVG","puntReturns_LONG","puntReturns_TD","kicking_FG","kicking_PCT","kicking_LONG","kicking_XP","kicking_PTS","punting_NO","punting_YDS","punting_AVG","punting_TB","punting_In 20","punting_LONG"]
    week_days = [["0825","0830","0831","0901","0902","0903"],["0907","0908"],["0912","0913","0914","0915"],["0920","0921","0922"],["0927","0928","0929"],["1004","1005","1006"],["1009","1011","1012","1013"],["1018","1019","1020"],["1023","1025","1026","1027"],["1030","1031","1101","1102","1103"],["1106","1107","1108","1109","1110"],["1113","1114","1115","1116","1117"],["1120","1122","1123","1124"]]
#    week_days = [["0830"]]
    
    week_num = 0
    for week in week_days:
        week_num = week_num + 1
        print("")
        print("----------------------")
        print(week_num)
        print("----------------------")
        print("")
        for day in week:
            continuation = True
            while continuation:
                espn_url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=2018"+day+"&limit=100"
                count = 1
                r = requests.get(espn_url)
                if r.status_code == requests.codes.ok:
                    data = r.json()
                    events = data["events"]
                    for event in events:
                        event_id = event.get("id")
                        print(str(count) + ": " + event_id)
                        event_ids.append(event_id)
                        count = count + 1
                    continuation = False
                else:
                    print(r.status_code)
            continuation = True
                    
        continuation = True
        with open('2018_season_data.csv', mode='a+') as data_file:
            data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL) #QUOTE_MINIMAL
            if week_num == 1:
                data_writer.writerow(data_header1)
            for event_id in event_ids:
                while continuation:
                    espn_url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event="+str(event_id)
                    print(event_id)
                    r = requests.get(espn_url, headers=HEADERS)
                    if r.status_code == requests.codes.ok:
                        data = r.json()
                        boxscore = data["boxscore"]
                        players = boxscore["players"]
                        teams = boxscore["teams"]
                        header = data["header"]
                        competitions = header["competitions"]
                        
                        scores = []
                        for i in competitions:
                            competitors = i["competitors"]
                            for team in competitors:
                                team_scores = []
                                team_id = team.get("id")
                                team_score = team.get("score")
                                team_rank = team.get("rank")
#                                print(team_id)
#                                print(team_score)
#                                print(team_rank)
                                team_scores.append(team_id)
                                team_scores.append(team_score)
                                team_scores.append(team_rank)
                                scores.append(team_scores)
                        team_stats = []
                        for i in teams:
                            team_info = []
                            team_info_names = []
                            team_id = i["team"].get("id")
                            team_info.append(team_id)
                            for stat in i["statistics"]:
                                stat_name = stat.get("name")
                                stat_value = stat.get("displayValue")
                                team_info.append(stat_value)
                                team_info_names.append(stat_name)
#                            print(team_info_names)
                            team_stats.append(team_info)
                        
                        score_counter = 0
                        for i in players:
                            a_team_stats = []
#                            a_team_labels = []
#                            a_team_stat_name = []
                            team_name = i["team"].get("slug")
                            team_id = i["team"].get("id")
                            a_team_stats.append("2018")
                            a_team_stats.append(week_num)
                            a_team_stats.append(event_id)
                            a_team_stats.append(team_id)
                            a_team_stats.append(team_name)
                            for a_score in scores:
                                if a_score[0] == team_id:
                                    a_team_stats.append(a_score[2]) #rank
                                    a_team_stats.append(a_score[1]) #score
                                    print(score_counter)
                                    if score_counter == 0: #win (1) and loss (0)
                                        if int(scores[0][1]) > int(scores[1][1]):
                                            a_team_stats.append(0)
                                            print(scores[0][1] + ">" + scores[1][1])
                                        elif int(scores[0][1]) < int(scores[1][1]):
                                            a_team_stats.append(1)
                                            print(scores[0][1] + "<" + scores[1][1])
                                        else:
                                            a_team_stats.append(-1)
                                    else:
                                        if int(scores[0][1]) > int(scores[1][1]):
                                            a_team_stats.append(1)
                                            print(scores[0][1] + ">" + scores[1][1])
                                        elif int(scores[0][1]) < int(scores[1][1]):
                                            a_team_stats.append(0)
                                            print(scores[0][1] + "<" + scores[1][1])
                                        else:
                                            a_team_stats.append(-1)
                                    score_counter = score_counter + 1
                            for a_team in team_stats:
                                if a_team[0] == team_id:
                                    iter_team = iter(a_team)
                                    next(iter_team)
                                    for team_stat in iter_team:
                                        a_team_stats.append(team_stat)
#                            a_team_stat_name.append("")
#                            a_team_labels.append("")
                            print(team_name)
                            statistics = i["statistics"]
                            for z in statistics:
                                stat_name = z.get("name")
#                                stat_label = z.get("labels")
                                stat_total = z.get("totals")
                                #print(stat_name)
                                if stat_total == []:
#                                    print("found how to fix the issue")
                                    for valarray in data_validation:
                                        if valarray[0] == stat_name:
                                            for num in range(int(valarray[1])):
                                                a_team_stats.append(0)
                                else:
                                    for stat in stat_total:
                                        #print(stat)
                                        a_team_stats.append(stat)
#                                    for label in stat_label:
#                                        the_label = stat_name + "_" + label
#                                        a_team_stat_name.append(stat_name)
#                                        a_team_labels.append(the_label)
                            #print(a_team_stats)
#                            data_writer.writerow(a_team_labels)
                            print(len(a_team_stats))
                            data_writer.writerow(a_team_stats)
                            continuation = False
                    else:
                        print(r.status_code)
                continuation = True
        data_file.close()
        event_ids = []

#def get_eventids():
#    week_one_days = ["0825","0830","0831","0901","0902","0903"]
#    f = open("fantasy_football/2018_week1_eventids.txt", "w")
#
#    for day in week_one_days:
#        espn_url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=2018"+day+"&limit=100"
#        count = 1
#        r = requests.get(espn_url)
#        if r.status_code == requests.codes.ok:
#            data = r.json()
#            events = data["events"]
#            for event in events:
#                event_id = event.get("id")
#                print(str(count) + ": " + event_id)
#                f.write(event_id + "\n")
#                count = count + 1
#    f.close()

def main():
    #get_eventids()
    get_data()
main()















