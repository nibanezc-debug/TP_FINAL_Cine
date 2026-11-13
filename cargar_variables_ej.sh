#!/usr/bin/env bash

export $(grep -v '^#' CINE_APP .env | xargs)