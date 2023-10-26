# Part I - Model Implementation

In this part, the objective is to transcribe the functionality from the provided `.ipynb` file into the `model.py` file. Any identified bugs have been addressed during this process.

## Model Selection

The selection of the logistic regression model was made over the next key factors:

1. **Simplicity and Transparency**: Logistic regression is known for its simplicity and interpretability. This is especially important when dealing with predictive models that are used in real-world applications.

2. **Suitability for Binary Classification**: The problem at hand involves binary classification, where the objective is to predict delays (1) or no delays (0). Logistic regression is well-suited for this type of classification problem and can provide reliable results.

3. **Class Imbalance Handling**: The `class_weight='balanced'` parameter in logistic regression helps address class imbalance issues. This ensures that the model can handle scenarios where the occurrence of delays is less frequent.

4. **Scalability**: Logistic regression is computationally efficient and can handle a large volume of data. This is advantageous when dealing with a high number of flight records, which is often the case in real-time applications.

5. **Library and Community Support**: The choice of logistic regression is further reinforced by the ongoing maintenance and strong support provided by the `scikit-learn` library and its community. This ensures that the model can benefit from updates, enhancements, and a wealth of resources for continuous improvement.

## Model Implementation

The selected model has been implemented in the `model.py` file. This model includes methods for preprocessing data, model fitting, and making predictions. The features used for training the model have been predefined and are included in the `FEATURES_COLS` attribute.

## Data Preprocessing

The `preprocess` method is responsible for preparing raw data for training or predictions. It generates features from the input data and ensures that the necessary columns are present. Additionally, it encodes categorical variables using one-hot encoding.

## Model Training

The `fit` method is used to train the model with preprocessed data. The model employs logistic regression with class weighting for balanced performance.

## Making Predictions

The `predict` method is used to make predictions for new flights. It takes preprocessed features as input and returns predicted delay values as a list of integers.

To validate the model's functionality, it must pass tests executed with the command `make model-test`.

# Part II - API Implementation with FastAPI

The model is operationalized as an API using the `api.py` file and the FastAPI framework. The API successfully passes tests executed with the command `make api-test`.

## Health Check Endpoint

A health check endpoint is provided at `/health`. It responds with a JSON payload indicating the status of the API, ensuring its operational state.

## Prediction Endpoint

The prediction endpoint at `/predict` receives a JSON payload containing flight data. This data is processed to make predictions using the logistic regression. Several checks are performed to validate the input data, including the flight type ("TIPOVUELO") and the month ("MES"). The chosen features are generated using the model's `preprocess` method.

If any issues are encountered during the prediction process, the API responds with a 400 Bad Request status code and an error message. Otherwise, it returns the predictions in a JSON format.

## Part III - Deploying the API to a Cloud Provider (Recommendation: GCP)

In this part, we deploy the API to a cloud provider, with a recommendation to use Google Cloud Platform (GCP). The provided Dockerfile is configured for this deployment.

### Dockerfile Configuration

Below is the configuration of the Dockerfile used for deploying the API:

```Dockerfile
FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install anyio==3.4.0

EXPOSE 8080
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
```

1. `FROM python:3.9`: The base Python image selected for the container.
2. `WORKDIR /app`: Setting the working directory within the container.
3. `COPY . /app` Copying the application code into the container.
4. `RUN pip install -r requirements.txt` Installing Python dependencies from the requirements.txt file.
5. `RUN pip install anyio==3.4.0` Installing a specific version of the AnyIO library (in local environment often this library does not get installed, because of that in the docker file is forced to get installed).
6. `EXPOSE 8080` Exposing port 8080 within the container.
7. `CMD ["uvicorn", "challenge.apiapp", "--host", "0.0.0.0", "--port", "8080"]`: Command to execute your FastAPI application using Uvicorn, making it accessible on port 8080.

## Part IV - CI/CD Implementation

In Part IV, we establish a proper Continuous Integration (CI) and Continuous Delivery (CD) system for the development.

### Continuous Delivery (CD)

The Continuous Delivery workflow is triggered by pushes to the main or develop branches, ensuring that updates are automatically delivered to the specified environment. The workflow runs on an Ubuntu latest runner and consists of the following steps:

- **Checkout code**: This step checks out the latest code from the repository using the `actions/checkout` action.

- **Set up Python**: It configures the Python environment, specifically using Python 3.9, to ensure compatibility with the application.

- **Install dependencies**: Installs the necessary Python dependencies from the `requirements.txt` file, preparing the environment for the application.

- **Build and push Docker image**: This step involves building a Docker image for the application using the provided Dockerfile (`Dockerfile`). The image is then pushed to the designated container registry or Docker Hub repository.

### Continuous Integration (CI)

The Continuous Integration workflow is triggered by pushes to the main branch, the develop branch, or any feature branches. It runs on an Ubuntu latest runner and consists of the following steps:

- **Checkout code**: This step checks out the latest code from the repository using the `actions/checkout` action.

- **Set up Docker**: It sets up the Docker environment using the `docker/setup-action` action.

- **Verify Dockerfile**: This step builds a temporary Docker image using the provided `Dockerfile`. It ensures that the Dockerfile is correctly configured and can be used for containerization.
