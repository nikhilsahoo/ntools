from enum import Enum

class RepositoryFormat(Enum):
    def __str__(self):
        return f"RepositoryFormat[{self.value}]"

    MAVEN = "maven2"
    PYPI = "pypi"
    NPM = "npm"
    NUGET = "nuget"


class RepositoryType(Enum):
    def __str__(self):
        return f"RepositoryType[{self.value}]"

    HOSTED = "hosted"
    PROXY = "proxy"
    GROUP = "group"


class Repository:
    FORMAT = None

    def __init__(
        self,
        artifactory,
        name: str,
        format: RepositoryFormat,
        type: RepositoryType,
    ):
        self.name = name
        self.format = format
        self.type = type
        self.artifactory = artifactory

    def __str__(self):
        return f"Repository[Name:{self.name}, Format:{self.format}, Type:{self.type}]"

    def upload_artefacts(self, dir: str):
        if self.type != RepositoryType.HOSTED:
            exp = Exception("upload supported for HOSTED repository only")
            raise exp
        pass
    
    @classmethod
    def get_format(cls):
        return cls.FORMAT

