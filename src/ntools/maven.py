from ntools.repository import (
    Repository,
    RepositoryFormat,
    RepositoryType,
)

import os
import requests


class MavenArtifact:
    
    def __init__(self, dir_root: str, pom_path: str = None, jar_path: str = None):
        if not os.path.isdir(dir_root):
            exp = Exception("root_dir should be a directory")
            raise exp
        self.pom_path = pom_path
        self.jar_path = jar_path
        if self.pom_path is not None and (not os.path.isfile(self.pom_path)):
            exp1 = Exception("pom_path should be a file")
            raise exp1
        if self.jar_path is not None and (not os.path.isfile(self.jar_path)):
            exp2 = Exception("jar_path should be a file")
            raise exp2
        if dir_root.endswith(os.path.sep):
            self.dir_root = dir_root
        else:
            self.dir_root = f"{dir_root}{os.path.sep}"
        (
            self.group_id,
            self.artifact_id,
            self.version,
        ) = MavenArtifact._get_artifact_details(
            self.pom_path, self.jar_path, self.dir_root
        )

    @classmethod
    def _get_artifact_details(
        cls, pom_path: str, jar_path: str, dir_root: str
    ):
        """
        returns groupId, artifactId, version
        """
        if not pom_path and not jar_path:
            exp = Exception("Maven artifact must contain a pom or a jar")
            raise exp
        else:
            if pom_path:
                try:
                    pom_path = pom_path.replace(dir_root, "")
                    pom_obj = pom_path.split(os.path.sep)
                    length = len(pom_obj)
                    pom_obj.pop(length - 1)
                    version = pom_obj.pop(length - 2)
                    artifact = pom_obj.pop(length - 3)
                    group = MavenArtifact._get_group_id(pom_obj)
                    return (group, artifact, version)
                except Exception:
                    print("unable to read pom file")
            elif jar_path:
                pom_path = jar_path.replace(dir_root + os.path.sep, "")
                pom_obj = pom_path.split(os.path.sep)
                length = len(pom_obj)
                pom_obj.pop(length - 1)
                version = pom_obj.pop(length - 2)
                artifact = pom_obj.pop(length - 3)
                group = MavenArtifact._get_group_id(pom_obj)
                return (group, artifact, version)
        return (None, None, None)

    def __str__(self):
        return f"MavenArtifact[{self.group_id}:{self.artifact_id}:{self.version}]"

    @classmethod
    def _get_group_id(cls, objs) -> str:
        result = ""
        for idx, obj in enumerate(objs):
            if idx == 0:
                result = result.join(obj)
            else:
                result = f"{result}.{obj}"
        return result


class MavenRepository(Repository):
    FORMAT = RepositoryFormat.MAVEN

    def __init__(
        self,
        artifactory,
        name: str,
        type: RepositoryType,
    ):
        Repository.__init__(self, artifactory, name, MavenRepository.FORMAT, type)

    def upload_artefacts(self, dir: str):
        super().upload_artefacts(dir)
        maven_artefacts = MavenUtil.get_poms_jars(dir)
        for artefact in maven_artefacts:
            self._upload(self.name, artefact)

    def _upload(self, repository: str, artefact: MavenArtifact):
        file = {}
        pom_file = None
        jar_file = None
        if artefact.pom_path is not None:
            pom_file = {
                "maven2.asset1.extension": (None, "pom"),
                "maven2.asset1": (artefact.pom_path, open(artefact.pom_path, "rb")),
            }
        if artefact.jar_path is not None:
            jar_file = {
                "maven2.asset2.extension": (None, "jar"),
                "maven2.asset2": (artefact.jar_path, open(artefact.jar_path, "rb")),
            }
        data = {
            "maven2.groupId": (None, artefact.group_id),
            "maven2.artifactId": (None, artefact.artifact_id),
            "maven2.version": (None, artefact.version),
        }

        if (pom_file is not None) and (jar_file is not None):
            file.update(pom_file)
            file.update(jar_file)
        else:
            if pom_file is not None:
                file = pom_file
            if jar_file is not None:
                file = jar_file
                data["maven2.generate-pom"] = (None, True)

        params = {"repository": repository}
        file.update(data)

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


class MavenUtil:
    @classmethod
    def get_poms_jars(cls, dir: str) -> list:
        """
        Returns a list of jar and pom files in a directory
        """
        file_list = []
        dir_map = {}
        for root, dirs, files in os.walk(dir):
            maven_object = {}
            for filename in files:
                if filename.endswith(".pom") or filename.endswith(".jar"):
                    if root in dir_map:
                        maven_object = dir_map[root]
                    else:
                        dir_map[root] = maven_object
                    if filename.endswith(".pom"):
                        maven_object["pom"] = os.path.join(root, filename)
                    if filename.endswith(".jar"):
                        maven_object["jar"] = os.path.join(root, filename)
        for vals in dir_map.values():
            _pom = None
            _jar = None
            if "pom" in vals:
                _pom = vals["pom"]
            if "jar" in vals:
                _jar = vals["jar"]
            file_list.append(MavenArtifact(dir, _pom, _jar))
        return file_list
