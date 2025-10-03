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
tournaments = lp.get_tournaments("Korea", year=2020)
games = lp.get_games("LCK/2020 Season/Spring Season")
game_details = lp.get_game_details(games[0])

# Teams & Players  
logo_url = lp.get_team_logo('T1')
players = lp.get_active_players('T1')
player = lp.get_player_by_name('Faker')

# Standings
standings = lp.get_tournament_standings("LCK/2024 Season/Summer Season")
team_standings = lp.get_team_standings("T1")

# Champions
champions = lp.get_champions_by_attributes("Marksman")
ranged_champs = lp.get_ranged_champions()
champion = lp.get_champion_by_name("Jinx")

# Items
ad_items = lp.get_ad_items()
legendary_items = lp.get_items_by_tier("Legendary")
infinity_edge = lp.get_item_by_name("Infinity Edge")

# Roster Changes
roster_changes = lp.get_team_roster_changes("T1")
recent_moves = lp.get_recent_roster_changes(days=30)
additions = lp.get_roster_additions(team="G2 Esports")
```

More usage examples can be found in the [`tests` folder](https://github.com/thomasbarrepitous/leaguepedia_parser/tree/master/tests).
