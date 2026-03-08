import asyncio
import os
import uuid
from collections.abc import AsyncGenerator, Iterable
from contextlib import asynccontextmanager, suppress
from itertools import batched
from pathlib import Path
from tempfile import NamedTemporaryFile, _TemporaryFileWrapper
from typing import TYPE_CHECKING, BinaryIO

import aioboto3
import types_aiobotocore_s3 as boto_types
from aiobotocore.session import ClientCreatorContext as _ClientCreatorContext

from common.s3.config import StorageConfig
from common.types import FileId, S3Key

if TYPE_CHECKING:
    ClientCreatorContext = _ClientCreatorContext[boto_types.S3Client]
else:
    ClientCreatorContext = _ClientCreatorContext


class S3Client:
    def __init__(self, config: StorageConfig, session: aioboto3.Session | None = None):

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

    async def new_upload(self, b: BinaryIO, /) -> FileId:
        file_id = FileId(uuid.uuid4())
        async with self.client() as client:
            await client.upload_fileobj(b, self.config.bucket, self.config.get_uploads(file_id))

        return file_id

    async def delete_object(self, key: S3Key, /) -> None:
        async with self.client() as client:
            await client.delete_object(Bucket=self.config.bucket, Key=key)

    async def delete_upload(self, file_id: FileId, /) -> None:
        async with self.client() as client:
            await client.delete_object(Bucket=self.config.bucket, Key=self.config.get_uploads(file_id))

    async def move_from_uploads(self, file_id: FileId, to: S3Key) -> None:
        async with self.client() as client:
            await client.copy_object(Bucket=self.config.bucket, CopySource={"Bucket": self.config.bucket, "Key": self.config.get_uploads(file_id)}, Key=to)

    @asynccontextmanager
    async def file(self, key: S3Key, /) -> AsyncGenerator[_TemporaryFileWrapper, None]:
        with NamedTemporaryFile(prefix="s3_") as temp_t:
            async with self.client() as client:
                await client.download_fileobj(Bucket=self.config.bucket, Key=key, Fileobj=temp_t)
                yield temp_t

    async def upload_file_to(self, f: str, t: S3Key) -> None:
        async with self.client() as client:
            await client.upload_file(f, self.config.bucket, t)

    async def batch_upload_file_to(self, fs: Iterable[str], ts: Iterable[S3Key], *, batch: int = 10) -> None:
        async with self.client() as client:
            for f_t_batch in batched(zip(fs, ts, strict=True), batch):
                await asyncio.gather(
                    *[client.upload_file(f, self.config.bucket, t) for f, t in f_t_batch],
                )

    async def upload_directory(self, dir_path: str, to: S3Key, *, batch: int = 10) -> None:
        directory = Path(dir_path)
        async with self.client() as client:
            for file_batch in batched(filter(Path.is_file, directory.rglob("*")), batch):
                await asyncio.gather(
                    *[client.upload_file(str(file), self.config.bucket, os.path.join(to, file.relative_to(directory))) for file in file_batch],
                )
