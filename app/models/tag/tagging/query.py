from typing import List, Mapping, Union, Literal
from dataclasses import dataclass

__all__ = ("TaggingQuery",)


@dataclass
class TaggingQuery:

    @classmethod
    def _remove_query(
        cls, vote: Literal["up", "down"], user_id: str
    ) -> Union[dict, Mapping]:
        return {"$pull": {f"{vote}_votes": {"$eq": user_id}}}

    @classmethod
    def _add_query(
        cls, vote: Literal["up", "down"], user_id: str
    ) -> Union[dict, Mapping]:

        return {"$addToSet": {f"{vote}_votes": user_id}}

    @classmethod
    def up_vote_user(cls, user_id) -> List[Union[dict, Mapping]]:
        return [cls._remove_query("down", user_id), cls._add_query("up", user_id)]

    @classmethod
    def down_vote_user(cls, user_id) -> List[Union[dict, Mapping]]:
        return [cls._remove_query("up", user_id), cls._add_query("down", user_id)]
