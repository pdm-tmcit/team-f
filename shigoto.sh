#!/bin/bash
awk -F, '{ print $2,$3 }' | sort | uniq
