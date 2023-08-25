import tempfile
from pathlib import Path
import tarfile
import http.server
import socketserver
import os
import click

import make_bundle

class CorsRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    extensions_map = {
        k: v + (';charset=UTF-8' if v.startswith('text/') else '')
        for k, v in http.server.SimpleHTTPRequestHandler.extensions_map.items()
    }


class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main(port):
    with tempfile.TemporaryDirectory() as tmpdir:
        tar_path = Path(tmpdir) / "content.tar"
        dist_dir_path = Path(tmpdir) / "dist"

        click.echo(f"Creating content tarfile in {tmpdir}")
        make_bundle.main(str(tar_path))

        click.echo(f"Unpacking content tarfile to {tmpdir}/dist")
        os.mkdir(dist_dir_path)
        with tarfile.open(tar_path) as tar_file:
            tar_file.extractall(dist_dir_path)

        click.echo(f"Serving content at http://localhost:{port}/")
        os.chdir(dist_dir_path)
        with ReuseAddrTCPServer(("", port), CorsRequestHandler) as httpd:
            httpd.serve_forever()


@click.command()
@click.option("-p", "--port", type=int, default=8128)
def main_cmd(port):
    main(port)


if __name__ == "__main__":
    main_cmd()
