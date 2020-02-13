# image-api-perf

Simple python script that takes an [IIIF Image API](`https://iiif.io/api/image/2.1/`) resource and makes requests for all tiles that make up the image.

Uses `@id` `width`, `height` and `tiles` parameters to generate a list of all tiles that would be required to generate full image at a specific scale factor.

## Getting Started

```bash
pip install requirements.txt

python test.py -image_url=http://path/to/image.jp2
```

### Arguments

The following args are available:

| Name | Description | Fallback |
| --- | --- | --- |
| image_url | The URL of iiif image api to use. | https://view.nls.uk/iiif/7443/74438561.5/info.json |
| scale_factor_index | The index of scaleFactor to use (e.g. for scaleFactors `[1, 2, 4, 8]`. 0 = 1, 2 = 2, 3 = 4 etc. | -1 (all) |
| dry_run | Whether this is a dry run (no http requests are made). | False |
| workers | The number of concurrent requests. | 10 |


 