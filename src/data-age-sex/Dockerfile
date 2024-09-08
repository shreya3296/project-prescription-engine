FROM python:3.9-slim-buster

RUN pip install --no-cache-dir 'pandas==2.*' 'scikit-learn==1.*' 

WORKDIR /data
# references:
# * Downloading a file from the command line using Python (https://stackoverflow.com/a/17164052)
# * Unzipping files in Python (https://stackoverflow.com/a/64110098)
# Data set: https://figshare.com/articles/dataset/DDXPlus_Dataset_English_/22687585
RUN python3 -c "from urllib.request import urlretrieve; urlretrieve('https://figshare.com/ndownloader/files/40278013', 'release_evidences.json')"
RUN python3 -c "from urllib.request import urlretrieve; urlretrieve('https://figshare.com/ndownloader/files/40278010 ', 'release_conditions.json')"
RUN python3 -c "from urllib.request import urlretrieve; urlretrieve('https://figshare.com/ndownloader/files/40278019 ', 'release_train_patients.zip')" \
  && python3 -c "import shutil; shutil.unpack_archive('release_train_patients.zip', '.')" \
  && rm release_train_patients.zip

WORKDIR /app

COPY * .

ENTRYPOINT ["python", "/app/create_age_sex_dataset.py"]
