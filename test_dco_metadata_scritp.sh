#!/bin/bash

cd /BPC/python-scripts
echo "python dco_metadata_exapmles_per_dataset.py >1"
python dco_metadata_exapmles_per_dataset.py >1
echo "diff 1 <(gzip -dc /Users/ashipunova/Dropbox/mix/today_ch/dco_metadata/all_fields.gz)"
diff 1 <(gzip -dc /Users/ashipunova/Dropbox/mix/today_ch/dco_metadata/all_fields.gz)
