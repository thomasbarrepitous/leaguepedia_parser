import pytest
import leaguepedia_parser


@pytest.mark.parametrize("team_tuple", [("tsm", "TSM"), ("IG", "Invictus Gaming")])
def test_get_long_team_name(team_tuple):
    assert leaguepedia_parser.get_long_team_name(team_tuple[0]) == team_tuple[1]


@pytest.mark.parametrize(
    "team_tournament",
    [("TSM", "LCS 2021 Summer"), ("TSM Academy", "NA Academy 2021 Summer")],
)
def test_get_long_team_name_in_tournament(team_tournament):
    team_name, tournament = team_tournament

    assert leaguepedia_parser.get_long_team_name("TSM", tournament) == team_name


def test_get_wrong_team_name():
    assert leaguepedia_parser.get_long_team_name("mister mv") is None


@pytest.mark.parametrize("team_name", ["T1", "G2 Esports"])
def test_get_team_logo(team_name):
    assert leaguepedia_parser.get_team_logo(team_name)
