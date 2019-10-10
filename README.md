# cfbFantasy

### Python File Descriptions:
1) fantasy_football_poc.py -> Will gather data from ESPN API. Creates a csv with the data
2) fantasy_football_scoring.py -> Holds several different functions. In the current form, if you ran the main class, it would hold a "draft" which 8 players draft 8 teams, calculate the combined scores for all of the teams and then generate the teams end of season records.

### CSV File Descriptions:
1) 2018_season_data.csv -> Holds all of the teams data from ESPN for the 2018 season
2) fantasy_teams_scores.csv -> Scores all of the data for every team in the 2018_season_data for every game played by team in the 2018 season.
3) draftable_teams.csv -> a list of all teams which played at least 11 games in the 2018 season
4) fantasy_teams.csv -> Produced after the "draft". Holds all of the fantasy teams and the college teams associated with them.
5) fantasy_matchup.csv -> all of the matchups for the 2018 fantasy season. 8 teams broken into two leagues. Every team playes one another once and plays teams in their league twice.
6) fantasy_combined_scores.csv -> Each fantasy team's scores from the teams that have played that week. This has the team's total score for the week.
7) fantasy_teams_records.csv -> The wins and losses for a given fantasy team during the "season".

### Scoring Information:
This application generates scores in 6 different areas. Each of the different scores has several metrics which go into the scoring of each one. Below is the list of scores and th ecode to generate them:
- Rushing Yards
```
rushing_score = (rushingYards * 0.05) + (rushingAttempts * 0.01) + (rushing_TD * 6)
```
- Passing Yards
```
passing_score = (passingYards * 0.05) + (completionPercentage * 5) + (passingTD * 6) + (passingINT * -2)
```
- First Downs
```
first_down_score = (first_downs * 0.1) + (third_eff_per * 10) + (fourth_eff_per * 10)
```
- Wins
```
win_score = (win_ind * 5) + ((score - opp_score) * 0.2) + (rank_ind * 2)
```
- Defensive Efficiency
```
deff_eff_score = (sacks * 1) + (deff_TD * 6) + (fumbles_caused * 1) + (fumbles_rec * 1) + (interceptions_num * 1) + (interceptions_TD * 6) + (interceptions_yards * 0.05) + (opp_rushing * -0.017) + (opp_passing * -0.017)
```
- Special Teams
```
special_teams_score = (kicking_long * 0.02) + (kicking_pts * 0.2) + (kicking_fg_per * 5) + (punting_yards * 0.05) + (punting_return_yards * 0.02) + (punting_return_td * 6) + (kick_return_yards * 0.02) + (kick_return_td * 6)
```
