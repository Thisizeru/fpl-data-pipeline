import subprocess

print ("beginning fpl pipeline execution")

subprocess.run(["python", "Extraction_file/extract.py"], check=True)

subprocess.run(["python", "Transformation_file/processing.py"], check=True)

subprocess.run(["python", "Load_file/load.py"], check=True)

print ("fpl pipeline execution completed successfully")