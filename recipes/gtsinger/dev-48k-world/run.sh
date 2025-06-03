#!/bin/bash

# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

function xrun () {
    set -x
    $@
    set +x
}

# Set useful directory paths
script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
NNSVS_ROOT=$script_dir/../../../
NNSVS_COMMON_ROOT=$NNSVS_ROOT/recipes/_common/spsvs
NO2_ROOT=$NNSVS_ROOT/recipes/_common/no2

# Import yaml parser
. $NNSVS_ROOT/utils/yaml_parser.sh || exit 1;

# Parse config.yaml
eval $(parse_yaml "./config.yaml" "")

# Set output directory names
train_set="train_no_dev"
dev_set="dev"
eval_set="eval"
datasets=($train_set $dev_set $eval_set)
testsets=($dev_set $eval_set)

dumpdir=dump

dump_org_dir=$dumpdir/$spk/org
dump_norm_dir=$dumpdir/$spk/norm

stage=0
stop_stage=0

. $NNSVS_ROOT/utils/parse_options.sh || exit 1;

# exp name
if [ -z ${tag:=} ]; then
    expname=${spk}
else
    expname=${spk}_${tag}
fi
expdir=exp/$expname

# Stage -1: Data downloading
if [ ${stage} -le -1 ] && [ ${stop_stage} -ge -1 ]; then
    # If database directory doesn't exist
    if [ ! -e $(eval echo $db_root) ]; then
    # Print multi-line output with cat
	cat<<EOF
stage -1: Downloading

This recipe does not automatically download GTSinger. To use, download parts or
the whole dataset manually.

Visit https://github.com/AaronZ345/GTSinger to learn more.
EOF
    fi
fi

if [ ${stage} -le 0 ] && [ ${stop_stage} -ge 0 ]; then
    echo "stage 0: Data preparation"
    
    # Step 1:
    # Generate full-context labels from musicxml

    # Will likely create a custom version of this script
    python $NO2_ROOT/utils/musicxml2lab.py ./config.yaml
fi