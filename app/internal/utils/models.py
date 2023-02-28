from beanie import Document, WriteRules, Indexed
from beanie.odm.actions import ActionDirections
from beanie.odm.documents import DocType
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import TypeVar, Optional, List, Union, Dict, Any

from pymongo.client_session import ClientSession
# from fastapi import Response
from starlette.responses import JSONResponse
from fastapi import Response

T = TypeVar('T')


class TreeModel(Document):
    tree_id: int = 1
    level: int = 0
    left: int = 1
    right: int = 2

    # is_leaf: bool = True
    parent: Optional[DocType] = None

    async def get_ancestors(self, include_self=False) -> List[DocType]:
        left = self.left
        right = self.right
        if not include_self:
            left -= 1
            right += 1
        ancestors = await self.find(self.__class__.left <= left, self.__class__.right >= right).to_list()
        return ancestors

    async def get_children(self, include_self=False) -> List[DocType]:
        left = self.left
        right = self.right
        if not include_self:
            left -= 1
            right += 1
        children = await self.find(self.__class__.left >= left, self.__class__.right <= right).to_list()
        return children

    async def is_root(self) -> bool:
        if self.parent:
            return False
        else:
            return True

    async def get_all_right(self):
        await self.fetch_all_links()
        parent_right = self.parent.right
        return await self.find(self.__class__.right > parent_right,self.__class__.left > parent_right,
                               self.__class__.tree_id == self.tree_id).to_list()

    async def correct_tree_indexes(self):
        await self.fetch_all_links()
        self.level = self.parent.level + 1
        self.tree_id = self.parent.tree_id
        for doc in await self.get_all_right():
            doc.right += 2
            doc.left += 2
            await self.__class__.save(doc)
        self.left = self.parent.right
        self.parent.right += 2
        self.right = self.left + 1
        await self.__class__.save(self.parent)

    async def correct_tree(self):
        if self.id is None:

            if await self.is_root():
                last_index = await self.find_all().sort('-tree_id').first_or_none()
                if last_index:
                    self.tree_id = last_index.tree_id + 1
            else:
                await self.correct_tree_indexes()

    async def insert(
            self: DocType,
            *,
            link_rule: WriteRules = WriteRules.DO_NOTHING,
            session: Optional[ClientSession] = None,
            skip_actions: Optional[List[Union[ActionDirections, str]]] = None,
    ):
        print(self)
        if self.id is None:
            await self.correct_tree()
        await super(TreeModel, self).insert(link_rule=link_rule, session=session, skip_actions=skip_actions)


class Content(BaseModel):
    message: str = Field(..., description='Response message')
    result: Optional[T] = None


class CommonResponse(Response):
    media_type = 'application/json'
    content: Content


class CommonHTTPException(HTTPException):
    detail: Content
