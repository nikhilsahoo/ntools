from ntools.repository import (
    Repository,
    RepositoryFormat,
    RepositoryType,
)

class NugetRepository(Repository):
    FORMAT = RepositoryFormat.NUGET
    def __init__(self, artifactory, name: str, type: RepositoryType):
        Repository.__init__(self, artifactory, name, NugetRepository.FORMAT, type)
