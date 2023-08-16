import click
import hashlib
import json
import mimetypes
from pathlib import Path
import subprocess
import unicodedata


def mimetype(url):
    maybe_type = mimetypes.guess_type(url)[0]
    if maybe_type is None:
        raise RuntimeError(f'could not guess mime-type of "{url}"')
    return maybe_type


def asset_transform_fingerprints(asset_metadata_file):
    # This is horrible but we want to match JavaScript's
    # floating-point representation exactly.
    result = subprocess.run(
        ["node", "transform-fingerprints.js"],
        stdin=asset_metadata_file,
        capture_output=True,
    )
    return json.loads(result.stdout)


def sha256hex(data_or_string):
    data = (
        unicodedata.normalize("NFC", data_or_string).encode("utf-8")
        if isinstance(data_or_string, str)
        else data_or_string
    )
    return hashlib.sha256(data).hexdigest()


def program_fingerprint(program):
    kind = program["kind"]
    if kind == "flat":
        hash = sha256hex(program["text"])
        return f"program=flat/{hash}"
    else:
        raise RuntimeError(f'unknown program-kind "{kind}"')


def project_fingerprint(root_dir):
    with (root_dir / "code" / "code.json").open("rb") as f_in:
        code_obj = json.load(f_in)
        program_fingerprint_line = program_fingerprint(code_obj)

    with (root_dir / "assets" / "metadata.json").open("rb") as f_in:
        asset_fingerprint_records = asset_transform_fingerprints(f_in)
        transform_fingerprint_from_asset = {
            record["name"]: record["fingerprint"]
            for record in asset_fingerprint_records
        }

    def asset_fingerprint(asset):
        name_hash = sha256hex(asset.name)
        mimetype_hash = sha256hex(mimetype(asset))
        content_hash = sha256hex(asset.read_bytes())
        transform_hash = sha256hex(transform_fingerprint_from_asset[asset.name])
        fingerprint = f"{name_hash}/{mimetype_hash}/{content_hash}/{transform_hash}"
        return fingerprint

    asset_fingerprints = sorted(
        [
            asset_fingerprint(asset)
            for asset in (root_dir / "assets" / "files").iterdir()
        ]
    )
    assets_fingerprint = f"assets={','.join(asset_fingerprints)}"

    return f"{program_fingerprint_line}\n{assets_fingerprint}\n"


def project_content_hash(root_dir):
    return sha256hex(project_fingerprint(root_dir))


@click.command()
@click.argument(
    "root_path", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def main(root_path):
    """Print the content-hash of the project at the given ROOT_PATH."""
    print(project_content_hash(Path(root_path)))


if __name__ == "__main__":
    main()
