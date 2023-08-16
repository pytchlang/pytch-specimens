const fs = require("fs");

// More/less copied from webapp code.  Extract?
function transformFingerprint(transform) {
  switch (transform.targetType) {
    case "image": {
      const numberPieces = [
        transform.originX,
        transform.originY,
        transform.width,
        transform.height,
        transform.scale,
      ].map((x) => x.toExponential());
      const pieces = ["ImageTransform", ...numberPieces];
      const fingerprint = pieces.join("/");
      return fingerprint;
    }
    case "audio":
      return "";
  }
}

allTransforms = JSON.parse(fs.readFileSync(0));

allFingerprints = allTransforms.map(
  record => ({
    name: record.name,
    fingerprint: transformFingerprint(record.transform),
  })
);

process.stdout.write(JSON.stringify(allFingerprints));
