from fastflows.providers import provider
from fastflows.config.app import configuration as cfg
from fastflows.schemas.prefect.block import BlockDocumentInput, BlockTypeResponse
from slugify import slugify
from uuid import uuid1
from fastflows.errors import FastFlowException


def get_storage_block_type() -> BlockTypeResponse:
    prefect_storage_type = cfg.PREFECT_STORAGE_BLOCK_TYPE
    block_type = provider.get_block_by_slug(prefect_storage_type)
    return block_type


def get_infrastructure_block_type() -> BlockTypeResponse:
    prefect_infrustructure_type = cfg.PREFECT_INFRASTRUCTURE_BLOCK_TYPE
    block_type = provider.get_block_by_slug(prefect_infrustructure_type)
    return block_type


def get_block_name(postfix: str) -> str:
    postfix = slugify(postfix)
    return f"{cfg.PREFECT_STORAGE_NAME}-{postfix}".lower()


def get_or_create_block_document(postfix: str) -> str:
    """postfix: can be a flow-name or any other string used as a additional to storage basepath"""

    block_name = get_block_name(postfix)

    try:
        document_block_id = provider.read_block_document_by_name(block_name).id
    except FastFlowException as e:
        if "404" in str(e):
            document_block_id = create_storage_block_document(postfix)
    return str(document_block_id)


def create_storage_block_document(postfix: str) -> str:

    # get block type
    block_type_id = get_storage_block_type().id

    block_schema_id = provider.get_block_schema_by_type_id(block_type_id=block_type_id)[
        0
    ].id

    data = {"basepath": f"{cfg.PREFECT_STORAGE_BASEPATH}/{postfix}"}

    block_name = get_block_name(postfix)
    if cfg.PREFECT_STORAGE_BLOCK_TYPE == "remote-file-system":
        # setting should be provided for connection purposes
        data["settings"] = cfg.PREFECT_STORAGE_SETTINGS

    block_document = BlockDocumentInput(
        block_type_id=block_type_id,
        block_schema_id=block_schema_id,
        name=block_name,
        data=data,
        is_anonymous=False,
    )
    # create block-document for postfix
    document_block_id = provider.create_block_document(block_document).id

    return str(document_block_id)


def create_infrustructure_block_document(flow_input):

    # get block type for flow deployment
    block_type_id = get_infrastructure_block_type().id
    block_schema_id = provider.get_block_schema_by_type_id(block_type_id=block_type_id)[
        0
    ].id
    block_document = BlockDocumentInput(
        block_type_id=block_type_id,
        block_schema_id=block_schema_id,
        name=slugify(flow_input.flow_name) + str(uuid1()),
        data={"env": {"key": "value"}},
        is_anonymous=False,
    )
    # create block for flow
    document_block_id = provider.create_block_document(block_document).id
    return str(document_block_id)
