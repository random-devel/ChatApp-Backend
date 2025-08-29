from beanie import Document
from typing import Any,Optional,Type
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
from beanie.exceptions import DocumentNotFound

async def fetch(Collection: Type[Document], **filters: Any) -> Optional[dict]:
    """that function filter by the values the user submit"""
    if data:= await Collection.find_one(filters):
        return data.model_dump(exclude={'id'})
    return None

async def insertHandler(Collection: Type[Document],returnData: bool, **data: Any) -> Optional[dict]:
    """before using this function you should know the right schema for the Document!!"""
    try:
        info = Collection(**data)
        await info.insert()
        if returnData:
            return info.model_dump(exclude={'id'})
    except DuplicateKeyError:
        raise HTTPException(302)
        
async def delHandler(Collection: Type[Document],**filters):
    if data:= await Collection.find_one(filters):
        await data.delete()
    else:
        return None
    
async def updateHandler(Collection: Type[Document],filter: dict,**updates: Any) -> bool:
    doc = await Collection.find_one(filter)
    if not doc:
        raise DocumentNotFound
    
    for key, value in updates.items():
        if key in doc.model_fields:
            setattr(doc, key, value)

    await doc.save()
    return True
