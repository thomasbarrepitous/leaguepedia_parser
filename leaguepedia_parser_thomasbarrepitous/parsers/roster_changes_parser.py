import dataclasses
from typing import List, Optional
from datetime import datetime
import enum

from leaguepedia_parser_thomasbarrepitous.site.leaguepedia import leaguepedia
from leaguepedia_parser_thomasbarrepitous.transmuters.field_names import (
    roster_changes_fields,
)


class RosterAction(enum.Enum):
    """Enumeration of possible roster actions."""

    ADD = "Add"
    REMOVE = "Remove"
    ROLE_CHANGE = "Role Change"
    SUBSTITUTE = "Substitute"
    LOAN = "Loan"
    TRANSFER = "Transfer"
    RETIREMENT = "Retirement"


@dataclasses.dataclass
class RosterChange:
    """Represents a roster change from Leaguepedia's RosterChanges table.

    Attributes:
        id: Unique identifier for the change
        team: Team name
        role: Player role
        player: Player name
        action: Type of roster change (Add, Remove, etc.)
        date: Date of the change
        tournament: Tournament context if applicable
        overview_page: Tournament overview page
        reference: Reference/source for the change
        roster_change_id: Roster change identifier
        news_id: Related news item ID
        is_retirement: Whether this is a retirement
        residency: Player's residency status
        residency_former: Player's former residency
        nationality: Player's nationality
        is_lowercase: Whether to display name in lowercase
        is_substitute: Whether this is a substitute change
        is_trainee: Whether player is a trainee
    """

    id: Optional[str] = None
    team: Optional[str] = None
    role: Optional[str] = None
    player: Optional[str] = None
    action: Optional[str] = None
    date: Optional[datetime] = None
    tournament: Optional[str] = None
    overview_page: Optional[str] = None
    reference: Optional[str] = None
    roster_change_id: Optional[str] = None
    news_id: Optional[str] = None
    is_retirement: Optional[bool] = None
    residency: Optional[str] = None
    residency_former: Optional[str] = None
    nationality: Optional[str] = None
    is_lowercase: Optional[bool] = None
    is_substitute: Optional[bool] = None
    is_trainee: Optional[bool] = None

    @property
    def action_enum(self) -> Optional[RosterAction]:
        """Returns the action as an enum value."""
        try:
            return RosterAction(self.action) if self.action else None
        except ValueError:
            return None

    @property
    def is_addition(self) -> bool:
        """Returns True if this is an addition to the team."""
        return self.action == RosterAction.ADD.value

    @property
    def is_removal(self) -> bool:
        """Returns True if this is a removal from the team."""
        return self.action == RosterAction.REMOVE.value


def _parse_roster_change_data(data: dict) -> RosterChange:
    """Parses raw API response data into a RosterChange object."""

    def parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(date_str) if date_str else None
        except (ValueError, AttributeError):
            return None

    def parse_bool(value: Optional[str]) -> Optional[bool]:
        return value == "Yes" if value else None

    return RosterChange(
        id=data.get("ID"),
        team=data.get("Team"),
        role=data.get("Role"),
        player=data.get("Player"),
        action=data.get("Action"),
        date=parse_datetime(data.get("Date")),
        tournament=data.get("Tournament"),
        overview_page=data.get("OverviewPage"),
        reference=data.get("Reference"),
        roster_change_id=data.get("RosterChangeId"),
        news_id=data.get("NewsId"),
        is_retirement=parse_bool(data.get("IsRetirement")),
        residency=data.get("Residency"),
        residency_former=data.get("ResidencyFormer"),
        nationality=data.get("Nationality"),
        is_lowercase=parse_bool(data.get("IsLowercase")),
        is_substitute=parse_bool(data.get("IsSubstitute")),
        is_trainee=parse_bool(data.get("IsTrainee")),
    )


def get_roster_changes(
    team: str = None,
    player: str = None,
    action: str = None,
    tournament: str = None,
    start_date: str = None,
    end_date: str = None,
    **kwargs,
) -> List[RosterChange]:
    """Returns roster change information from Leaguepedia.

    Args:
        team: Team name to filter by
        player: Player name to filter by
        action: Action type to filter by (Add, Remove, etc.)
        tournament: Tournament to filter by
        start_date: Start date for filtering (YYYY-MM-DD format)
        end_date: End date for filtering (YYYY-MM-DD format)
        **kwargs: Additional query parameters

    Returns:
        A list of RosterChange objects

    Raises:
        RuntimeError: If the Leaguepedia query fails
    """
    try:
        where_conditions = []

        if team:
            escaped_team = team.replace("'", "''")
            where_conditions.append(f"RosterChanges.Team='{escaped_team}'")

        if player:
            escaped_player = player.replace("'", "''")
            where_conditions.append(f"RosterChanges.Player='{escaped_player}'")

        if action:
            escaped_action = action.replace("'", "''")
            where_conditions.append(f"RosterChanges.Action='{escaped_action}'")

        if tournament:
            escaped_tournament = tournament.replace("'", "''")
            where_conditions.append(f"RosterChanges.Tournament='{escaped_tournament}'")

        if start_date:
            where_conditions.append(f"RosterChanges.Date >= '{start_date}'")

        if end_date:
            where_conditions.append(f"RosterChanges.Date <= '{end_date}'")

        where_clause = " AND ".join(where_conditions) if where_conditions else None

        changes = leaguepedia.query(
            tables="RosterChanges",
            fields=",".join(roster_changes_fields),
            where=where_clause,
            order_by="RosterChanges.Date DESC",
            **kwargs,
        )

        return [_parse_roster_change_data(change) for change in changes]

    except Exception as e:
        raise RuntimeError(f"Failed to fetch roster changes: {str(e)}")


def get_team_roster_changes(
    team: str, tournament: str = None, **kwargs
) -> List[RosterChange]:
    """Returns all roster changes for a specific team.

    Args:
        team: Team name
        tournament: Tournament to filter by (optional)
        **kwargs: Additional query parameters

    Returns:
        A list of RosterChange objects for the specified team
    """
    return get_roster_changes(team=team, tournament=tournament, **kwargs)


def get_player_roster_changes(player: str, **kwargs) -> List[RosterChange]:
    """Returns all roster changes for a specific player.

    Args:
        player: Player name
        **kwargs: Additional query parameters

    Returns:
        A list of RosterChange objects for the specified player
    """
    return get_roster_changes(player=player, **kwargs)


def get_recent_roster_changes(
    days: int = 30, team: str = None, **kwargs
) -> List[RosterChange]:
    """Returns recent roster changes within the specified number of days.

    Args:
        days: Number of days to look back (default: 30)
        team: Team to filter by (optional)
        **kwargs: Additional query parameters

    Returns:
        A list of recent RosterChange objects
    """
    from datetime import datetime, timedelta

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    return get_roster_changes(
        team=team, start_date=start_date, end_date=end_date, **kwargs
    )


def get_roster_additions(
    team: str = None, tournament: str = None, **kwargs
) -> List[RosterChange]:
    """Returns roster additions (players joining teams).

    Args:
        team: Team to filter by (optional)
        tournament: Tournament to filter by (optional)
        **kwargs: Additional query parameters

    Returns:
        A list of RosterChange objects representing additions
    """
    return get_roster_changes(team=team, tournament=tournament, action="Add", **kwargs)


def get_roster_removals(
    team: str = None, tournament: str = None, **kwargs
) -> List[RosterChange]:
    """Returns roster removals (players leaving teams).

    Args:
        team: Team to filter by (optional)
        tournament: Tournament to filter by (optional)
        **kwargs: Additional query parameters

    Returns:
        A list of RosterChange objects representing removals
    """
    return get_roster_changes(
        team=team, tournament=tournament, action="Remove", **kwargs
    )


def get_retirements(**kwargs) -> List[RosterChange]:
    """Returns player retirements.

    Args:
        **kwargs: Additional query parameters

    Returns:
        A list of RosterChange objects representing retirements
    """
    # Use the specialized retirement filter
    where_clause = "RosterChanges.IsRetirement='Yes'"

    try:
        changes = leaguepedia.query(
            tables="RosterChanges",
            fields=",".join(roster_changes_fields),
            where=where_clause,
            order_by="RosterChanges.Date DESC",
            **kwargs,
        )

        return [_parse_roster_change_data(change) for change in changes]

    except Exception as e:
        raise RuntimeError(f"Failed to fetch retirements: {str(e)}")
