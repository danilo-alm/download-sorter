import filetype
import logging
import os

def main():
    global dirs_paths, dirs_paths_exist
    
    download_path = '/home/danilo/Downloads/fake-download-path'
    files = [os.path.join(download_path, file) for file in os.listdir(download_path)
             if os.path.isfile(os.path.join(download_path, file))]

    dirs_names = ('images', 'videos', 'documents', 'archives', 'audio', 'books')
    dirs_paths = {dir_name: os.path.join(download_path, dir_name.capitalize()) for dir_name in dirs_names}
    dirs_paths_exist = {name:os.path.exists(path) for name, path in dirs_paths.items()}
    
    typelist = get_filetypes(files)
    move_files(zip(files, typelist), dirs_paths)

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
    if not dirs_paths_exist[category]:
        os.mkdir(dirs_paths[category])
        logging.info(f'Directory for {category}: {dirs_paths[category]} was created')
        dirs_paths_exist[category] = True

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
            continue

        category = kind.mime.split('/')[0]
        if category in category_dirs:
            move_file(filepath, category_dirs[category])
        else:
            move_file(filepath, category)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()