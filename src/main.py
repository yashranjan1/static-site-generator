import os
from shutil import rmtree, copy
from helper_functions import markdown_to_html_node

def init() -> None:
    """
        Prepares the public folder and make sure that all the required folders and files exist

        Takes:
        
        Returns: `None`
    """
    if not os.path.exists('./static/'):
        raise Exception('static folder must exist')
    public_path = './public/'
    if os.path.exists(public_path):
        rmtree(public_path)
    os.mkdir('./public/')

def copy_files(from_path: str, to_path: str) -> None:
    """
        Copies over the files from static to public.

        Takes:
        `from_path: str` => A path to copy from 
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

    raise Exception('there is no h1 header')

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
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

    file = open(dest_path, 'x')
    file.write(html)
    file.close()

def main():
    init()
    copy_files('./static', './public')
    generate_page('./content/index.md','./template.html','./public/index.html')

if __name__ == "__main__":
    main()
