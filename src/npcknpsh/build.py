import os
import sys

import buildconfig

class Build:
    
    class ProjectNotFoundError(Exception):
        pass

    def __init__(self, config = None):
        self.config = config or buildconfig

    def project_class(self):
        return self.config.project_class

    def project_dir(self):
        
        project_dir = self.config.project_dir
        if project_dir:
            return project_dir

        script_file = sys.argv[0]
        script_path = os.path.dirname(script_file)
        
        current_path = script_path
        while True:

            current_path = os.path.dirname(current_path)
            items = os.listdir(current_path)
            files = (f for f in items if os.path.isfile(f))
            files = [f for f in files if f.endswith('.csproj')]

            if len(files):
                file = files[0]
                file_dir = os.path.dirname(file)
                return os.path.abspath(file_dir)

            next_path = os.path.dirname(current_path)
            if next_path == current_path:
                raise Build.ProjectNotFoundError()

            current_path = next_path

    def process(self):

        project_dir = self.project_dir()
        project_class = self.project_class()

        project = project_class(project_dir)
        project.pack()

if __name__ == '__main__':
    Build().process()