import click
import io
from pathlib import Path
import shutil
import tarfile
import zipfile
import time
import content_hash


def walked_relative_paths(dir):
    return [
        fpath.relative_to(dir)
        for fpath in dir.rglob("*")
        if not fpath.is_dir()
    ]


def add_specimen(bundle_tar, root_dir, specimen_relative_path):
    specimen_path = root_dir / specimen_relative_path
    specimen_zip_path = f"{specimen_relative_path}.zip"

    specimen_zip_io = io.BytesIO()
    with zipfile.ZipFile(specimen_zip_io, "w") as zip:
        for entry_path in walked_relative_paths(specimen_path):
            zip.write(specimen_path / entry_path, arcname=entry_path)
    specimen_zip_io.seek(0)

    specimen_zip_buf = specimen_zip_io.getbuffer()
    zip_tarinfo = tarfile.TarInfo(specimen_zip_path)
    zip_tarinfo.size = len(specimen_zip_buf)
    zip_tarinfo.mode = 0o444
    zip_tarinfo.mtime = time.time()

    bundle_tar.addfile(zip_tarinfo, specimen_zip_io)

    hash = content_hash.project_content_hash(specimen_path)
    link_tarinfo = tarfile.TarInfo(f"_by_content_hash_/{hash}.zip")
    link_tarinfo.type = tarfile.SYMTYPE
    link_tarinfo.linkname = f"../{specimen_zip_path}"
    link_tarinfo.mode = 0o444
    bundle_tar.addfile(link_tarinfo)


def pytch_project_dirs(base_dir):
    """Heuristically discover all directories under BASE_DIR which contain
    Pytch projects.
    """
    return [
        fpath.relative_to(base_dir)
        for fpath in base_dir.rglob("*")
        if (
            fpath.is_dir()
            and (fpath / "version.json").is_file()
            and (fpath / "meta.json").is_file()
        )
    ]


repo_root = Path(__file__).resolve().parent.parent
specimens_root = Path(repo_root) / "specimens"


def main(out_tarfile):
    bundle_tar_io = io.BytesIO()
    bundle_tar = tarfile.TarFile(mode="w", fileobj=bundle_tar_io)

    for specimen_path in pytch_project_dirs(specimens_root):
        add_specimen(bundle_tar, specimens_root, specimen_path)

    bundle_tar_io.seek(0)

    with open(out_tarfile, "wb") as f_out:
        shutil.copyfileobj(bundle_tar_io, f_out)


@click.command()
@click.argument("out-tarfile", type=click.Path(dir_okay=False))
def main_cmd(out_tarfile):
    main(out_tarfile)


if __name__ == "__main__":
    main_cmd()
