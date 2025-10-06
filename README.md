# leaguepedia_parser - Enhanced Edition

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Features](https://img.shields.io/badge/features-6_modules-green.svg)](#features)

A **comprehensive** Leaguepedia parser providing easy access to League of Legends esports data. This enhanced fork extends the original with extensive coverage of standings, champions, items, and roster changes.

## ✨ Features

**Enhanced beyond the original with:**
- 🏆 **Tournament Standings** - Team rankings, win rates, series/game statistics
- 🎮 **Champion Data** - All champions with attributes, stats, and filtering
- ⚔️ **Items Database** - Complete item catalog with stats and tier filtering  
- 👥 **Roster Changes** - Player transfers, team history, and timeline tracking

**Plus all original functionality:**
- 🎯 Games & match details with picks/bans
- 🏟️ Tournament & regional data
- 👤 Teams & player information

## Install

```bash
# With pip
pip install leaguepedia_parser_thomasbarrepitous

# With Poetry
poetry add leaguepedia_parser_thomasbarrepitous

# Quick verification
python -c "import leaguepedia_parser_thomasbarrepitous as lp; print('✅ Import successful')"
```

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

## 🎯 Common Use Cases

```python
# Tournament Analysis
standings = lp.get_tournament_standings("LCK/2024 Season/Summer Season")
top_team = standings[0].team
roster = lp.get_team_roster_changes(top_team)

# Meta Research  
marksmen = lp.get_champions_by_attributes("Marksman")
crit_items = lp.search_items_by_stat("Crit")

# Transfer Tracking
recent_moves = lp.get_recent_roster_changes(days=7)
team_additions = lp.get_roster_additions(team="T1")
```

## 📋 Data Types

| Module | Returns | Key Properties |
|--------|---------|----------------|
| **Games** | `Game`, `GameDetails` | teams, winner, date, picks_bans |
| **Standings** | `Standing` | team, place, win_rate, total_games |
| **Champions** | `Champion` | name, attributes, is_ranged, attack_range |
| **Items** | `Item` | name, tier, provides_ad/ap, total_cost |
| **Roster** | `RosterChange` | player, team, direction, is_addition |

## 📚 More Information

- **Examples**: Comprehensive usage examples in the [`tests` folder](https://github.com/thomasbarrepitous/leaguepedia_parser/tree/master/tests)
- **Development**: See [CLAUDE.md](CLAUDE.md) for development commands and setup
- **Original**: Based on [mrtolkien/leaguepedia_parser](https://github.com/mrtolkien/leaguepedia_parser)
- **Rate Limits**: Leaguepedia API has rate limits - the library handles basic throttling

## 🤝 Contributing

This enhanced fork welcomes contributions! Areas of interest:
- Additional data parsers (bans, statistics, etc.)
- Performance optimizations  
- Better error handling and retry logic
- Documentation improvements
