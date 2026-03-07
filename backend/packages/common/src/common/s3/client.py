import uuid
from contextlib import suppress
from typing import BinaryIO

import aioboto3
from aiobotocore.session import ClientCreatorContext

from common.s3.config import StorageCongfig
from common.types import FileId


class S3Client:
    def __init__(self, config: StorageCongfig, session: aioboto3.Session | None = None):

        self.config = config

        self.session = session or aioboto3.Session(
            aws_access_key_id=config.access_key_id,
            aws_secret_access_key=config.secret_access_key,
        )

    def client(self) -> ClientCreatorContext:
        return self.session.client(
            "s3",
            endpoint_url=self.config.endpoint_url,
            region_name=self.config.region_name,
        )

    async def safe_create_bucket(self) -> None:
        async with self.client() as client:
            with suppress(client.exceptions.BucketAlreadyExists):
                await client.create_bucket(Bucket=self.config.bucket)

    async def upload_file(self, b: BinaryIO, /) -> FileId:
        file_id = FileId(uuid.uuid4())
        async with self.client() as client:
            await client.upload_fileobj(b, self.config.bucket, self.config.get_uploads(file_id))

        return file_id

    async def delete_object(self, key: str, /) -> None:
        async with self.client() as client:
            await client.delete_object(Bucket=self.config.bucket, Key=key)

    async def delete_upload(self, file_id: FileId, /) -> None:
        async with self.client() as client:
            await client.delete_object(Bucket=self.config.bucket, Key=self.config.get_uploads(file_id))

    async def move_from_uploads(self, file_id: FileId, to: str) -> None:
        async with self.client() as client:
            await client.copy_object(Bucket=self.config.bucket, CopySource={"Bucket": self.config.bucket, "Key": self.config.get_uploads(file_id)}, Key=to)
