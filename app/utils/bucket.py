from os import getenv
from boto3 import client


class Bucket:
    def __init__(self,name,folder) -> None:
        self.name=name
        self.folder=folder
        self.region=getenv('AWS_REGION')
        self.access_id=getenv('AWS_ACCESS_KEY_ID')
        self.access_secret=getenv('AWS_ACCESS_KEY_SECRET')

        self.client=client(
            's3',
            region_name=self.region,
            aws_access_key_id=self.access_id,
            aws_secret_access_key=self.access_secret
        )
        self.__url=f'https://{self.name}.s3.{self.region}.amazonaws.com'

        
    def uploadObject(self,filename,stream):
        try:
            self.client.upload_fileobj(
                stream,self.name,f'{self.folder}/{filename}',
                ExtraArgs={'ACL':'public-read'}
            )
            return f'{self.__url}/{self.folder}/{filename}'
        except Exception as e:
            raise Exception(f'Bucket error -> {str(e)}')

    def deleteObject(self,filename):
        try:
            self.client.delete_objects(
                Bucket=self.name,
                Delete={
                    'Objects':[
                        {
                            'Key':f'{self.folder}/{filename}'
                        }
                    ]
                }
            )
        except Exception as e:
            raise Exception(f'Bucket error -> {str(e)}')       