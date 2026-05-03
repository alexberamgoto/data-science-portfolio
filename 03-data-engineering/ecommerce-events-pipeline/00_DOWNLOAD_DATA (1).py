import kagglehub
import shutil
from pathlib import Path

# https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store
path = kagglehub.dataset_download("mkechinov/ecommerce-behavior-data-from-multi-category-store")

target_dir = Path("data/in/")
target_dir.mkdir(parents=True, exist_ok=True)

for file in Path(path).iterdir():
    shutil.copy(file, target_dir / file.name)

print("Dataset wrote to: ", target_dir.resolve())