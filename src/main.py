import os
import shutil


def main():
    src = "./static"
    dest = "./public"
    copy_files(src, dest)


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


if __name__ == "__main__":
    main()
