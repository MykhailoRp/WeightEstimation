from fastapi import APIRouter, UploadFile

from api.dependencies import ApiUser, S3Client
from api.models.basic import FileRespose

router = APIRouter()


@router.post(path="/upload", status_code=200, operation_id="Upload File To Temporary Folder Public")
async def upload(file: UploadFile, s3_client: S3Client, token_data: ApiUser) -> FileRespose:
    file_id = await s3_client.new_upload(file.file, token_data.customer_id)
    return FileRespose(file_id=file_id)
