import os
import tempfile
import subprocess
from lib.git import GitRepository

class Component:
    def __init__(self, data):
        self._name = data['name']
        self._repository = data['repository']
        self._ref = data['ref']

    def name(self):
        return self._name

    def repository(self):
        return self._repository

    def git_repository(self):
        return self._git_repository

    def ref(self):
        return self._ref

    def artifacts(self):
        return self._artifacts

    def checkout(self):
        self._git_repository = GitRepository(self.repository(), self.ref())

    # script overridden in this repo
    def custom_component_script_path(self):
        dirname = os.path.dirname(os.path.abspath(__file__))      
        return os.path.realpath(os.path.join(dirname, '../../../scripts/bundle-build/components', self.name(), 'build.sh'))

    # script inside the component repo
    def component_script_path(self):
        dirname = self.git_repository().dir()     
        return os.path.realpath(os.path.join(dirname, 'scripts/build.sh'))

    # default gradle script
    def default_script_path(self):
        dirname = os.path.dirname(os.path.abspath(__file__))      
        return os.path.realpath(os.path.join(dirname, '../../../scripts/bundle-build/standard-gradle-build/build.sh'))

    def build_script(self):
        paths = [self.component_script_path(), self.custom_component_script_path(), self.default_script_path()]
        return next(filter(lambda path: os.path.exists(path), paths), None)

    def build(self, version, arch):
        build_script = f'{self.build_script()} {version} {arch}' 
        print(f'Running {build_script} ...')
        self.git_repository().execute(build_script)

    def artifacts_path(self):
        dirname = self.git_repository().dir()
        return os.path.realpath(os.path.join(dirname, 'artifacts'))

    def export(self, dest):
        artifacts_path = self.artifacts_path()
        if os.path.exists(artifacts_path):
            print(f'Publishing artifacts from {artifacts_path} into {dest} ...')
            self.git_repository().execute(f'cp -r "{artifacts_path}/"* "{dest}"')
            self.set_artifacts()
        else:
            print(f'No artifacts found in {artifacts_path}, skipping.')

    def set_artifacts(self):
       self._artifacts = {key: self.file_paths(key) for key in ["maven", "plugins", "bundle", "libs"] if self.file_paths(key)}

    def file_paths(self, dir_name):
      artifacts_path = self.artifacts_path()
      sub_dir = os.path.join(artifacts_path, dir_name)
      file_paths = []
      if os.path.exists(sub_dir):
        for dir, dirs, files in os.walk(sub_dir):
          for file_name in files:
            path = os.path.relpath(os.path.join(dir, file_name), artifacts_path)
            file_paths.append(path)
      return file_paths

    def dict(self):
        return {
            'name': self.name(),
            'repository': self.repository(),
            'ref': self.ref(),
            'sha': self.git_repository().sha(),
            'artifacts': self.artifacts()
        }
