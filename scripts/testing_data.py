import kagglehub

# Download latest version
path = kagglehub.dataset_download("alexjr2001/formula-1-dataset-race-data-and-telemetry")

print("Path to dataset files:", path)
