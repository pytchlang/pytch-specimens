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
