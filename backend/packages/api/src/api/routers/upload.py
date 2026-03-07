from fastapi import APIRouter, UploadFile

from api.dependencies import S3Client
from api.models.basic import FileRespose

router = APIRouter()


@router.post(path="/upload", status_code=200, operation_id="Upload file to temporary folder")
async def upload(file: UploadFile, s3_client: S3Client) -> FileRespose:
    file_id = await s3_client.upload_file(file.file)
    return FileRespose(file_id=file_id)
