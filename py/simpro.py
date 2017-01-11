
import sys, os
import datetime
import json, copy

class SimpleProject :
    
    config = {     # 'para_name' : 'value',
            'profile_ext' : '.pro'
    }

    components = {  # 'component_name' : 'initializing content',
        'component' : '# initializing line',
    }


    def __init__(self, name = None, path = None, profile = None) :
        
        if name is None :
            name = ''
        if path is None :
            path = ''
            
        self.context = {}
        self.logs = []
            
        if profile is not None :

            # load project according to 'pro_file'
            
            result = self.load(profile)
        else :
            if path is not None and name is not None :
                self.log('Initialize with \'name\' : %s, and \'path\' : %s' % (name, path))
                
                # create project according to 'name' and 'path'
                
                self.name = name
                self.path = path
                result = self.create(name = self.name, path = self.path)
            else :  
                self.log('None \'name\' or \'path\'')
                result = None
                
        if result :
            self.log('Initialization succeeds.') 
        else :
            self.log('Initialization fails.')
            

    def __str__(self) :
        return "[SimpleProject name : %s , path : %s]" % (self.name, self.path)
    
    
    def log(self, logline) :
        timelabel = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.logs.append(timelabel + '\t' + logline)
        print('Log: %s' % logline)
   
   
    def error(self, errorline) :
        timelabel = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.logs.append(timelabel + '\t' + errorline)
        print('Error: %s' % errorline)
        
        
    def create(self, name, path) :

        # check if 'path' is a directory
        # check if there already exists a folder or file with the same name
        
        self.log('Create new project with \'name\' : %s, and \'path\' : %s' % (name, path))
        if name.__class__.__name__ == 'str' and path.__class__.__name__ == 'str' \
                and os.path.isdir(path) \
                and not os.path.isdir(os.path.join(path, name)) \
                and not os.path.exists(os.path.join(path, name)) :
                
            self.log('Create project directory and pro_file.') 
            os.mkdir(os.path.join(path, name))
            profile = os.path.join(path, name, name + self.config['profile_ext'])
                    
            # initialize and load the profile
            
            with open(profile, 'w') as f :
                json.dump(self.context, f)
                
            self.load(profile)
        else :
            self.error('Invalid \'name\' : %s, or \'path\' : %s' % (name, path)) 
            return False
            
        return True
        
        
    def load(self, profile) :

        # check if pro_file correctly indicates a Dao project.
        
        self.log('Load project with \'profile\' : %s' % profile)
        if profile.__class__.__name__ == 'str' \
                and len(profile) > len(self.config['profile_ext']) \
                and profile[-len(self.config['profile_ext']) : ] == self.config['profile_ext'] \
                and os.path.exists(profile) : 

            name = '' 
            path = ''
            is_name_consistent = False
            profile_split = profile.strip().split('/')
            
            if len(profile_split) >= 3 and len(profile_split[-1]) > len(self.config['profile_ext']) :
                name = profile_split[-1][ : -len(self.config['profile_ext'])]
                if len(profile_split[0]) < 1 :
                    profile_split[0] = '/'
                path = os.path.join(*profile_split[:-2])
                is_name_consistent = (name == profile_split[-2])
                
            if len(path) > 0 and len(name) > 0 and is_name_consistent :
                self.path = path
                self.name = name
                
                with open(profile, 'r') as f :
                    self.context = json.load(f)
                    
                self.validate() 
            else :
                self.error('Invalid \'profile\' : %s' % profile)
                return False 
        else :
            self.error('No such \'profile\' : %s' % profile)
            return False 
            
        return True


    def validate(self) : # check if config and files are valid and consistent.

        self.log("Validate the project.")
        
        try :
            if len(self.path) < 1 or len(self.name) < 1 :
                self.error('The project needs to be initialized properly.') 
                return False

            profile = os.path.join(self.path, self.name, self.name + self.config['profile_ext'])
            if not os.path.exists(profile) :
                self.error('The project has no valid profile: %s' % profile) 
                return False
                
            for component in self.components.keys() :
                component_path = os.path.join(self.path, self.name, component)
                        
                if not os.path.isdir(component_path) :
                    os.mkdir(component_path)
        except Exception as e:
            self.error("Exception happens during validating. %s" % e)
            return False
                        
        return True
    
    
    def new(self, component, name, ext = '') :
    
        self.log("Create new file with \'component\' : %s, \'name\' : %s, \'ext\' : %s" % 
                (component, name, ext))
                
        if component in self.components.keys() :
        
            if len(name) <= len(ext) or name[-len(ext) : ] != ext :
                name += ext
                
            new_file = os.path.join(self.path, self.name, component, name)
                    
            if not os.path.exists(new_file) :
                with open(new_file, 'w') as f :
                    f.write(self.components[component])
                self.log('Created file : %s' % new_file)
            else :  
                self.error('Failed to create the file : %s. It already exists.' % new_file)
                return False
        else :
            self.error('Invalid \'component\' : %s' % component)
            return False

        return True


    def save(self) :
        if self.validate() :
            self.log("Project is valid.")
            profile = os.path.join(self.path, self.name, self.name + self.config['profile_ext'])
            
            with open(profile, 'w') as f :
                json.dump(self.context, f)
            self.log("Save the project.")
            
            return True
        else :
            self.error("Project is not valid.")
            return False
        
        
    def exec(self) :
        self.save()

    def print_logs(self) :
        print('\nLogs : \n' + '-' * 64)
        for line in self.logs :
            print(line)
        print('-' * 64)


if __name__ == '__main__' :
    print('Developing test.')
    print('\nDone.')
    


    

