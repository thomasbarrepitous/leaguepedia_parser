# leaguepedia_parser

[![Generic badge](https://img.shields.io/github/workflow/status/mrtolkien/leaguepedia_parser/Python%20application)](https://shields.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A parser for Leaguepedia focused on accessing esports data including games, tournaments, standings, champions, items, and roster changes.

## Install

`pip install leaguepedia_parser_thomasbarrepitous`

## Demo

![Demo](https://raw.githubusercontent.com/mrtolkien/leaguepedia_parser/master/leaguepedia_parser_demo.gif)

## Usage

```python
import leaguepedia_parser_thomasbarrepitous as lp

# Games & Tournaments
regions = lp.get_regions()
# ['Korea', 'Europe', 'North America', 'China', ...]

tournaments = lp.get_tournaments("Korea", year=2020)
# [{'name': 'LCK/2020 Season/Spring Season', 'region': 'Korea'}, ...]

games = lp.get_games("LCK/2020 Season/Spring Season")
# [Game(team1='T1', team2='GenG', winner='T1', date='2020-02-05'), ...]

# Teams & Players  
logo_url = lp.get_team_logo('T1')
# 'https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/t1_logo.png'

players = lp.get_active_players('T1')
# [Player(name='Faker', role='Mid'), Player(name='Gumayusi', role='Bot'), ...]

# Standings
standings = lp.get_tournament_standings("LCK/2024 Season/Summer Season")
# [Standing(team='T1', place=1, win_series=16, loss_series=2), ...]

# Champions
champions = lp.get_champions_by_attributes("Marksman")
# [Champion(name='Jinx', attributes='Marksman', attack_range=525), ...]

champion = lp.get_champion_by_name("Jinx")
# Champion(name='Jinx', attributes='Marksman', attack_range=525, is_ranged=True)

# Items
ad_items = lp.get_ad_items()
# [Item(name='Infinity Edge', ad=70, total_cost=3400), ...]

infinity_edge = lp.get_item_by_name("Infinity Edge")
# Item(name='Infinity Edge', ad=70, crit=20, total_cost=3400, provides_ad=True)

# Roster Changes
roster_changes = lp.get_team_roster_changes("T1")
# [RosterChange(player='Faker', direction='Join', team='T1', date=2013-01-01), ...]

recent_moves = lp.get_recent_roster_changes(days=30)
# [RosterChange(player='Caps', direction='Leave', team='G2', date=2024-11-15), ...]
```

More usage examples can be found in the [`tests` folder](https://github.com/thomasbarrepitous/leaguepedia_parser/tree/master/tests).
