# README

Fruits classification app (BuildID: 437)

- This app classifies 7 fruits (apple, avocado, banana, cherry, mango, orange, peach)
- Trained fruit images from [https://www.kaggle.com/moltean/fruits](https://www.kaggle.com/moltean/fruits)

## Model 

Train the model with fruits dataset from [kaggle](https://www.kaggle.com/moltean/fruits) using following notebook:

- [Train notebook](./train/Fruits-Train.ipynb)
- [Test notebook]((./train/Fruits-Test.ipynb))

This app trained only 7 fruits (apple, avocado, banana, cherry, mango, orange, peach) from the dataset.

## Docker image

You can train your own model or download pre-trained models from following url
- [fruits-01-0.7265.h5](https://drive.google.com/uc?id=1FeRRMmEh9OEv4YyHLa8bR8rOm2j7edlq&export=download)
- [fruits-05-0.0264.h5](https://drive.google.com/uc?id=1OpN3YfBeMNznKzneawcYEXEbULuW0pz9&export=download)

Once you have models and upload to your blob storage.

Build a docker image for deployment (to AKS, ACI or Web App for Container)

```bash
docker build -f Dockerfile --build-arg MODELURL=https://yourblob.blob.core.windows.net/model/fruits-05-0.0264.h5 -t myfruits .
```

Run docker image with environment variables, `MODELPATH`, `BLOBACCT`, and `BLOBKEY`.

```bash
docker run -p 8080:8080 -e "MODELPATH=/models/fruits.h5" -e "BLOBACCT=_blob_account_" -e "BLOBKEY=_blob_ket_" -d fruits
```

## Local test

```bash
export MODELPATH=../models/fruits-05-0.0264.h5
export BLOBACCT=_blob_account_
export BLOBKEY=_blob_ket_
python app.py
```