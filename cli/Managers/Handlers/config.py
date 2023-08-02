from json import load

class Config:
    
    def get_file_contents(self, file):
        with open(file, "r") as file:
            return load(file)
