#!/usr/bin/env bash

# Log commands and quit if you encounter any error
set -ex

vlad --config-file dbconf.yml create_cluster 
vlad --config-file dbconf.yml add_security_group  --use-my-current-ip 
vlad --config-file dbconf.yml attach_iam_policy  RedshiftReadS3
vlad --config-file dbconf.yml describe_clusters 

