'''
生成目录以及附加信息,并同步到子目录docs

本脚本为以下脚本的修改版:
https://github.com/QSCTech/zju-icicles/blob/master/update.py
'''
import os

EXCLUDE_DIRS = ['.git', '.github', '.vscode', 'docs', 'site', 'assets']
README_MD = ['README.md', 'readme.md', 'index.md']

FASTGITHUB_REPO_BASE_URL = 'https://raw.fastgit.org/OpenWyu/wyu-courses-lib/'
BRANCH_PREFIX = FASTGITHUB_REPO_BASE_URL + 'master/'


def get_readme_path(root: str, file: str):
    return f'{root}/{file}'


def list_files(course: str):
    filelist_md = '## 文件列表\n\n'
    readme_path = ''
    for root, dirs, files in os.walk(course):
        # Intent level
        level = root.count(os.sep)
        # Make the separator unique
        if os.name != 'posix':
            root = root.replace(os.sep, os.altsep)
        indent = ' ' * 4 * level
        filelist_md += '{}- {}\n'.format(indent, os.path.basename(root))
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            if file not in README_MD:
                file_path = f'{BRANCH_PREFIX}{root}/{file}'
                filelist_md += f'{sub_indent}- [{file}]({file_path})\n'
            else:
                readme_path = get_readme_path(root, file)
    return filelist_md, readme_path


def generate_md(course: str, filelist_md: str, readme_path: str):
    result_md = ['\n', filelist_md]
    if readme_path:
        with open(readme_path, 'r', encoding='utf-8') as file:
            result_md = file.readlines() + result_md
    with open(f'docs/{course}.md', 'w', encoding='utf-8') as file:
        file.writelines(result_md)


if __name__ == "__main__":
    # Copy the index markdown
    with open('README.md', 'r', encoding='utf-8') as readme_md:
        with open('docs/index.md', 'w', encoding='utf-8') as index_md:
            index_md.writelines(readme_md)
    # Generate courses markdown
    courses = list(filter(lambda x: os.path.isdir(x) and (
                          x not in EXCLUDE_DIRS), os.listdir('.')))

    for course in courses:
        filelist_md, readme_path = list_files(course)
        generate_md(course, filelist_md, readme_path)
