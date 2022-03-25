class BaseAPI:
    def __init__(self, client=None):
        self._client = client

    def _get(self, url: str, relay={}):
        return self._client.get(url, relay)

    def _post(self, url: str, relay={}):
        return self._client.post(url, relay)

    @property
    def baseurl(self) -> str:
        return self._client.baseurl

    @property
    def group_id(self):
        return self._client.group_id

    @property
    def node(self):
        return self._client.node

    @property
    def group(self):
        return self._client.group

    @property
    def config(self):
        return self._client.config

    @property
    def paid(self):
        return self._client.paid

    @property
    def db(self):
        return self._client.db
