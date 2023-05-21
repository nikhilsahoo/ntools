from ntools.repository import (
    Repository,
    RepositoryFormat,
    RepositoryType,
)
from ntools.util import Util
import requests


class NPMArtifact:
    def __init__(self, path: str = None) -> None:
        self.path = path

    def __str__(self):
        return f"NPMArtifact[path:{self.path}]"


class NPMRepository(Repository):
    FORMAT = RepositoryFormat.NPM

    def __init__(self, artifactory, name: str, type: RepositoryType):
        Repository.__init__(self, artifactory, name, NPMRepository.FORMAT, type)

    def upload_artefacts(self, dir: str):
        super().upload_artefacts(dir)
        artefacts = NPMUtil.get_artefacts(dir)
        for artefact in artefacts:
            self._upload(self.name, artefact)

    def _upload(self, repository: str, artefact: NPMArtifact):
        file = {"npm.asset": (artefact.path, open(artefact.path, "rb"))}
        params = {"repository": repository}
        response = requests.post(
            self.artifactory.component_endpoint,
            auth=self.artifactory.creds.get_http_auth(),
            files=file,
            params=params,
        )
        if response.status_code not in [200, 201, 204]:
            print(response.json())
            exp = Exception(
                "{obj} upload failed, status {status}".format(
                    obj=str(artefact), status=response.status_code
                )
            )
            raise exp
        else:
            print(f"{artefact} uploaded")


class NPMUtil:
    @classmethod
    def get_artefacts(cls, dir: str):
        artefacts = []
        filter = ["tgz"]
        files = Util.get_files(dir, filter)
        for path in files.keys():
            for file in files[path]:
                artefacts.append(NPMArtifact(path=file))
        return artefacts
