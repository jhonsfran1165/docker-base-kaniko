import yaml

# Define the pipeline configuration template
pipeline_template = """
docker-build-{PROJECT}:
  stage: build
  script: {PATH_PROJECT}
  when: 'always'
  only:
    - feat/devops-cicd
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

# Iterate over the variables and create a configuration for each set
for variables in variables_list:
    # Use string formatting to insert the values of the variables into the template
    pipeline_config = pipeline_template.format(**variables)

    # Load the configuration as a dictionary
    pipeline = yaml.safe_load(pipeline_config)

    # Write the configuration to a file
    with open(f'.gitlab-ci-{variables["PROJECT"]}.yml', 'w') as file:
        yaml.dump(pipeline, file)
