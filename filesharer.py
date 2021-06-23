from filestack import Client

class FileShare:

    def __init__(self, filepath, api_key = 'A2UWvpWIRii8epuTYcPwLz'):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath = self.filepath)
        return new_filelink.url