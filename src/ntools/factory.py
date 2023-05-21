from enum import Enum
from ntools.repository import (
    RepositoryType,
)

from ntools.maven import MavenRepository
from ntools.pypi import PyPiRepository
from ntools.npm import NPMRepository
from ntools.nuget import NugetRepository


class RepositoryFactory(Enum):
    def __init__(self, *args, **kwds):
        self.repo_map = {}

    def register(self, clazz):
        self.repo_map[clazz.get_format().value] = clazz

    INSTANCE = "INSTANCE"

    def get_repository(
        self, artifactory, name: str, format: str, type: str
    ):
        if format in RepositoryFactory.INSTANCE.repo_map.keys():
            return self.repo_map[format](artifactory, name, RepositoryType(type))
        
        
RepositoryFactory.INSTANCE.register(MavenRepository)
RepositoryFactory.INSTANCE.register(PyPiRepository)
RepositoryFactory.INSTANCE.register(NPMRepository)
RepositoryFactory.INSTANCE.register(NugetRepository)
