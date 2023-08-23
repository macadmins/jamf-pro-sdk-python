from __future__ import annotations

import logging
import math
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterator

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

CHUNK_SIZE = 1024 * 1024 * 10  # 10 MB

logger = logging.getLogger("jamf_pro_sdk")


class LocalFile:
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
    def _upload_file(s3_client, jcds_file: NewFile, local_file: LocalFile):
        logger.info("JCDS2-Upload %s ", local_file.path)
        with open(local_file.path, "rb") as fobj:
            resp = s3_client.put_object(
                Body=fobj,
                Bucket=jcds_file.bucketName,
                Key=f"{jcds_file.path}{local_file.path.name}",
            )
            logger.debug(resp)

    def _upload_multipart(self, s3_client, jcds_file: NewFile, local_file: LocalFile):
        logger.info("JCDS2-UploadMultipart %s", local_file.path)
        multipart_upload = s3_client.create_multipart_upload(
            Bucket=jcds_file.bucketName, Key=f"{jcds_file.path}{local_file.path.name}"
        )
        logger.debug(multipart_upload)

        multipart_upload_parts = list()

        for r in self.concurrent_api_requests(
            handler=self._upload_part,
            arguments=[
                {
                    "s3_client": s3_client,
                    "part_number": i,
                    "local_file": local_file,
                    "multipart_upload": multipart_upload,
                }
                for i in range(1, local_file.total_chunks + 1)
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
            logger.error("JCDS2-UploadMultipart-Aborted %s", local_file.path)
            multipart_aborted = s3_client.abort_multipart_upload(
                Bucket=multipart_upload["Bucket"],
                Key=multipart_upload["Key"],
                UploadId=multipart_upload["UploadId"],
            )
            logger.debug(multipart_aborted)

    @staticmethod
    def _upload_part(s3_client, multipart_upload: dict, part_number: int, local_file: LocalFile):
        logger.info("JCDS2-UploadMultipart-Part %s %s", part_number, local_file.path.name)
        part_resp = s3_client.upload_part(
            Body=local_file.get_chunk(part_number - 1),
            Bucket=multipart_upload["Bucket"],
            Key=multipart_upload["Key"],
            PartNumber=part_number,
            UploadId=multipart_upload["UploadId"],
        )
        logger.debug(part_resp)
        return {"PartNumber": part_number, "ETag": part_resp["ETag"]}

    def upload_file(self, file_path: Path):
        local_file = LocalFile(file_path)
        new_jcds_file = self.pro_api_client.create_jcds_file_v1()

        boto3_session = boto3.Session(
            aws_access_key_id=new_jcds_file.accessKeyID,
            aws_secret_access_key=new_jcds_file.secretAccessKey,
            aws_session_token=new_jcds_file.sessionToken,
            region_name=new_jcds_file.region,
        )

        s3_client = boto3_session.client(service_name="s3")

        try:
            if local_file.size < 5368709120:  # 5 GiB
                self._upload_file(
                    s3_client=s3_client, jcds_file=new_jcds_file, local_file=local_file
                )
            else:
                self._upload_multipart(
                    s3_client=s3_client, jcds_file=new_jcds_file, local_file=local_file
                )
        except Exception as err:
            logger.exception(err)
            raise
        else:
            new_package = ClassicPackage(name=file_path.name, filename=file_path.name)
            new_pkg_resp = self.classic_api_client.create_package(data=new_package)
            logger.info("")
            logger.debug(new_pkg_resp)
