from __future__ import annotations
from abc import ABCMeta, abstractmethod
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List, Optional

__all__ = ("i18n", "dbInit")

ISO_639 = ["en", "ko"]


class i18n(Document):
    value: str
    lang: str

    def __eq__(self, compare: i18n):
        return self.value == compare.value and self.lang == compare.lang

    @classmethod
    def RIGHT_JOIN(cls, left: List[i18n], right: List[i18n]) -> List[i18n]:

        result: List[i18n] = []
        for new_val in right:
            flag = True
            for val in left:
                # if val.value == new_val.value and val.lang == new_val.lang:
                if val == new_val:
                    # 일부 언어 번역이 중복으로 있을 경우 기존 Document 사용
                    result.append(val)
                    flag = False
                    break
            if flag:
                # 새로운 번역 추가 될 경우 or 번역이 수정된 경우
                result.append(new_val)
        return result

    @classmethod
    def LEFT_ONLY(self, left: List[i18n], right: List[i18n]) -> List[i18n]:
        result: List[i18n] = []
        for val_left in left:
            flag = False
            for val_right in right:
                # if val.value == new_val.value and val.lang == new_val.lang:
                if val_left == val_right:
                    flag = True
                    break
            if flag:
                continue
            result.append(val_left)

        return result

    def to_front(self):
        return self.model_dump(include=["value", "lang"])

    def as_lang_key(self):
        """

        return {"en" : "Ford"}
        """
        return {self.lang: self.value}

    class Settings:
        is_root = True


dbInit = [i18n]
