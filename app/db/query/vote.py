from typing import List, Literal, Union, Mapping


def _remove_from(vote: Literal["up", "down"], user_id: str) -> Union[dict, Mapping]:
    return {"$pull": {f"{vote}_votes": {"$eq": user_id}}}


def _add_to(vote: Literal["up", "down"], user_id: str) -> Union[dict, Mapping]:

    return {"$addToSet": {f"{vote}_votes": user_id}}


def user_up_vote(user_id: str) -> List[Union[dict, Mapping]]:
    remove_ = _remove_from("down", user_id)
    add_ = _add_to("up", user_id)
    return [remove_, add_]


def user_down_vote(user_id: str) -> List[Union[dict, Mapping]]:
    remove_ = _remove_from("up", user_id)
    add_ = _add_to("down", user_id)
    return [remove_, add_]
