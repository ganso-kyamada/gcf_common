# -*- coding: utf-8 -*-

import base64
import json
import os

from google.cloud import bigquery
from google.cloud import storage
from google.cloud import kms_v1
from google.cloud import pubsub_v1

__version__ = '0.0.1'


def decode_key(project_id: str, location: str, key_ring: str,
               cipher_text: str, key_name: str, client=None) -> bytes:
    """暗号化されたkeyを復号する

    Cloud Key Management Serviceを用いて暗号化されている
    :param str project_id: Google Cloud Platform のプロジェクトID
    :param str location: 場所
    :param str key_ring: KEY RING
    :param str cipher_text: 暗号化した文字列
    :param str key_name: 復号に必要なKey
    :return: 復号されたバイト文字列
    :rtype: bytes
    """

    if client is None:
        client = kms_v1.KeyManagementServiceClient()

    name = client.crypto_key_path(project_id, location, key_ring, key_name)
    response = client.decrypt(name, base64.b64decode(cipher_text))

    return response.plaintext


def upload_to_gcs(raw: str, filename: str,
                  bucket_name: str, client=None) -> None:
    """Google Cloud Storageにファイルをアップロード

    :param str raw: ファイルの中身
    :param str filename: ファイル名
    :param str bucket_name: バケット名
    """

    if client is None:
        client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_string(raw)


def execute_cloud_functions(data: dict, project_id: str,
                            topic_name: str, client=None) -> None:
    if client is None:
        client = pubsub_v1.PublisherClient()
    
    topic_path = client.topic_path(project_id, topic_name)
    json_data = json.dumps(data)

    client.publish(topic_path, data=json_data.encode('utf-8'))


def cloud_function_name() -> str:
    """実行中のcloud function名を取得

    GoogleCloudFunctions限定
    FUNCTION_NAMEという環境変数が標準で入っている

    :return: 実行中のcloud function名
    :rtype: str
    """

    if "FUNCTION_NAME" in os.environ:
        return os.environ["FUNCTION_NAME"]
    else:
        return ""


def is_test() -> bool:
    """テスト実行かを現在のcloud function名で判断する

    :return: テスト実行かどうか
    :rtype: bool
    """

    return ("test" in cloud_function_name())
