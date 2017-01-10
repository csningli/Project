
import sys, os

sys.path.append('../py/')   # add the path to the directory containing simpro.py. 
sys.path.append('./py/')    # add the path to the directory containing simpro.py. 

from simpro import SimpleProject

class ExampleProject(SimpleProject) :
   
    config = {
        'profile_ext' : '.egpro',   # configure the default extension of project profile. 
    }
    
    components = {  # add example components
        'component1' : '# this is a component1 file.',
        'component2' : '# this is a component2 file.',
    }

    def __init__(self, path_to_project = None) :
        
        # In this example, we change the initialization parameter to a single path directing
        # to a project directory. 
        # If this directory dose not exist, then create it; 
        # If the directory already exists and has a .egpro .

        # * During the initialization, for any case, it should result in a calling 
        # of SimpleProject.__init__() with proper parameters. 

        if path_to_project is not None and len(path_to_project) > 0 :
            # resolve 'path_to_project' to get 'path' and 'name'

            if path_to_project[-1] == '/' :
                path_to_project = path_to_project[ : -1]

            name = os.path.basename(path_to_project)
           
            if os.path.isdir(path_to_project) :
                profile_path = os.path.join(path_to_project, name + self.config['profile_ext'])
                if os.path.exists(profile_path) :
                    super(ExampleProject, self).__init__(profile = profile_path)
                else :
                    super(ExampleProject, self).__init__()
                    print('Directory already exists and it has no valid profile.')
            else :
                path = os.path.dirname(path_to_project)
                super(ExampleProject, self).__init__(path = path, name = name)
        else :
            super(ExampleProject, self).__init__()
            print('The project should be properly initialized.')
       

    def validate(self) :
        
        # In the subclass' validate method, should call super().validate at first. 

        super(ExampleProject, self).validate()

        # Do some subclass specified validating.

    def new(self, component, name) :
        if component in self.components.keys() :
            if component == 'component1' :
                return super(ExampleProject, self).new(
                        component = 'component1', 
                        name = name, 
                        ext = '.c1')
            elif component == 'component2' :
                return super(ExampleProject, self).new(
                        component = 'component2', 
                        name = name, 
                        ext = '.c2')
            else :
                return super(ExampleProject, self).new(
                        component = component, 
                        name = name, 
                        ext = '.cx')
        else :
            self.error('Invalid \'componnet\' : %s' % component)
            return False
        
        
    def exec(self) :
        
        # Do some subclass specified execution.
        
        pass


if __name__ == "__main__" :
    path = './TestExample'
    name = 'helloworld'
    path_to_project = os.path.join(path, name)
    example = ExampleProject(path_to_project) 
    print(example)
    example.print_logs()


