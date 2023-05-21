# Nexus3 repository upload library
`ntools` is a small library of objects that can help in connecting and uploading artifacts to nexus 3 repository

# Usage
## Upload Maven Artefacts from a directory following m2 format
```python
from ntools.artifactory import Artifactory

artifactory = Artifactory("<nexus url>", "<username>", "<password>")
artifactory.get_repositories()
#returns a list of repository objects
maven_repo = artifactory.get_repository("<maven repository name>")
#fetches repository object of given name
maven_repo.upload_artefacts("<dir path>")
#uploads jar and poms files from dir path to nexus
```

## Upload PyPi Artefacts from a directory containing tar.gz and whl files
```python
from ntools.artifactory import Artifactory

artifactory = Artifactory("<nexus url>", "<username>", "<password>")
pypi_repo = artifactory.get_repository("<pypi repository name>")
#fetches repository object of given name
pypi_repo.upload_artefacts("<dir path>")
#uploads tar.gz and whl files from dir path to nexus
```
