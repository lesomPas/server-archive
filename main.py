import shutil
from pathlib import Path
import subprocess
import sys

file_name = "78eiaAMgBgA="

def zip_with_parent(source_folder: str, output_zip: str):
    """
    压缩文件夹，保留父级目录结构
    例如: /home/user/project/src -> zip内: project/src/...
    """
    source = Path(source_folder).resolve()
    parent = source.parent      # 父目录作为 root_dir
    base = source.name          # 目标文件夹作为 base_dir

    # output_zip 不需要 .zip 后缀，make_archive 会自动添加
    shutil.make_archive(
        base_name=output_zip.replace('.zip', ''),  # 输出路径（无后缀）
        format='zip',
        root_dir=parent,        # zip 的根目录
        base_dir=base           # 要打包的相对目录
    )
    print(f"[info] created successfully: {output_zip}")


def commit(date: str, state: str = "release", archive: int = 1, branch: str = "main") -> None:
    zip_with_parent(file_name, f"archives/SauionServer.{branch}.{date}.archive{archive}.{state}")

    shutil.rmtree(file_name)
    print("[info] removed successfully: {file_name}")

    subprocess.run(f'git add . && git commit -m {date} && git push origin main', shell=True)
    print("[info] pushed successfully")

def main():
    args = sys.argv

    if not Path(file_name).is_dir():
        print(f"[error] not found dir: {file_name}")
        return

    if len(args) < 2:
        print("[error] required date")
        return

    if len(args) > 5:
        print(f"[error] extra args: {args[5]}")
        return

    try:
        commit(*args)
    except Exception:
        print("[error] made archive failed")

if __name__ == "__main__":
    main()
