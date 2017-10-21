#!/usr/bin/env python3

import yaml

output_fname = "preemptible-operations.tsv"
outf = open(output_fname, 'w')
outf.write('\t'.join(
    ["operation", "labels", "start", "end", "instance", "machine_type", "zone", "preempt_time"]
) + '\n')

preempted = {}
with open("preemptions.txt") as inf:
    for line in inf:
        tokens = line.split()
        if tokens[1] == "compute.instances.preempted":
            instance = tokens[2].split('/')[2]
            time = tokens[5]
            if instance in preempted:
                raise RuntimeError("instance must be unique")
            else:
                preempted[instance] = time

xs = yaml.load_all(open("genomics-operations.yaml").read())
for x in xs:
    if x["done"]:
        meta = x["metadata"]
        resources = meta["request"]["ephemeralPipeline"]["resources"]
        preemptible = resources["preemptible"]
        if not preemptible: continue

        name = x["name"]
        start = meta["startTime"]
        end = meta["endTime"]
        labels = ",".join(meta["labels"].values())
        #events = meta["events"]
        
        engine = meta["runtimeMetadata"]["computeEngine"]
        instance_name = engine["instanceName"]
        machine_type = engine["machineType"]
        machine_type = machine_type[machine_type.find('/')+1:]
        zone = engine["zone"]

        if instance_name in preempted:
            preempt_time = preempted[instance_name]
        else:
            preempt_time = ""

        outf.write('\t'.join([name, labels, start, end, instance_name, machine_type, zone, preempt_time]) + '\n')


outf.close()

