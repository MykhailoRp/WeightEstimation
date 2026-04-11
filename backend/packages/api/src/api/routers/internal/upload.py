from fastapi import APIRouter, UploadFile

from api.dependencies import S3Client, TokenData
from api.models.basic import FileRespose

router = APIRouter()


@router.post(path="/upload", status_code=200, operation_id="Upload File To Temporary Folder")
async def upload(file: UploadFile, s3_client: S3Client, token_data: TokenData) -> FileRespose:
    file_id = await s3_client.new_upload(file.file, token_data.id)
    return FileRespose(file_id=file_id)
