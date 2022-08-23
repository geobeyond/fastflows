import datetime
from pydantic import BaseModel
from typing import List, Optional


class BlockDocumentInput(BaseModel):
    name: str
    data: dict
    block_schema_id: str
    block_type_id: str
    is_anonymous: bool = False


class BlockDocumentResponse(BaseModel):
    id: str
    created: datetime.datetime
    updated: datetime.datetime
    name: str
    data: dict
    block_schema_id: str


class BlockTypeResponse(BaseModel):
    id: str
    created: datetime.datetime
    updated: datetime.datetime
    name: str
    slug: str
    logo_url: Optional[str]
    documentation_url: Optional[str]
    description: str
    code_example: Optional[str]
    is_protected: bool = False


class BlockSchemaResponse(BaseModel):
    id: str
    created: datetime.datetime
    updated: datetime.datetime
    checksum: str
    fields: dict
    block_type_id: str
    block_type: BlockTypeResponse
    capabilities: List[str]
