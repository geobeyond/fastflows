# this flow example, to run it with command 'python examples/flow_minio.py' uncomment the last line

from prefect import flow, task, get_run_logger
from prefect.blocks.core import Block
import fsspec


@flow(name="file_reader")
def read_file_from_minio(path_to_file: str):
    file_content = read_file_from_bucket(path_to_file)
    print_file_content(file_content)


@task
def print_file_content(file_content: bytes) -> None:
    logger = get_run_logger()
    logger.info(f"File Content: {file_content}")


@task
def read_file_from_bucket(path_to_file: str) -> bytes:
    # you should create before run flow - block that stores those
    # creds with connection secrets to minio server
    # go to UI -> Blocks -> + (create) -> Remote File System

    # example of settings, should be json like:
    # {
    #    "key": "0xoznLEXV3JHiOKx",
    #    "secret": "MmG3vfemCe5mpcxP66a1XvPnsIoXTlWs",
    #    "client_kwargs": {
    #        "endpoint_url": "http://minio:9000"
    #    }
    # }
    # where key & secret - minio users creds
    # endpoint_url - path to minio server
    # name of the block - first type is a 'slug' for type of the block,
    # second part - name how you call it when create
    minio_block = Block.load("remote-file-system/minio-data-storage")

    # read file from minio - don't forget to put it firstly in minio bucket
    of = fsspec.open(
        f"{minio_block.basepath}/{path_to_file}",
        client_kwargs={
            "aws_access_key_id": minio_block.settings["key"],
            "aws_secret_access_key": minio_block.settings["secret"],
            "endpoint_url": minio_block.settings["client_kwargs"]["endpoint_url"],
        },
    )
    # of is just a place-holder
    with of as f:
        # f is now a real file-like object holding resources
        file_content = f.read()
        return file_content


# test.txt - path to file in bucket
# read_file_from_minio('test.txt')
