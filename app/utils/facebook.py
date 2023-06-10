
from requests import get

class Facebook:
    def __init__(self,access_token) -> None:
        self.base_url='https://graph.facebook.com'
        self.access_token=access_token


    def debugToken(self) :
        url=f'{self.base_url}/debug_token?input_token={self.access_token}&access_token={self.access_token}'
        response=get(url)
        return response.json()['data']['is_valid']
    
    def getUserInformation(self):
        url=f'{self.base_url}/me?fields=id,name,email,picture&access_token={self.access_token}'
        response=get(url)
        return response.json()
    


