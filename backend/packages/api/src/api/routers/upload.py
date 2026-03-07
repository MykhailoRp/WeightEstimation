from fastapi import APIRouter, UploadFile

from api.dependencies import S3Clinet
from api.models.basic import FileRespose

router = APIRouter()


@router.post(path="/upload")
async def upload(file: UploadFile, s3_client: S3Clinet) -> FileRespose:
    file_id = await s3_client.upload_file(file.file)
    return FileRespose(file_id=file_id)
