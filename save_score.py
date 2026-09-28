import pickle, os
class File_Error(Exception):
    pass

class Save_System():
    def __init__(self, file_extension, save_folder):
        self.file_extension = file_extension
        self.save_folder = save_folder
        os.makedirs(self.save_folder, exist_ok=True)

    def save_score(self, data, name):
     try:
        save_file = open(self.save_folder+"/"+name+self.file_extension, "wb")
        pickle.dump(data, save_file)
        save_file.close()
     except FileNotFoundError:
        raise File_Error(f"Couldn't save '{name}' - folder '{self.save_folder}' does not exist.")
    

    def load_score(self, name):
     try:
        save_file = open(self.save_folder+"/"+name+self.file_extension, "rb")
        return pickle.load(save_file)
     except FileNotFoundError:
          raise File_Error("Failed to load score, save_file is either missing or doesnt exist.")

    def check_for_file(self,name):
            return os.path.exists(self.save_folder+"/"+name+self.file_extension)
     
        
          

    