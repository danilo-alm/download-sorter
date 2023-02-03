import filetype
import logging
import os

def main():
    typelist = get_filetypes(files)
    move_files(zip(files, typelist), dirs_paths)

def list_files(dirname: str) -> list:
    files = []
    for filename in os.listdir(dirname):
        filepath = os.path.join(dirname, filename)
        if os.path.isdir(filepath):
            continue
        files.append(filepath)
    return files

def get_filetypes(filelist: list) -> list:
    """ Returns a filetype.types object for each file in list """
    typelist = []
    for file in filelist:
        kind = filetype.guess(file)
        if kind is None:
            logging.info(f'Couldn\'t guess "{file}" filetype. Ignoring it.')
        typelist.append(kind)
    return typelist

def move_file(filepath: str, category: str):
    def create_dir_if_doesnt_exist(dirname):
        """ Creates dir in dirs_paths[dirname] location if it doesn't exist yet """
        if os.path.exists(dirs_paths[dirname]):
            logging.info(f'Directory for {dirname} already exists: {dirs_paths[dirname]}')
            return
        
        os.mkdir(dirs_paths[dirname])
        logging.info(f'Directory for {dirname}: {dirs_paths[dirname]} was created')
        dirs_paths_exist[dirname] = True
    
    if not dirs_paths_exist[category]:
        create_dir_if_doesnt_exist(category)
    os.rename(filepath, os.path.join(dirs_paths[category], os.path.basename(filepath)))

def move_files(files_plus_filetypes: list, dirs_paths: dict) -> None:
    """ Moves each file in its correct directory """
    
    def log_file_move(source, dest):
        """ Logs where the file was and where it was moved to """
        logging.info(f'File {source} moved to {dest}')

    category_dirs = {
        'image': 'images',
        'video': 'videos',
        'application': 'documents'
    }

    for filepath, kind in files_plus_filetypes:
        if kind is None:
            continue

        # Handle ebooks separately
        if kind.extension == 'epub' or kind.extension == 'mobi':
            move_file(filepath, 'books')

        category = kind.mime.split('/')[0]
        if category in category_dirs:
            move_file(filepath, category_dirs[category])
        else:
            move_file(filepath, category)

download_path = '/home/danilo/Downloads/fake-download-path'
files = list_files(download_path)

dirs_names = ('images', 'videos', 'documents', 'archives', 'audio', 'books')
dirs_paths = {dir_name: os.path.join(download_path, dir_name.capitalize()) for dir_name in dirs_names}
dirs_paths_exist = {name:os.path.exists(path) for name, path in dirs_paths.items()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()