import io
from typing import Union
from urllib.parse import quote

import httpx
from app.core.config import S3_ACCESS_KEY, S3_ENDPOINT_URL, S3_SECRET_KEY
from httpx_aws_auth import AwsCredentials, AwsSigV4Auth


class S3HttpxSigV4Adapter:
    def __init__(
        self,
        bucket: str,
        region: str = "ru-1",
    ):
        self.bucket = bucket
        self.endpoint_url = S3_ENDPOINT_URL.rstrip("/")
        creds = AwsCredentials(access_key=S3_ACCESS_KEY, secret_key=S3_SECRET_KEY)
        self.auth = AwsSigV4Auth(credentials=creds, region=region, service="s3")
        self.client = httpx.AsyncClient(auth=self.auth)

    async def upload_file(
        self,
        file_data: Union[str, bytes, io.BytesIO],
        object_name: str,
        public: bool = True,
    ):
        if isinstance(file_data, str):
            data = open(file_data, "rb").read()
        elif isinstance(file_data, io.BytesIO):
            file_data.seek(0)
            data = file_data.read()
        elif isinstance(file_data, bytes):
            data = file_data
        else:
            raise TypeError("Unsupported file_data type")

        headers = {}
        if public:
            headers["x-amz-acl"] = "public-read"

        url = f"{self.endpoint_url}/{self.bucket}/{object_name}"
        resp = await self.client.put(url, content=data, headers=headers)
        resp.raise_for_status()

    async def delete_file(self, object_name: str):
        url = f"{self.endpoint_url}/{self.bucket}/{object_name}"
        resp = await self.client.delete(url)
        resp.raise_for_status()

    async def copy_file(self, source_object: str, dest_object: str, public: bool = True):
        url = f"{self.endpoint_url}/{self.bucket}/{dest_object}"
        headers = {
            "x-amz-copy-source": f"/{self.bucket}/{quote(source_object)}",
        }
        if public:
            headers["x-amz-acl"] = "public-read"

        resp = await self.client.put(url, headers=headers)
        resp.raise_for_status()

    def get_url(self, object_name: str) -> str:
        bucket_host = self.endpoint_url.split("://", 1)[1].split("/", 1)[0]
        return f"https://{self.bucket}.{bucket_host}/{object_name}"
