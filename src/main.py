import os
import sys
from shutil import rmtree, copy
from helper_functions import markdown_to_html_node

def init() -> None:
    """
        Prepares the docs folder and make sure that all the required folders and files exist

        Takes:
        
        Returns: `None`
    """
    if not os.path.exists('./static/'):
        raise Exception('static folder must exist')
    public_path = './docs/'
    if os.path.exists(public_path):
        rmtree(public_path)
    os.mkdir('./docs/')

def copy_files(from_path: str, to_path: str) -> None:
    """
        Copies over the files from static to destination.

        Takes:

        `to_path: str` => A path to copy to
        
        Returns: `None`
    """
    files = os.listdir(from_path)
    for file in files:
        if os.path.isfile(f'{from_path}/{file}'):
            copy(f'{from_path}/{file}', to_path)
        else:
            if not os.path.exists(f'{to_path}/{file}'):
                os.mkdir(f'{to_path}/{file}')
            copy_files(f'{from_path}/{file}', f'{to_path}/{file}')
    
def extract_title(markdown: str) -> str:
    """
        Reads a file and extracts first line that is a header1 from import 

        Takes:
        `markdown: str` => The markdown text

        Returns
        `title: str` => The title
    """

    markdown_blocks = markdown.split('\n')

    for line in markdown_blocks:
        stripped_line = line.lstrip().rstrip()
        if stripped_line.startswith('# '):
            return stripped_line.lstrip('# ')

    raise Exception(f'there is no h1 header in {markdown}')

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    """
        Generates the HTML page

        Takes:
        `from_path: str` => the path of the md file to be converted
        `template_path: str` => the path of the template file 
        `dest_path: str` => the path of the destination html file

        Returns
        `None`
    """
    
    print(f'Generating pades from {from_path} to {dest_path} using {template_path}')
    file = open(from_path)
    markdown = file.read()
    file.close()
    file = open(template_path)
    html = file.read()
    file.close()
    
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    html = html.replace('{{ Title }}', title)
    html = html.replace('{{ Content }}', content)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    file = open(dest_path, 'x')
    file.write(html)
    file.close()

def generate_page_recursive(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    """
        Recursively runs `generate_page` on all files and subfiles in the `from_path` directory

        Takes:
        `from_path: str` => the path of the md file to be converted
        `template_path: str` => the path of the template file 
        `dest_path: str` => the path of the destination html file

        Returns
        `None`
    """
    files = os.listdir(from_path)
    for file in files:
        if os.path.isfile(f'{from_path}/{file}'):
            new_file_name = f'{file.split('.')[0]}.html'
            generate_page(f'{from_path}/{file}', template_path, f'{dest_path}/{new_file_name}', basepath)
        else:
            if not os.path.exists(f'{dest_path}/{file}'):
                os.mkdir(f'{dest_path}/{file}')
            generate_page_recursive(f'{from_path}/{file}', template_path, f'{dest_path}/{file}', basepath)

def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    init()
    copy_files('./static', './docs')
    generate_page_recursive('./content','./template.html','./docs', basepath)

if __name__ == "__main__":
    main()
