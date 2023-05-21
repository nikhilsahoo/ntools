import requests
from requests.auth import HTTPBasicAuth
from ntools.factory import RepositoryFactory


class Artifactory:
    def __init__(self, url, username, password):
        self.url = url
        self.creds = ArtifactoryCreds(username, password)
        self.rest_endpoint = f"{url}/service/rest"
        self.repository_endpoint = f"{self.rest_endpoint}/v1/repositories"
        self.component_endpoint = f"{self.rest_endpoint}/v1/components"
        self.repositories = []

    def get_repositories(self, reload: bool = False) -> list:
        if not self.repositories:
            response = requests.get(
                self.repository_endpoint, auth=self.creds.get_http_auth()
            )
            if response.status_code == 200:
                content = response.json()
                for repo in content:
                    self.repositories.append(
                        RepositoryFactory.INSTANCE.get_repository(
                            self, repo["name"], repo["format"], repo["type"]
                        )
                    )
            return self.repositories 
        elif reload:
            self.repositories = []
            return self.get_repositories()
        else:
            return self.repositories

    def get_repository(self, name: str):
        repos = self.get_repositories()
        for repo in repos:
            if repo.name == name:
                return repo


class ArtifactoryCreds:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_http_auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.username, self.password)


