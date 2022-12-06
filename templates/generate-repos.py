import os, subprocess
import argparse
import yaml


# Define the command-line arguments that the script accepts
parser = argparse.ArgumentParser()
parser.add_argument('--file', help='the name of the file to write', required=True)
args = parser.parse_args()

# Get the path of the script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir   = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


# Define the pipeline configuration template
pipeline_template = """
docker-build-{PROJECT}:
  stage: devops-build
  script:
    - bin/build {CI_REGISTRY_IMAGE} {PATH_PROJECT}
  interruptible: true
  # cache:
  #   <<: *global_cache
  when: 'always'
  only:
    - feat/devops-images
"""

# images is the default directory for all docker images
path        = os.path.join(root_dir, 'images')
directories = os.listdir(path)

data_pipeline = ""

for directory in directories:
    path_project = path + "/" + directory
    # Use string formatting to insert the values of the variables into the template
    data_pipeline += pipeline_template.format(
        PATH_PROJECT=path_project,
        PROJECT=directory,
        CI_REGISTRY_IMAGE=os.getenv("CI_REGISTRY_IMAGE", "devops-images") # should live in the CICD
    )

# Load the configuration as a dictionary
pipeline = yaml.safe_load(data_pipeline)

# Write the configuration to a file
with open(os.path.join(script_dir, args.file), 'w') as file:
  yaml.dump(pipeline, file)
