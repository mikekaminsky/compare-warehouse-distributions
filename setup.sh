#!/usr/bin/env bash

# Log commands and quit if you encounter any error
set -ex

vlad create_cluster
vlad add_security_group --use-my-current-ip
vlad describe_clusters

