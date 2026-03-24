import os
import shutil
from block_markdown import markdown_to_html_node, extract_title


def delete_dir_files(file_path):
    child_dirs = os.listdir(file_path)
    if len(child_dirs) == 0:
        return
    for child_dir in child_dirs:
        path = os.path.join(file_path, child_dir)
        if os.path.isdir(path):
            delete_dir_files(path)
            os.removedirs(path)
        elif os.path.isfile(path):
            os.remove(path)


def copy_files_recur(src, dest):
    src_abs_path = os.path.abspath(src)
    dest_abs_path = os.path.abspath(dest)
    child_dirs = os.listdir(src_abs_path)
    if len(child_dirs) == 0:
        return
    for child_dir in child_dirs:
        src_sub_path = os.path.join(src_abs_path, child_dir)
        dest_sub_path = os.path.join(dest_abs_path, child_dir)
        if os.path.isdir(src_sub_path):
            os.mkdir(dest_sub_path)
            copy_files_recur(src_sub_path, dest_sub_path)
        elif os.path.isfile(src_sub_path):
            shutil.copy(src_sub_path, dest_sub_path)


def copy_files(src, dest):
    if not os.path.exists(src):
        raise ValueError("source folder does not exist")
    if os.path.exists(dest):
        delete_dir_files(dest)
    else:
        os.mkdir(dest)
    copy_files_recur(src, dest)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        md = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", content)
    dirname = os.path.dirname(dest_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(dest_path, "w") as file:
        file.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    child_dirs = os.listdir(dir_path_content)
    if len(child_dirs) == 0:
        return
    for child_dir in child_dirs:
        path = os.path.join(dir_path_content, child_dir)
        if os.path.isdir(path):
            dest_sub_path = os.path.join(dest_dir_path, child_dir)
            os.mkdir(dest_sub_path)
            generate_pages_recursive(path, template_path, dest_sub_path)
        elif os.path.isfile(path):
            generated_file_name = child_dir.split(".")[0] + ".html"
            dest_sub_path = os.path.join(dest_dir_path, generated_file_name)
            generate_page(path, template_path, dest_sub_path)


def main():
    src = "./static"
    dest = "./public"
    copy_files(src, dest)
    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()
