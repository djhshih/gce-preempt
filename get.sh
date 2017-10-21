#!/bin/bash

gcloud compute operations list > compute-operations.txt
grep 'compute.instances.preempted' compute-operations.txt > preemptions.txt

gcloud alpha genomics operations list > genomics-operations.txt
# if file names are sensitive, remember to redact them
