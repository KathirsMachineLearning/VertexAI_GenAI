from io import FileIO
import yaml
import os
from os import listdir
from os.path import isfile, join

class YamlConverter:
  
  def ConvertYamltoObject(self, yamlConfigurationPath):
    objectList = []
    cwd = yamlConfigurationPath
    onlyfiles = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(cwd) for filename in filenames if filename.endswith('.yaml')]
    for file in onlyfiles:      
      if "template.yaml" not in file: 
        with open(file) as f:
          dataMap = yaml.safe_load(f)
          objectList.append(dataMap)
        continue
    return objectList
  
  def ConvertObjectToYaml(self, object, filepath:str):  
    with open(filepath, 'w') as file:
      yaml.dump(object, file)