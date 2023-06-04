import json
import logging
from logging import config
from google.cloud import storage
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)

with open('phase_2/config.json', 'r') as f:
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
    bucket_name: str = field(init=False)

    def __post_init__(self):
        self.bucket_name = config.get('gcp').get('bucket').get('bucket_name')
        logger.info('From {cls} defining bucket name with attr: {attr}'.format(cls=self.bucket_name.__class__.__name__, attr=self.bucket_name), exc_info=True)
        return self.bucket_name

    def bucket_obj(self):
        self.bucket = Client().client_storage().bucket(self.bucket_name)
        logger.info('From {cls} defining bucket obj with attr: {attr}'.format(cls=self.bucket.__class__.__name__, attr=self.bucket), exc_info=True)
        return self.bucket

@dataclass
class Blob(Bucket):
    blob: str = field(init=False)
    blob_list: list = field(default_factory=list)
    blob_dict: "defaultdict[dict]" = field(default_factory=lambda: defaultdict(dict), init=False)
    bucket_name: str = field(init=False)
    client: str = field(init=False)
    prefix_folder: str = field(init=False)
    
    def __post_init__(self):
        if config.get('gcp').get('bucket').get('mode') == 'socrata':
            self.prefix_folder = config.get('gcp').get('bucket').get('prefix_socrata')
        else:
            self.prefix_folder = config.get('gcp').get('bucket').get('prefix_test')
        logger.info('From {cls} defining prefox folder with attr: {attr}'.format(cls=self.prefix_folder.__class__.__name__, attr=self.prefix_folder), exc_info=True)
        
        self.bucket_name = config.get('gcp').get('bucket').get('bucket_name')
        logger.info('From {cls} defining bucket name with attr: {attr}'.format(cls=self.bucket_name.__class__.__name__, attr=self.bucket_name), exc_info=True)

    def list_blobs(self):
        self.bucket = Bucket().bucket_obj()
        self.blob = self.bucket.list_blobs(prefix=self.prefix_folder) 

        for blob in self.blob:
            blob_name = blob.name
            self.blob_list.append(blob_name)

        logger.info('From {cls} listing blobs with attr: {attr}'.format(cls=self.blob_dict.__class__.__name__, attr=self.blob_dict), exc_info=True)
        return self.blob_list

@dataclass
class Blob_obj():
    blob: str = field(init=False)
    bucket: str = field(init=False)
    bucket_name: str = field(init=False)
    client: str = field(init=False)

    # TO DO I did not find a way to make reusable the Blob class because the blob_name attribute. So, I had to build this Blob_obj class
    blob_name: str

    def __post_init__(self):
        self.bucket_name = config.get('gcp').get('bucket').get('bucket_name')
        logger.info('From {cls} defining bucket name with attr: {attr}'.format(cls=self.bucket_name.__class__.__name__, attr=self.bucket_name), exc_info=True)
    
    def blob_obj(self):
        self.bucket = Bucket().bucket_obj()

        if config.get('gcp').get('bucket').get('mode') == 'socrata':
            self.prefix_folder = config.get('gcp').get('bucket').get('prefix_socrata')
        else:
            self.prefix_folder = config.get('gcp').get('bucket').get('prefix_test')
        
        self.blob_name = self.prefix_folder + '/' + self.blob_name
        self.blob = self.bucket.blob(self.blob_name)

        logger.info('From {cls} defining blob obj with attr: {attr}'.format(cls=self.blob.__class__.__name__, attr=self.blob), exc_info=True)
        return self.blob
    
if __name__ == '__main__':
    Bucket
    Blob
    Client
    
    # TO DO: I did not find a way to make reusable the Blob class because the blob_name attribute. So, I had to build this Blob_obj class
    Blob_obj