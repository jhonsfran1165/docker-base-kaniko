import os
import argparse
import yaml


# Define the command-line arguments that the script accepts
parser = argparse.ArgumentParser()
parser.add_argument('--file', help='the name of the file to write', required=True)
args = parser.parse_args()

# Get the path of the script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))


# Define the pipeline configuration template
pipeline_template = """
docker-build-{PROJECT}:
  extends: docker-build
  script: {PATH_PROJECT}
  when: 'always'
  variables:
    TERRAFORM_DIRECTORY: development
    PROJECT: oceana
    JSON_PLAN_FILE: development_plan.json
  only:
    - feat/devops-images
"""
  

# Define a list of dictionaries containing the values for the variables
variables_list = [
    {
        'PROJECT': 'project1',
        'PATH_PROJECT': './',
    },
    {
        'PROJECT': 'project2',
        'PATH_PROJECT': './',
    },
    {
        'PROJECT': 'project3',
        'PATH_PROJECT': './',
    }
]

data_pipeline = ""

# Iterate over the variables and create a configuration for each set
for variables in variables_list:
    # Use string formatting to insert the values of the variables into the template
    data_pipeline += pipeline_template.format(**variables)

# Load the configuration as a dictionary
pipeline = yaml.safe_load(data_pipeline)


# Write the configuration to a file
with open(os.path.join(script_dir, args.file), 'w') as file:
  yaml.dump(pipeline, file)
