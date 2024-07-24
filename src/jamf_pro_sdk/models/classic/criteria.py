from enum import Enum

from pydantic import BaseModel, ConfigDict


class ClassicCriterionAndOr(str, Enum):
    and_: str = "and"
    or_: str = "or"


class ClassicCriterionSearchType(str, Enum):
    """Supported search types for Classic API criteria.

    .. attention::

        The supported search types are dependent on the field that is entered in the criterion's
        ``name`` field.

    """

    is_: str = "is"
    is_not: str = "is not"
    like: str = "like"
    not_like: str = "not like"
    has: str = "has"
    does_not_have: str = "does not have"
    matches_regex: str = "matches regex"
    does_not_match_regex: str = "does not match regex"
    before_yyyy_mm_dd: str = "before (yyyy-mm-dd)"
    after_yyyy_mm_dd: str = "after (yyyy-mm-dd)"
    more_than_x_days_ago: str = "more than x days ago"
    less_than_x_days_ago: str = "less than x days ago"
    current: str = "current"
    not_current: str = "not current"
    member_of: str = "member of"
    not_member_of: str = "not member of"
    more_than: str = "more than"
    less_than: str = "less than"
    greater_than: str = "greater than"
    greater_than_or_equal: str = "greater than or equal"
    less_than_or_equal: str = "less than or equal"


class ClassicCriterion(BaseModel):
    """Classic API criterion. Used by Smart Groups and Advanced Searches."""

    model_config = ConfigDict(extra="allow", use_enum_values=True)

    name: str
    priority: int
    and_or: ClassicCriterionAndOr
    search_type: ClassicCriterionSearchType
    value: str
    opening_paren: bool
    closing_paren: bool
