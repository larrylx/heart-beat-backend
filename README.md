# Heart Beat

## Start Server in a container
```sh
docker build -t heart-beat:latest .
docker run -d -t -p 5000:5000 heart-beat:latest
```

## Update PIP Dependencies
```sh
pip install abc==xyz
pip freeze > requirements.txt
```

## Woking with CONDA
```sh
conda env create -f env.yml
conda env update -f env.yml
```