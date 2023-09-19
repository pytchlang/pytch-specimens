# Tools for working with Pytch specimens

## Development server

Run with

```
cd $GIT_ROOT
./tools/serve-specimens.sh
```

## Deployment to production server

Create a tarfile of the zips and symlinks with

```
cd $GIT_ROOT/tools
poetry run python ./make_bundle.py /tmp/specimens.tar
```

Then `scp` that tarfile to the hosting server and untar under
`lesson-specimens`.

Alternatively, untar to a local temporary directory and then, within
that directory, use `rsync`:

```
rsync --del -vrlt -n . $USER@$HOST:$PATH
```

and then if all looks OK, repeat without the `-n` (dry-run) option.
