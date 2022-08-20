import yaml
import sys
with open('regression-training-ex-1.yaml', 'r') as yaml_file:
    file = yaml.load(yaml_file, Loader=yaml.FullLoader)
print(file)