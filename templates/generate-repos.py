import os
import subprocess
import argparse
import yaml

#!/usr/bin/env python
from subprocess import check_output, STDOUT, CalledProcessError

# default image registry
REGISTRY_REPO=os.getenv("REGISTRY_REPO", "devops-images")

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='the name of the file to write', required=True)
parser.add_argument('--path', help='path where dockerfiles live', required=True)
parser.add_argument('--dockerfile', help='path of specific dockerfile you want to build', default="")
args = parser.parse_args()

# Get the path of the script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir   = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# the script you want to execute
script = os.path.join(root_dir, 'bin/build')
dockerfiles = ""

try:
    # execute the script and save the output -> bin/build
    dockerfiles = check_output(
        ["bash", script, REGISTRY_REPO, args.path, args.dockerfile],
        stderr=STDOUT, 
        text=True
    )
except CalledProcessError as exc:
    print(script, exc.output)
    exit

builds = dockerfiles.splitlines()

# Define the pipeline configuration template
pipeline_template = """
docker-build-{IMAGE_NAME}:
    extends: .docker-builds
    variables:
        CONTEXT: {CONTEXT}
        DOCKERFILE: {DOCKERFILE}
        IMAGE_NAME: {IMAGE_NAME}
        GLOBAL_SCRIPTS: {GLOBAL_SCRIPTS}
"""

data_pipeline = ""

for build in builds:
    [context, dockerfile, image_name, global_scripts] = build.split("*")

    data_pipeline += pipeline_template.format(
        CONTEXT=context,
        DOCKERFILE=dockerfile,
        IMAGE_NAME=image_name,
        GLOBAL_SCRIPTS=global_scripts
    )

# Load the configuration as a dictionary
pipeline = yaml.safe_load(data_pipeline)

# Write the configuration to a file
with open(os.path.join(script_dir, args.file), 'w') as file:
  yaml.dump(pipeline, file)
