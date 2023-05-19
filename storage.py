import json
import logging
from logging import config
from google.cloud import storage
from dataclasses import dataclass, field
from collections import defaultdict

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

@dataclass
class Client:
    credential_path: str = field(init=False)
    storage_client: str = field(init=False)

    def __post_init__(self):
        self.credential_path = config.get('gcp').get('credentials').get('folder')

        logger.info('From {cls} defining credential path with attr: {attr}'.format(cls=self.credential_path.__class__.__name__, attr=self.credential_path), exc_info=True)

        return self.credential_path

    def client_storage(self):
        self.storage_client = storage.Client.from_service_account_json(json_credentials_path=self.credential_path)

        logger.info('From {cls} defining storage client with attr: {attr}'.format(cls=self.storage_client.__class__.__name__, attr=self.storage_client), exc_info=True)

        return self.storage_client

@dataclass
class Bucket(Client):
    bucket: str = field(init=False)
    bucket_name: str
    blob: str = field(init=False)
    blob_dict: "defaultdict[dict]" = field(default_factory=lambda: defaultdict(dict), init=False)
    client: str = field(init=False)
    prefix_folder: str = field(init=False)

    def __post_init__(self):
        self.prefix_folder = config.get('gcp').get('bucket').get('prefix_socrata')
        # self.bucket_name = config.get('gcp').get('bucket').get('bucket_name').replace("/", "")
        return self.prefix_folder

    def list_blobs(self):
        self.client = Client().client_storage()
        self.bucket = self.client.bucket(bucket_name=self.bucket_name.replace("/", ""))
        self.blob = self.client.list_blobs(bucket_or_name=self.bucket_name.replace("/", ""), prefix=self.prefix_folder)

        blob_list = []
        for blob in self.blob:
            blob_name = blob.name
            blob_list.append(blob_name)
        
        self.blob_dict = dict(enumerate(blob_list))

        logger.info('From {cls} listing blobs with attr: {attr}'.format(cls=self.blob_dict.__class__.__name__, attr=self.blob_dict), exc_info=True)

        return self.blob_dict

@dataclass
class Blob(Client):
    bucket: str = field(init=False)
    bucket_name: str
    blob: str = field(init=False)
    blob_name: str
    
    def bucket_blob(self):
        self.bucket = Client().client_storage().bucket(self.bucket_name)
        
        logger.info('From {cls} defining bucket obj with attr: {attr}'.format(cls=self.bucket.__class__.__name__, attr=self.bucket), exc_info=True)
        
        self.blob = self.bucket.blob(self.blob_name)
        
        logger.info('From {cls} defining blob obj with attr: {attr}'.format(cls=self.blob.__class__.__name__, attr=self.blob), exc_info=True)
        
        return self.bucket, self.blob

if __name__ == '__main__':
    Bucket
    Blob
    Client
    
    # name_bucket = config.get('gcp').get('bucket').get('bucket_name')
    # name_blob = 'test/my_file_4.csv'
    # blob_obj = Blob(bucket_name=name_bucket, blob_name=name_blob).bucket_blob()[1]

    # with blob_obj.open("w") as write_file:
    #     json.dump(config.get('api').get('domain').get('url'), write_file, indent=4)
    #     print(Client().storage())

    # blobs = Bucket(bucket_name=name_bucket).list_blobs()
    # print(blobs)