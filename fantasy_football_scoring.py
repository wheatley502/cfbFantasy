#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 13:25:12 2019

@author: Zach
"""

import pandas as pd
import csv
import random
import math

def getTeamsInfo():
    data = pd.read_csv('2018_season_data.csv',header=0)
    team_IDs = data['team ID'].unique()
    team_names = data['team name'].unique()
    data_header1 = ["team ID","team name"]

    count = 0
    with open('team_lkp.csv', mode='w') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        data_writer.writerow(data_header1)
        for id in team_IDs:
            print(str(count) + ": " + str(id) + ": " + team_names[count])
            data_writer.writerow([id,team_names[count]])
            count = count + 1
    data_file.close()

def countTeamInstances():
    teams = pd.read_csv('team_lkp.csv',header=0)
    season = pd.read_csv('2018_season_data.csv',header=0)
    team_games_count = []
    data_header1 = ["team ID","team name"]
    
    count = 0
    for team in teams['team ID']:
        team_name = teams['team name'][count]
        game_count = len(season.loc[lambda df: season['team ID'] == team])
        team_games_count.append([team,team_name,game_count])
        count = count + 1
    team_games_count = sorted(team_games_count, key=lambda x: x[2], reverse=True)
    count = 1
    with open('draftable_teams.csv', mode='w') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        data_writer.writerow(data_header1)
        for team in team_games_count:
            if team[2] >= 11:
                data_writer.writerow([team[0],team[1]])
                print(str(count) + ": " + str(team[0]) + ": " + str(team[1]) + ": " + str(team[2]))
            count = count + 1
    data_file.close()
    
def theDraft():
    team_count = 8 #number of teams in the mock draft
    spots_per_team = 8 #number of positions on the team
    data_header1 = ["team number","memberTeam1","memberTeam2","memberTeam3","memberTeam4","memberTeam5","memberTeam6","memberTeam7","memberTeam8"]
    drafted_memberTeams = []
    draftable_teams = pd.read_csv('draftable_teams.csv',header=0)
    
    drafted_teams = 1
    
    with open('fantasy_teams.csv', mode='w') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        data_writer.writerow(data_header1)
        while drafted_teams <= team_count:
            fantasy_team = []
            team_number = drafted_teams
            fantasy_team.append(team_number)
            drafted_memberTeams_count = 0
            while drafted_memberTeams_count < spots_per_team:
                team_index = random.randint(1,129)
                while team_index in drafted_memberTeams:
                    team_index = random.randint(1,129)
                drafted_memberTeams.append(team_index)
                drafted_team = draftable_teams.loc[team_index]
                team_name = drafted_team['team name']
                team_id = drafted_team['team ID']
                print(str(drafted_teams) + ": " + str(drafted_memberTeams_count) + ": " + str(team_name))
                fantasy_team.append(team_id)
                drafted_memberTeams_count = drafted_memberTeams_count + 1
            data_writer.writerow(fantasy_team)
            drafted_teams = drafted_teams + 1
            
def create_matchups():
    print("creating matchups")
#    data_header1 = ["week_num","home team number","visitor team number"]
#    max_week_num = 10
    teams = pd.read_csv('fantasy_teams.csv',header=0)
    division1 = []
    division2 = []
    teams_per_division = len(teams) / 2
    count = 0
    for team in teams['team number']:
        if count < teams_per_division:
            division1.append(team)
        else:
            division2.append(team)
        count = count + 1
    print("D1:")
    print(division1)
    print("D2:")
    print(division2)
    
#    with open('fantasy_teams.csv', mode='w') as data_file:
#        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
#        data_writer.writerow(data_header1)
#        week_num = 1
#        while week_num <= max_week_num:
#            if week < teams_per_division:
#                game1 = [division1[0],division1[1]]
#                game2 = [division1[],division1[week_num]]

def scoring():
    print("scoring")
    max_week_num = 13
#    teams_info = pd.read_csv('fantasy_teams.csv',header=0)
#    matchups = pd.read_csv('fantasy_matchups.csv',header=0)
    season_data = pd.read_csv('2018_season_data.csv',header=0)
    data_header1 = ["team ID","week","passing score","rushing score","win score","defense score","first down","special teams","total score"]
    week_num = 1
    with open('fantasy_teams_scores.csv', mode='w') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        data_writer.writerow(data_header1)
        while week_num <= max_week_num:
            week_data = season_data.loc[lambda df: season_data['week'] == week_num]
            for team in week_data['team ID']:
#            week_matchups = matchups.loc[lambda df: matchups['week number'] == week_num]
#            week_data = season_data.loc[lambda df: season_data['week'] == week_num]
#            for team in teams_info['team number']:
#                team_members = teams_info.loc[lambda df: teams_info['team number'] == team]
                #calculate passing score based on first team in lineup
#                team_member_id = team_members['memberTeam1'].values[0]
                team_member_id = team
                team_score_data = []
                team_score_data.append(team_member_id)
                team_score_data.append(week_num)
#                print('team number: ' + str(team))
                print('team ID: ' + str(team_member_id) + ' - week: ' + str(week_num))
                win_score = 0
                passing_score = 0
                rushing_score = 0
                team_blank_ind = season_data[(season_data['week'] == week_num) & (season_data['team ID'] == team_member_id)][['winInd']]['winInd'].values[0]
                
                if team_blank_ind != -1:
                    passing_data = season_data[(season_data['week'] == week_num) & (season_data['team ID'] == team_member_id)][['netPassingYards','completionAttempts','passing_TD','passing_INT']]
                    if passing_data.empty:
                        print("Bye Week LOL!")
                    else:
                        passingYards = int(passing_data['netPassingYards'].values[0])
                        completionAttempts = passing_data['completionAttempts'].values[0].split('-')
                        completionPercentage = round(float(completionAttempts[0])/float(completionAttempts[1]),2)
                        passingTD = int(passing_data['passing_TD'].values[0])
                        passingINT = int(passing_data['passing_INT'].values[0])
                
                        passing_score = (passingYards * 0.05) + (completionPercentage * 5) + (passingTD * 6) + (passingINT * -2)
#                        print('passing score: ' + str(passing_score))
                        team_score_data.append(passing_score)
            
                    rushing_data = season_data[(season_data['week'] == week_num) & (season_data['team ID'] == team_member_id)][['rushingYards','rushingAttempts','rushing_TD']]
                    if rushing_data.empty:
                        print("Bye Week LOL!")
                    else:
                        rushingYards = int(rushing_data['rushingYards'].values[0])
                        rushingAttempts = int(rushing_data['rushingAttempts'].values[0])
                        rushing_TD = int(rushing_data['rushing_TD'].values[0])
                            
                        rushing_score = (rushingYards * 0.05) + (rushingAttempts * 0.01) + (rushing_TD * 6)
#                        print('rushing score: ' + str(rushing_score))
                        team_score_data.append(rushing_score)
            
                    win_data = season_data[(season_data['week'] == week_num) & (season_data['team ID'] == team_member_id)][['event ID','winInd','rank','score']]
                    if win_data.empty:
                        print("Bye Week LOL!")
                    else:
                        event_id = win_data['event ID'].values[0]
                        opp_win_data = season_data[(season_data['week'] == week_num) & (season_data['event ID'] == event_id) & (season_data['team ID'] != team_member_id)][['event ID','team name','winInd','rank','score']]
#                        print(opp_win_data)
                        win_ind = int(win_data['winInd'].values[0])
                        rank = win_data['rank'].values[0]
                        score = int(win_data['score'].values[0])
                        opp_rank = opp_win_data['rank'].values[0]
                        opp_score = int(opp_win_data['score'].values[0])
                        rank_ind = 0
                        if not math.isnan(opp_rank) and win_ind == 1 and not math.isnan(rank): 
                            rank_ind = 1.5
                        elif not math.isnan(opp_rank) and win_ind == 1 and math.isnan(rank):
                            rank_ind = 2.5
                        elif math.isnan(opp_rank) and win_ind == 0 and not math.isnan(rank):
                            rank_ind = -2.5
                
                        if win_ind == 0:
                            win_ind = -1
                
                        win_score = (win_ind * 5) + ((score - opp_score) * 0.2) + (rank_ind * 2)
#                        print('win score: ' + str(win_score))
                        team_score_data.append(win_score)
                
                    deff_eff_data = season_data[(season_data['week'] == week_num) & (season_data['team ID'] == team_member_id)][['event ID','defensive_SACKS','defensive_TD','fumbles_FUM','fumbles_REC','interceptions_INT','interceptions_TD','interceptions_YDS']]
                    if deff_eff_data.empty:
                        print("Bye Week LOL!")
                    else:
                        event_id = int(deff_eff_data['event ID'].values[0])
                        opp_offense_data = season_data[(season_data['week'] == week_num) & (season_data['event ID'] == event_id) & (season_data['team ID'] != team_member_id)][['netPassingYards','rushingYards']]
                        sacks = int(deff_eff_data['defensive_SACKS'].values[0])
                        deff_TD = int(deff_eff_data['defensive_TD'].values[0])
                        fumbles_caused = int(deff_eff_data['fumbles_FUM'].values[0])
                        fumbles_rec = int(deff_eff_data['fumbles_REC'].values[0])
                        interceptions_num = int(deff_eff_data['interceptions_INT'].values[0])
                        interceptions_TD = int(deff_eff_data['interceptions_TD'].values[0])
                        interceptions_yards = int(deff_eff_data['interceptions_YDS'].values[0])
                        opp_rushing = int(opp_offense_data['rushingYards'].values[0])
                        opp_passing = int(opp_offense_data['netPassingYards'].values[0])
#                        opp_rushing_score = 0
#                        opp_passing_score = 0
                        
                        deff_eff_score = (sacks * 1) + (deff_TD * 6) + (fumbles_caused * 1) + (fumbles_rec * 1) + (interceptions_num * 1) + (interceptions_TD * 6) + (interceptions_yards * 0.05) + (opp_rushing * -0.017) + (opp_passing * -0.017)
                        team_score_data.append(deff_eff_score)
                        
                    first_down_data = season_data[(season_data['week'] == week_num) & (season_data['team ID'] == team_member_id)][['firstDowns','thirdDownEff','fourthDownEff']]
                    if first_down_data.empty:
                        print("Bye Week LOL!")
                    else:
                        first_downs = int(first_down_data['firstDowns'].values[0])
                        third_eff = first_down_data['thirdDownEff'].values[0].split('-')
                        third_eff_per = round(float(third_eff[0]) / float(third_eff[1]),2) if float(third_eff[1]) != 0 else 0
                        fourth_eff = first_down_data['fourthDownEff'].values[0].split('-')
                        fourth_eff_per = round(float(fourth_eff[0]) / float(fourth_eff[1]),2) if float(fourth_eff[1]) != 0 else 0
                        
                        first_down_score = (first_downs * 0.1) + (third_eff_per * 10) + (fourth_eff_per * 10)
                        team_score_data.append(first_down_score)
                        
                    special_teams_data = season_data[(season_data['week'] == week_num) & (season_data['team ID'] == team_member_id)][['kicking_LONG','kicking_PTS','punting_YDS','kicking_FG','kickReturns_YDS','kickReturns_TD','puntReturns_YDS','puntReturns_TD']]
                    if special_teams_data.empty:
                        print("Bye Week LOL!")
                    else:
                        kicking_long = int(special_teams_data['kicking_LONG'].values[0])
                        kicking_pts = int(special_teams_data['kicking_PTS'].values[0])
                        kicking_fg = special_teams_data['kicking_FG'].values[0].split('/')
                        kicking_fg_per = 0
                        try:
                            kicking_fg_per = round(float(kicking_fg[0]) / float(kicking_fg[1]),2) if float(kicking_fg[1]) != 0 else 0
                        except:
                            print("not good")
                        punting_yards = int(special_teams_data['punting_YDS'].values[0])
                        punting_return_yards = int(special_teams_data['puntReturns_YDS'].values[0])
                        punting_return_td = int(special_teams_data['puntReturns_TD'].values[0])
                        kick_return_yards = int(special_teams_data['kickReturns_YDS'].values[0])
                        kick_return_td = int(special_teams_data['kickReturns_TD'].values[0])
                        
                        special_teams_score = (kicking_long * 0.02) + (kicking_pts * 0.2) + (kicking_fg_per * 5) + (punting_yards * 0.05) + (punting_return_yards * 0.02) + (punting_return_td * 6) + (kick_return_yards * 0.02) + (kick_return_td * 6)
                        team_score_data.append(special_teams_score)
                        
                total_score = rushing_score + passing_score + win_score + deff_eff_score + first_down_score + special_teams_score
                team_score_data.append(total_score)
                data_writer.writerow(team_score_data)
            week_num = week_num + 1
    data_file.close()
    
def combine_scores():
    fantasy_scores = pd.read_csv('fantasy_teams_scores.csv',header=0)
    teams_info = pd.read_csv('fantasy_teams.csv',header=0)
    matchups = pd.read_csv('fantasy_matchups.csv',header=0)
    
    data_header1 = ["match ID","team ID","passing score","rushing score","win score","defense score","first down","special teams","total score"]
    with open('fantasy_combined_scores.csv', mode='w') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        data_writer.writerow(data_header1)
        for matchID in matchups['match ID']:
            matchup_info = matchups.loc[lambda df: matchups['match ID'] == matchID]
            week_num = int(matchup_info['week number'].values[0])
            team1 = int(matchup_info['team1'].values[0])
            print(str(week_num) + " - " + str(team1))
            team1_scores = []
            team1_scores.append(matchID)
            team1_scores.append(team1)
            team1_members = teams_info.loc[lambda df: teams_info['team number'] == team1]
            team2 = int(matchup_info['team2'].values[0])
            print(str(week_num) + " - " + str(team2))
            team2_scores = []
            team2_scores.append(matchID)
            team2_scores.append(team2)
            team2_members = teams_info.loc[lambda df: teams_info['team number'] == team2]
        
            #passing score
            team1_passing_member = int(team1_members['memberTeam1'].values[0])
            team1_passing_score = 0.0
            team1_passing_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team1_passing_member)][['passing score']]['passing score']
            if not team1_passing_array.empty: team1_passing_score = float(team1_passing_array.values[0])
            team1_scores.append(team1_passing_score)
            
            team2_passing_member = int(team2_members['memberTeam1'].values[0])
            team2_passing_score = 0.0
            team2_passing_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team2_passing_member)][['passing score']]['passing score']            
            if not team2_passing_array.empty: team2_passing_score = float(team2_passing_array.values[0])
            team2_scores.append(team2_passing_score)
            
            #rushing score	
            team1_rushing_member = int(team1_members['memberTeam2'].values[0])
            team1_rushing_score = 0.0
            team1_rushing_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team1_rushing_member)][['rushing score']]['rushing score']
            if not team1_rushing_array.empty: team1_rushing_score = float(team1_rushing_array.values[0])            
            team1_scores.append(team1_rushing_score)
            
            team2_rushing_member = int(team2_members['memberTeam2'].values[0])
            team2_rushing_score = 0.0
            team2_rushing_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team2_rushing_member)][['rushing score']]['rushing score']
            if not team2_rushing_array.empty: team2_rushing_score = float(team2_rushing_array.values[0])            
            team2_scores.append(team2_rushing_score)
            
            #win score	
            team1_win_member = int(team1_members['memberTeam3'].values[0])
            team1_win_score = 0.0
            team1_win_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team1_win_member)][['win score']]['win score']
            if not team1_win_array.empty: team1_win_score = float(team1_win_array.values[0])
            team1_scores.append(team1_win_score)
            
            team2_win_member = int(team2_members['memberTeam3'].values[0])
            team2_win_score = 0.0
            team2_win_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team2_win_member)][['win score']]['win score']
            if not team2_win_array.empty: team2_win_score = float(team2_win_array.values[0])
            team2_scores.append(team2_win_score)
            
            #defense score
            team1_defense_member = int(team1_members['memberTeam4'].values[0])
            team1_defense_score = 0.0
            team1_defense_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team1_defense_member)][['defense score']]['defense score']
            if not team1_defense_array.empty: team1_defense_score = float(team1_defense_array.values[0])
            team1_scores.append(team1_defense_score)
            
            team2_defense_member = int(team2_members['memberTeam4'].values[0])
            team2_defense_score = 0.0
            team2_defense_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team2_defense_member)][['defense score']]['defense score']
            if not team2_defense_array.empty: team2_defense_score = float(team2_defense_array.values[0])
            team2_scores.append(team2_defense_score)
            
            #first down
            team1_firstdown_member = int(team1_members['memberTeam5'].values[0])
            team1_firstdown_score = 0.0
            team1_firstdown_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team1_firstdown_member)][['first down']]['first down']
            if not team1_firstdown_array.empty: team1_firstdown_score = float(team1_firstdown_array.values[0])
            team1_scores.append(team1_firstdown_score)
            
            team2_firstdown_member = int(team2_members['memberTeam5'].values[0])
            team2_firstdown_score = 0.0
            team2_firstdown_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team2_firstdown_member)][['first down']]['first down']
            if not team2_firstdown_array.empty: team2_firstdown_score = float(team2_firstdown_array.values[0])
            team2_scores.append(team2_firstdown_score)
            
            #special teams
            team1_special_member = int(team1_members['memberTeam6'].values[0])
            team1_special_score = 0.0
            team1_special_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team1_special_member)][['special teams']]['special teams']
            if not team1_special_array.empty: team1_special_score = float(team1_special_array.values[0])
            team1_scores.append(team1_special_score)
            
            team2_special_member = int(team2_members['memberTeam6'].values[0])
            team2_special_score = 0.0
            team2_special_array = fantasy_scores[(fantasy_scores['week'] == week_num) & (fantasy_scores['team ID'] == team2_special_member)][['special teams']]['special teams']
            if not team2_special_array.empty: team2_special_score = float(team2_special_array.values[0])
            team2_scores.append(team2_special_score)
            
            #total scores
            team1_total = team1_passing_score + team1_rushing_score + team1_win_score + team1_defense_score + team1_firstdown_score + team1_special_score
            team1_scores.append(team1_total)
            data_writer.writerow(team1_scores)
            
            team2_total = team2_passing_score + team2_rushing_score + team2_win_score + team2_defense_score + team2_firstdown_score + team2_special_score
            team2_scores.append(team2_total)
            data_writer.writerow(team2_scores)
    data_file.close()
    
def count_wins():
    team_scores = pd.read_csv('fantasy_combined_scores.csv',header=0)
    
    data_header1 = ["team ID","wins","losses"]
    with open('fantasy_teams_records.csv', mode='w') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        data_writer.writerow(data_header1)
        for team_id in range(1,9):
            matchup_ids = team_scores[(team_scores['team ID'] == team_id)][['match ID']]['match ID']
            wins = 0.0
            losses = 0.0
            for match_id in matchup_ids:
                team_score = float(team_scores[(team_scores['team ID'] == team_id) & (team_scores['match ID'] == match_id)][['total score']]['total score'].values[0])
                opp_score = float(team_scores[(team_scores['team ID'] != team_id) & (team_scores['match ID'] == match_id)][['total score']]['total score'].values[0])
                
                if team_score > opp_score:
                    wins = wins + 1
                elif team_score < opp_score:
                    losses = losses + 1
                else:
                    wins = wins + 0.5
                    losses = losses + 0.5
            print(str(team_id) + ": " + str(wins) + "-" + str(losses))
            data_writer.writerow([team_id,wins,losses])
    data_file.close()
    

def main():
    print("starting")
#    getTeamsInfo()
#    countTeamInstances()
    theDraft()
#    create_matchups()
#    scoring()
    combine_scores()
    count_wins()
    print("end")
main()








