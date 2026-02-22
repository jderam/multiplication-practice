#!/bin/bash

# This script copies all website files from the source directory to the destination directory.
SOURCE_DIR=./public
REMOTE_DIR=/var/www/html/multiplication-practice

rsync --archive --verbose --progress --exclude='multiplication_practice.sqlite' ${SOURCE_DIR}/ pi-zero-w:${REMOTE_DIR}/

# Copy the sqlite database only if it doesn't already exist on the target
rsync --archive --verbose --progress --ignore-existing ${SOURCE_DIR}/multiplication_practice.sqlite pi-zero-w:${REMOTE_DIR}/multiplication_practice.sqlite
