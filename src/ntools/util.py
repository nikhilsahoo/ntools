import os

class Util:
    @classmethod
    def get_files(cls, dir: str, types: list):
        dir_map = {}
        for root, dirs, files in os.walk(dir):
            dir_object = []
            for filename in files:
                for filetype in types:
                    if filename.endswith(filetype):
                        if root in dir_map:
                            dir_object = dir_map[root]
                        else:
                            dir_map[root] = dir_object
                        dir_object.append(os.path.join(root, filename))
        return dir_map
