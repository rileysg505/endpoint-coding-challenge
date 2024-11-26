class FileSystem():
    def __init__(self):
        self.filesystem = {}

    def create(self,path):
        """
        Creates a new directory at a given path.
        Input is expected to be a string representing the path to create.
        ex. path = "home/user/new_directory" 
        """
        path_parts = path.split("/")
        new_item = path_parts[-1]
        current_folder = self.get_folder(path_parts[:-1])        
        if new_item in current_folder:
            raise ValueError(f'Item: {new_item} already exists in path')

        current_folder[new_item] = {}


    def delete(self,path):
        """
        Deletes directory at a given path.
        Input is expected to be a string representing the path to delete.
        ex. path = "home/user/new_directory"
        """
        path_parts = path.split("/")
        item = path_parts[-1]
        # Navigate to the parent folder of the item to delete
        current_folder = self.get_folder(path_parts[:-1])
        if item not in current_folder:
            raise ValueError(f'Item: {item} does not exist in path {path}')
        
        if path_parts[-1] not in current_folder:
            raise ValueError(f'Item: {path_parts[-1]} does not exist in path {current_path}')
        del current_folder[path_parts[-1]]


    def list(self):
        '''
        Lists the contents of the filesystem in a tree-like structure.
        '''

        # Recursively list contents of the filesystem
        def list_contents(folder, depth=0, prefix=""):
            for item, contents in folder.items():
                print(prefix + "├──" + item)
                list_contents(contents, depth + 1, prefix + "│   ")
        
        
        list_contents(self.filesystem)
        return


    def move(self,old_path,new_path):
        '''
        Moves an item from one path to another.
        Input is expected to be two strings representing the old path and the new path.
        ex old_path = "home/user/item" new_path = "home/user/new_item"
        '''
        if old_path == new_path:
            raise ValueError("Old path and new path are the same.")
        path_parts = old_path.split("/")
        target = path_parts[-1]
        # Look for the item to move
        current_folder = self.get_folder(path_parts[:-1])

        if target not in current_folder:
            raise ValueError(f'Item: {item} does not exist in path {old_path}')
         
        
        children = current_folder[target]

        # Delete the item from the old path
        del current_folder[target]

        # Navigate to the new path
        path_parts = new_path.split("/")
        current_folder = self.get_folder(path_parts)
        
        if target in current_folder:
            raise ValueError(f'Item: {target} already exists in path {new_path}')

        current_folder[target] = children        

    def get_folder(self,path_parts):
        '''
        Returns the folder at a given path.
        Input is expected to be an array of strings representing the path to the folder.
        ex. path = ["home","user","item"] => "home/user/item"
        '''
        current_folder = self.filesystem
        i = 0
        while i < len(path_parts):
            item = path_parts[i]
            if item not in current_folder:
                raise ValueError(f'Parent folder: {path_parts[i]} does not exist.')
            current_folder = current_folder[item]
            i+=1
        return current_folder

def main():
    """
    Main entry point to enter our Directory Tree CLI
    """
    print("Welcome to the Endpoint Directory Tree CLI! Type 'exit' to quit.")
    
    fs = FileSystem()
    while True:
        # Prompt for user input
        user_input = input("Enter command: ")
        
        if user_input.lower() in {"exit", "quit"}:
            print("Thanks for checking the tool out!")
            break
        
        try:
            # Parse user input into arguments for argparse
            args = user_input.split()
            command = args[0].lower()
            path = args[1] if len(args) > 1 else None
            if command == "create":
                fs.create(path)
            elif command == "list":
                contents = fs.list()
            elif command == "delete":
                fs.delete(path)
            elif command == "move":
                # Default value for new_path is an null value
                # This allows us to move an item to the root directory
                new_path = args[2] if len(args) > 2 else None
                fs.move(path,new_path)
            else:
                print("Unknown command. Please try again.")
        
        except ValueError as ve:
            print(f"Cannot complete {command} | Error: {ve}")
        except IndexError:
            print(" Error: Missing arguments. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()