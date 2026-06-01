import os

backend_dir = "backend"
folders = [
    "app",
    "app/api",
    "app/api/endpoints",
    "app/core",
    "app/models",
    "app/schemas",
    "app/services",
    "app/db",
    "tests"
]

for folder in folders:
    os.makedirs(os.path.join(backend_dir, folder), exist_ok=True)
    # create __init__.py
    with open(os.path.join(backend_dir, folder, "__init__.py"), "w") as f:
        pass

print("Backend folder structure created.")
