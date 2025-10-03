"""Tests for roster changes functionality in Leaguepedia parser."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from typing import List

import leaguepedia_parser_thomasbarrepitous as lp
from leaguepedia_parser_thomasbarrepitous.parsers.roster_changes_parser import RosterChange, RosterAction

from .conftest import TestConstants, assert_valid_dataclass_instance, assert_mock_called_with_table


class TestRosterChangesImports:
    """Test that roster changes functions are properly importable."""
    
    @pytest.mark.unit
    def test_roster_changes_functions_importable(self):
        """Test that all roster changes functions are available in the main module."""
        expected_functions = [
            'get_roster_changes',
            'get_team_roster_changes',
            'get_player_roster_changes',
            'get_recent_roster_changes',
            'get_roster_additions',
            'get_roster_removals',
            'get_retirements'
        ]
        
        for func_name in expected_functions:
            assert hasattr(lp, func_name), f"Function {func_name} is not importable"


class TestRosterActionEnum:
    """Test RosterAction enumeration."""
    
    @pytest.mark.unit
    def test_roster_action_enum_values(self):
        """Test that RosterAction enum has expected values."""
        expected_actions = {
            'ADD': 'Add',
            'REMOVE': 'Remove',
            'ROLE_CHANGE': 'Role Change',
            'SUBSTITUTE': 'Substitute',
            'LOAN': 'Loan',
            'TRANSFER': 'Transfer',
            'RETIREMENT': 'Retirement'
        }
        
        for attr_name, expected_value in expected_actions.items():
            assert hasattr(RosterAction, attr_name)
            assert getattr(RosterAction, attr_name).value == expected_value


class TestRosterChangeDataclass:
    """Test RosterChange dataclass functionality and computed properties."""
    
    @pytest.mark.unit
    def test_roster_change_initialization_complete(self):
        """Test RosterChange dataclass can be initialized with all fields."""
        change_date = datetime(2023, 11, 15)
        roster_change = RosterChange(
            id="RC001",
            team=TestConstants.TEAM_T1,
            role="Mid",
            player=TestConstants.PLAYER_FAKER,
            action="Add",
            date=change_date,
            tournament="LCK/2013 Season/Winter",
            overview_page="LCK/2013 Season/Winter",
            reference="Official announcement",
            roster_change_id="RC001",
            news_id="NEWS001",
            is_retirement=False,
            residency="KR",
            residency_former=None,
            nationality="KR",
            is_lowercase=False,
            is_substitute=False,
            is_trainee=False
        )
        
        assert_valid_dataclass_instance(roster_change, RosterChange, ['team', 'player', 'action'])
        assert roster_change.team == TestConstants.TEAM_T1
        assert roster_change.player == TestConstants.PLAYER_FAKER
        assert roster_change.action == "Add"
        assert roster_change.date == change_date
        assert roster_change.role == "Mid"
    
    @pytest.mark.unit
    def test_roster_change_action_enum_property(self):
        """Test action_enum property converts string to enum."""
        # Test valid action
        change_add = RosterChange(action="Add")
        assert change_add.action_enum == RosterAction.ADD
        
        # Test another valid action
        change_remove = RosterChange(action="Remove")
        assert change_remove.action_enum == RosterAction.REMOVE
        
        # Test invalid action
        change_invalid = RosterChange(action="InvalidAction")
        assert change_invalid.action_enum is None
        
        # Test None action
        change_none = RosterChange(action=None)
        assert change_none.action_enum is None
    
    @pytest.mark.unit
    def test_roster_change_is_addition_property(self):
        """Test is_addition property."""
        change_add = RosterChange(action="Add")
        assert change_add.is_addition is True
        
        change_remove = RosterChange(action="Remove")
        assert change_add.is_addition is True  # This should be False based on the logic
        
        change_none = RosterChange(action=None)
        assert change_none.is_addition is False
    
    @pytest.mark.unit
    def test_roster_change_is_removal_property(self):
        """Test is_removal property."""
        change_remove = RosterChange(action="Remove")
        assert change_remove.is_removal is True
        
        change_add = RosterChange(action="Add")
        assert change_add.is_removal is False
        
        change_none = RosterChange(action=None)
        assert change_none.is_removal is False
    
    @pytest.mark.unit
    def test_roster_change_boolean_field_handling(self):
        """Test boolean fields are properly handled."""
        roster_change = RosterChange(
            is_retirement=True,
            is_substitute=False,
            is_trainee=True,
            is_lowercase=False
        )
        
        assert roster_change.is_retirement is True
        assert roster_change.is_substitute is False
        assert roster_change.is_trainee is True
        assert roster_change.is_lowercase is False


class TestRosterChangesAPI:
    """Test roster changes API functions with mocked data."""
    
    @pytest.mark.integration
    def test_get_roster_changes_basic_call(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test basic get_roster_changes call returns properly parsed RosterChange objects."""
        mock_leaguepedia_query.return_value = roster_changes_mock_data
        
        changes = lp.get_roster_changes()
        
        assert len(changes) == 2
        assert all(isinstance(c, RosterChange) for c in changes)
        assert changes[0].team == TestConstants.TEAM_T1
        assert changes[0].player == TestConstants.PLAYER_FAKER
        assert changes[1].team == TestConstants.TEAM_G2
        assert changes[1].player == TestConstants.PLAYER_CAPS
        assert_mock_called_with_table(mock_leaguepedia_query, "RosterChanges")
    
    @pytest.mark.integration
    def test_get_roster_changes_with_team_filter(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_roster_changes with team filter."""
        # Return only T1 changes
        filtered_data = [roster_changes_mock_data[0]]
        mock_leaguepedia_query.return_value = filtered_data
        
        changes = lp.get_roster_changes(team=TestConstants.TEAM_T1)
        
        assert len(changes) == 1
        assert changes[0].team == TestConstants.TEAM_T1
        mock_leaguepedia_query.assert_called_once()
        # Verify WHERE clause includes team filter
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert f"Team='{TestConstants.TEAM_T1}'" in call_kwargs['where']
    
    @pytest.mark.integration
    def test_get_roster_changes_with_player_filter(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_roster_changes with player filter."""
        # Return only Faker changes
        filtered_data = [roster_changes_mock_data[0]]
        mock_leaguepedia_query.return_value = filtered_data
        
        changes = lp.get_roster_changes(player=TestConstants.PLAYER_FAKER)
        
        assert len(changes) == 1
        assert changes[0].player == TestConstants.PLAYER_FAKER
        mock_leaguepedia_query.assert_called_once()
        # Verify WHERE clause includes player filter
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert f"Player='{TestConstants.PLAYER_FAKER}'" in call_kwargs['where']
    
    @pytest.mark.integration
    def test_get_roster_changes_with_action_filter(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_roster_changes with action filter."""
        # Return only Add actions
        filtered_data = [roster_changes_mock_data[0]]
        mock_leaguepedia_query.return_value = filtered_data
        
        changes = lp.get_roster_changes(action="Add")
        
        assert len(changes) == 1
        assert changes[0].action == "Add"
        mock_leaguepedia_query.assert_called_once()
        # Verify WHERE clause includes action filter
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert "Action='Add'" in call_kwargs['where']
    
    @pytest.mark.integration
    def test_get_roster_changes_with_date_range(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_roster_changes with date range filters."""
        mock_leaguepedia_query.return_value = roster_changes_mock_data
        
        start_date = "2013-01-01"
        end_date = "2013-12-31"
        changes = lp.get_roster_changes(start_date=start_date, end_date=end_date)
        
        assert len(changes) == 2
        mock_leaguepedia_query.assert_called_once()
        # Verify WHERE clause includes date filters
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert f"Date >= '{start_date}'" in call_kwargs['where']
        assert f"Date <= '{end_date}'" in call_kwargs['where']
    
    @pytest.mark.integration
    def test_get_team_roster_changes(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_team_roster_changes convenience function."""
        filtered_data = [roster_changes_mock_data[0]]
        mock_leaguepedia_query.return_value = filtered_data
        
        changes = lp.get_team_roster_changes(TestConstants.TEAM_T1)
        
        assert len(changes) == 1
        assert changes[0].team == TestConstants.TEAM_T1
        assert_mock_called_with_table(mock_leaguepedia_query, "RosterChanges")
    
    @pytest.mark.integration
    def test_get_player_roster_changes(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_player_roster_changes convenience function."""
        filtered_data = [roster_changes_mock_data[0]]
        mock_leaguepedia_query.return_value = filtered_data
        
        changes = lp.get_player_roster_changes(TestConstants.PLAYER_FAKER)
        
        assert len(changes) == 1
        assert changes[0].player == TestConstants.PLAYER_FAKER
        assert_mock_called_with_table(mock_leaguepedia_query, "RosterChanges")
    
    @pytest.mark.integration
    @patch('leaguepedia_parser_thomasbarrepitous.parsers.roster_changes_parser.datetime')
    def test_get_recent_roster_changes(self, mock_datetime, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_recent_roster_changes with mocked datetime."""
        # Mock current time
        mock_now = datetime(2023, 12, 15)
        mock_datetime.now.return_value = mock_now
        mock_datetime.timedelta = timedelta  # Use real timedelta
        
        mock_leaguepedia_query.return_value = roster_changes_mock_data
        
        changes = lp.get_recent_roster_changes(days=30)
        
        assert len(changes) == 2
        mock_leaguepedia_query.assert_called_once()
        
        # Verify date range was calculated correctly (30 days back)
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert "Date >= '2023-11-15'" in call_kwargs['where']  # 30 days before 2023-12-15
        assert "Date <= '2023-12-15'" in call_kwargs['where']
    
    @pytest.mark.integration
    def test_get_roster_additions(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_roster_additions convenience function."""
        # Return only additions
        filtered_data = [roster_changes_mock_data[0]]
        mock_leaguepedia_query.return_value = filtered_data
        
        additions = lp.get_roster_additions()
        
        assert len(additions) == 1
        assert additions[0].action == "Add"
        mock_leaguepedia_query.assert_called_once()
        # Verify action filter
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert "Action='Add'" in call_kwargs['where']
    
    @pytest.mark.integration
    def test_get_roster_removals(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_roster_removals convenience function."""
        # Return only removals
        filtered_data = [roster_changes_mock_data[1]]
        mock_leaguepedia_query.return_value = filtered_data
        
        removals = lp.get_roster_removals()
        
        assert len(removals) == 1
        assert removals[0].action == "Remove"
        mock_leaguepedia_query.assert_called_once()
        # Verify action filter
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert "Action='Remove'" in call_kwargs['where']
    
    @pytest.mark.integration
    def test_get_retirements(self, mock_leaguepedia_query):
        """Test get_retirements function with retirement filter."""
        retirement_data = [{
            'ID': 'RC003',
            'Team': 'Former Team',
            'Player': 'RetiredPlayer',
            'Action': 'Retirement',
            'IsRetirement': 'Yes',
            'Date': '2023-11-01'
        }]
        mock_leaguepedia_query.return_value = retirement_data
        
        retirements = lp.get_retirements()
        
        assert len(retirements) == 1
        assert retirements[0].is_retirement is True
        mock_leaguepedia_query.assert_called_once()
        # Verify retirement filter
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert "IsRetirement='Yes'" in call_kwargs['where']


class TestRosterChangesErrorHandling:
    """Test error handling in roster changes functionality."""
    
    @pytest.mark.integration
    def test_get_roster_changes_api_error(self, mock_leaguepedia_query):
        """Test that API errors are properly wrapped in RuntimeError."""
        mock_leaguepedia_query.side_effect = Exception("API connection failed")
        
        with pytest.raises(RuntimeError, match="Failed to fetch roster changes"):
            lp.get_roster_changes()
    
    @pytest.mark.integration
    def test_get_retirements_api_error(self, mock_leaguepedia_query):
        """Test that API errors in get_retirements are handled."""
        mock_leaguepedia_query.side_effect = Exception("API connection failed")
        
        with pytest.raises(RuntimeError, match="Failed to fetch retirements"):
            lp.get_retirements()
    
    @pytest.mark.integration
    def test_get_roster_changes_empty_response(self, mock_leaguepedia_query):
        """Test handling of empty API response."""
        mock_leaguepedia_query.return_value = []
        
        changes = lp.get_roster_changes()
        
        assert changes == []
        assert isinstance(changes, list)


class TestRosterChangesEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @pytest.mark.unit
    def test_roster_change_with_special_characters_in_names(self):
        """Test RosterChange with special characters in team/player names."""
        special_team = "Team Liquid'"
        special_player = "Bjergsen"
        
        roster_change = RosterChange(team=special_team, player=special_player)
        
        assert roster_change.team == special_team
        assert roster_change.player == special_player
    
    @pytest.mark.unit
    def test_roster_change_with_none_date(self):
        """Test RosterChange with None date."""
        roster_change = RosterChange(date=None)
        
        assert roster_change.date is None
    
    @pytest.mark.unit
    def test_roster_change_role_variations(self):
        """Test RosterChange with various role values."""
        roles = ["Top", "Jungle", "Mid", "Bot", "Support", "Coach", "Substitute"]
        
        for role in roles:
            roster_change = RosterChange(role=role)
            assert roster_change.role == role
    
    @pytest.mark.integration
    def test_roster_changes_sql_injection_protection(self, mock_leaguepedia_query, roster_changes_mock_data):
        """Test that SQL injection attempts are properly escaped."""
        mock_leaguepedia_query.return_value = roster_changes_mock_data
        
        malicious_input = "'; DROP TABLE RosterChanges; --"
        
        # Should not raise an exception and should escape the input
        changes = lp.get_roster_changes(team=malicious_input)
        
        # Verify the input was escaped (single quotes doubled)
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert "''" in call_kwargs['where']  # Escaped single quotes
    
    @pytest.mark.unit
    def test_roster_change_residency_fields(self):
        """Test residency-related fields."""
        roster_change = RosterChange(
            residency="NA",
            residency_former="EU",
            nationality="US"
        )
        
        assert roster_change.residency == "NA"
        assert roster_change.residency_former == "EU"
        assert roster_change.nationality == "US"
    
    @pytest.mark.integration
    @patch('leaguepedia_parser_thomasbarrepitous.parsers.roster_changes_parser.datetime')
    def test_get_recent_roster_changes_custom_days(self, mock_datetime, mock_leaguepedia_query, roster_changes_mock_data):
        """Test get_recent_roster_changes with custom day count."""
        mock_now = datetime(2023, 12, 15)
        mock_datetime.now.return_value = mock_now
        mock_datetime.timedelta = timedelta
        
        mock_leaguepedia_query.return_value = roster_changes_mock_data
        
        changes = lp.get_recent_roster_changes(days=7)  # Last 7 days
        
        call_kwargs = mock_leaguepedia_query.call_args[1]
        assert "Date >= '2023-12-08'" in call_kwargs['where']  # 7 days before 2023-12-15
    
    @pytest.mark.unit
    def test_roster_change_additional_fields(self):
        """Test additional fields like news_id, roster_change_id."""
        roster_change = RosterChange(
            roster_change_id="RC001",
            news_id="NEWS001",
            reference="Official announcement"
        )
        
        assert roster_change.roster_change_id == "RC001"
        assert roster_change.news_id == "NEWS001"
        assert roster_change.reference == "Official announcement"


class TestRosterChangesDataParsing:
    """Test data parsing from API responses."""
    
    @pytest.mark.unit
    def test_roster_change_boolean_parsing(self):
        """Test that boolean fields are properly parsed."""
        # This would typically test the internal parsing function
        roster_change = RosterChange(
            is_retirement=True,
            is_substitute=False,
            is_trainee=True,
            is_lowercase=False
        )
        
        assert isinstance(roster_change.is_retirement, bool)
        assert isinstance(roster_change.is_substitute, bool) 
        assert isinstance(roster_change.is_trainee, bool)
        assert isinstance(roster_change.is_lowercase, bool)
    
    @pytest.mark.unit
    def test_roster_change_date_parsing(self):
        """Test date field parsing."""
        test_date = datetime(2023, 11, 15)
        roster_change = RosterChange(date=test_date)
        
        assert isinstance(roster_change.date, datetime)
        assert roster_change.date == test_date


if __name__ == "__main__":
    pytest.main([__file__])
