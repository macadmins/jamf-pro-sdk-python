from __future__ import annotations

import logging
import math
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Callable, Iterator

import requests
from requests.adapters import HTTPAdapter

try:
    import boto3
except ImportError:
    BOTO3_IS_INSTALLED = False
    boto3 = None
else:
    BOTO3_IS_INSTALLED = True

from ..models.classic.packages import ClassicPackage
from ..models.pro.jcds2 import NewFile

if TYPE_CHECKING:
    from .classic_api import ClassicApi
    from .pro_api import ProApi

CHUNK_SIZE = 1024 * 1024 * 20  # 20 MB

logger = logging.getLogger("jamf_pro_sdk")


class FileUpload:
    def __init__(self, path: Path):
        self.path = path
        self.size = path.stat().st_size
        self.total_chunks = math.ceil(self.size / CHUNK_SIZE)

    def get_chunk(self, chunk_number: int) -> bytes:
        if chunk_number > self.total_chunks:
            raise ValueError(f"Chunk number must be less than or equal to {self.total_chunks}")

        with open(self.path, "rb") as fobj:
            fobj.seek(chunk_number * CHUNK_SIZE)
            return fobj.read(CHUNK_SIZE)


class JCDS2:
    """Provides an interface to manage files in JCDS2."""

    def __init__(
        self,
        classic_api_client: ClassicApi,
        pro_api_client: ProApi,
        concurrent_requests_method: Callable[..., Iterator],
    ):
        if not BOTO3_IS_INSTALLED:
            raise ImportError("The 'aws' extra dependency is required.")

        self.classic_api_client = classic_api_client
        self.pro_api_client = pro_api_client
        self.concurrent_api_requests = concurrent_requests_method

    @staticmethod
    def _upload_file(s3_client, jcds_file: NewFile, file_upload: FileUpload):
        logger.info("JCDS2-Upload %s ", file_upload.path)
        with open(file_upload.path, "rb") as fobj:
            resp = s3_client.put_object(
                Body=fobj,
                Bucket=jcds_file.bucketName,
                Key=f"{jcds_file.path}{file_upload.path.name}",
            )
            logger.debug(resp)

    def _upload_multipart(self, s3_client, jcds_file: NewFile, file_upload: FileUpload):
        logger.info("JCDS2-UploadMultipart %s", file_upload.path)
        multipart_upload = s3_client.create_multipart_upload(
            Bucket=jcds_file.bucketName, Key=f"{jcds_file.path}{file_upload.path.name}"
        )
        logger.debug(multipart_upload)

        multipart_upload_parts = list()

        for r in self.concurrent_api_requests(
            handler=self._upload_part,
            arguments=[
                {
                    "s3_client": s3_client,
                    "part_number": i,
                    "file_upload": file_upload,
                    "multipart_upload": multipart_upload,
                }
                for i in range(1, file_upload.total_chunks + 1)
            ],
        ):
            multipart_upload_parts.append(r)

        try:
            multipart_upload_complete = s3_client.complete_multipart_upload(
                Bucket=multipart_upload["Bucket"],
                Key=multipart_upload["Key"],
                MultipartUpload={"Parts": multipart_upload_parts},
                UploadId=multipart_upload["UploadId"],
            )
            logger.debug(multipart_upload_complete)
        except:
            logger.error("JCDS2-UploadMultipart-Aborted %s", file_upload.path)
            multipart_aborted = s3_client.abort_multipart_upload(
                Bucket=multipart_upload["Bucket"],
                Key=multipart_upload["Key"],
                UploadId=multipart_upload["UploadId"],
            )
            logger.debug(multipart_aborted)
            raise

    @staticmethod
    def _upload_part(s3_client, multipart_upload: dict, part_number: int, file_upload: FileUpload):
        logger.info("JCDS2-UploadMultipart-Part %s %s", part_number, file_upload.path.name)
        # TODO: Retry functionality if a part upload fails
        part_resp = s3_client.upload_part(
            Body=file_upload.get_chunk(part_number - 1),
            Bucket=multipart_upload["Bucket"],
            Key=multipart_upload["Key"],
            PartNumber=part_number,
            UploadId=multipart_upload["UploadId"],
        )
        logger.debug(part_resp)
        return {"PartNumber": part_number, "ETag": part_resp["ETag"]}

    def upload_file(self, file_path: Path):
        file_upload = FileUpload(file_path)
        new_jcds_file = self.pro_api_client.create_jcds_file_v1()

        boto3_session = boto3.Session(
            aws_access_key_id=new_jcds_file.accessKeyID,
            aws_secret_access_key=new_jcds_file.secretAccessKey,
            aws_session_token=new_jcds_file.sessionToken,
            region_name=new_jcds_file.region,
        )

        s3_client = boto3_session.client(service_name="s3")

        try:
            # if file_upload.size < 5368709120:  # 5 GiB
            if file_upload.size < 1073741824:  # 1 GiB
                self._upload_file(
                    s3_client=s3_client, jcds_file=new_jcds_file, file_upload=file_upload
                )
            else:
                self._upload_multipart(
                    s3_client=s3_client, jcds_file=new_jcds_file, file_upload=file_upload
                )
        except Exception as err:
            logger.exception(err)
            raise
        else:
            new_package = ClassicPackage(name=file_path.name, filename=file_path.name)
            new_pkg_resp = self.classic_api_client.create_package(data=new_package)
            logger.debug(new_pkg_resp)

    @staticmethod
    def _download_range(session: requests.Session, url: str, index: int, temp_dir: str):
        range_start = index * CHUNK_SIZE
        range_end = ((index + 1) * CHUNK_SIZE) - 1
        with session.get(
            url, headers={"Range": f"bytes={range_start}-{range_end}"}, timeout=60
        ) as range_response:
            logger.debug(range_response.headers)
            with open(temp_dir + f"/chunk_{str(index).zfill(9)}", "wb") as fobj:
                fobj.write(range_response.content)

    def download_file(self, file_name: str, download_path: Path):
        if download_path.exists():
            raise FileExistsError("A file or directory at the download path already exists")

        download_file = self.pro_api_client.get_jcds_file_v1(file_name=file_name)

        # TODO: Retry feature that's not relying on urllib3's implementation
        download_session = requests.Session()
        download_session.mount(
            prefix="https://",
            adapter=requests.adapters.HTTPAdapter(
                max_retries=3, pool_connections=5, pool_maxsize=5
            ),
        )

        with download_session.head(download_file.uri) as download_file_head:
            total_chunks = math.ceil(int(download_file_head.headers["Content-Length"]) / CHUNK_SIZE)

        temp_dir = TemporaryDirectory(prefix="jcds2-download-")
        logger.debug("JCDS2-Download-TempDir %s", temp_dir.name)

        r = self.concurrent_api_requests(
            handler=self._download_range,
            arguments=[
                {
                    "session": download_session,
                    "url": download_file.uri,
                    "index": i,
                    "temp_dir": temp_dir.name,
                }
                for i in range(0, total_chunks)
            ],
            max_concurrency=5,
        )
        list(r)

        with open(download_path, "ab") as fobj:
            for chunk in sorted(Path(temp_dir.name).glob("chunk_*")):
                with open(chunk, "rb") as chunk_fobj:
                    fobj.write(chunk_fobj.read())
