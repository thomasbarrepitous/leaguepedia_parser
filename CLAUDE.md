# Claude Code Documentation

## Development Commands

### Testing
```bash
# Install dependencies
poetry install

# Run all tests
poetry run python -m pytest tests/ -v

# Test specific modules
poetry run python -c "import leaguepedia_parser_thomasbarrepitous; print('Import successful')"
```

### Code Quality
```bash
# Format code with black
poetry run black leaguepedia_parser_thomasbarrepitous/

# Check code style
poetry run black --check leaguepedia_parser_thomasbarrepitous/
```

### Package Management
```bash
# Install new dependency
poetry add <package-name>

# Install development dependency
poetry add --group dev <package-name>

# Update dependencies
poetry update

# Show dependency tree
poetry show --tree
```

## Project Structure

```
leaguepedia_parser_thomasbarrepitous/
├── __init__.py                    # Main package exports
├── logger.py                      # Logging configuration
├── site/
│   └── leaguepedia.py            # Leaguepedia site connection
├── parsers/                       # Data extraction layer
│   ├── game_parser.py            # Game and tournament data
│   ├── team_parser.py            # Team data and assets
│   ├── player_parser.py          # Player information
│   └── tournament_roster_parser.py # Tournament rosters
└── transmuters/                   # Data transformation layer
    ├── field_names.py            # Field mapping constants
    ├── game.py                   # Game data transformation
    ├── game_players.py           # Player data transformation
    ├── picks_bans.py             # Draft data transformation
    └── tournament.py             # Tournament data transformation
```

## Common Issues & Solutions

### Import Errors
If you encounter `ModuleNotFoundError`, ensure you're using the Poetry environment:
```bash
poetry run python your_script.py
```

### Test Failures
The tests expect the package to be importable as `leaguepedia_parser`, but the actual package name is `leaguepedia_parser_thomasbarrepitous`. Update test imports accordingly.

### API Rate Limiting
The Leaguepedia API has rate limits. If you encounter issues:
1. Add delays between requests
2. Implement exponential backoff
3. Use the built-in pagination in `LeaguepediaSite.query()`

## Recent Fixes Applied

### Security & Reliability Improvements
1. **SQL Injection Prevention**: Escaped user inputs in query building (`game_parser.py:64-77`)
2. **Logger Fix**: Corrected logger name from `"leaguepedia_&arser"` to `"leaguepedia_parser"` (`logger.py:3`)
3. **Exception Handling**: Improved error handling with specific exception types and cycle detection (`team_parser.py:215-228`)
4. **Code Cleanup**: Removed test file `blabla.py`

### Development Best Practices
- Always use Poetry for dependency management
- Run tests before committing changes
- Follow the existing code style and patterns
- Add proper error handling for new API calls

## API Usage Examples

### Basic Usage
```python
import leaguepedia_parser_thomasbarrepitous as lp

# Get regions
regions = lp.get_regions()

# Get tournaments
tournaments = lp.get_tournaments("Korea", year=2020)

# Get games
games = lp.get_games("LCK/2020 Season/Spring Season")

# Get detailed game information
game_details = lp.get_game_details(games[0])

# Get team players
players = lp.get_active_players("T1")

# Get player information
player = lp.get_player_by_name("Faker")
```

### Error Handling
```python
try:
    players = lp.get_active_players("NonexistentTeam")
except ValueError as e:
    print(f"Team not found: {e}")
except RuntimeError as e:
    print(f"API error: {e}")
```