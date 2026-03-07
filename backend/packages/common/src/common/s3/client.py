import uuid
from contextlib import suppress
from typing import BinaryIO

import aioboto3

from common.s3.config import StorageCongfig
from common.types import FileId


class S3Client:
    def __init__(self, config: StorageCongfig, session: aioboto3.Session | None = None):

        self.config = config

        self.session = session or aioboto3.Session(
            aws_access_key_id=config.access_key_id,
            aws_secret_access_key=config.secret_access_key,
        )

        self.client = self.session.client(
            "s3",
            endpoint_url=config.endpoint_url,
            region_name=config.region_name,
        )

    async def safe_create_bucket(self) -> None:
        async with self.client as client:
            with suppress(client.exceptions.BucketAlreadyExists):
                await client.create_bucket(Bucket=self.config.bucket)

    async def upload_file(self, b: BinaryIO, /) -> FileId:
        file_id = FileId(uuid.uuid4())
        async with self.client as client:
            await client.upload_fileobj(b, self.config.bucket, self.config.get_uploads_path(file_id))

        return file_id
