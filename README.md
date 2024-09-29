---

# GCN HTTP Server

This repository hosts an HTTP server that processes HTTP requests to perform tasks related to a **Graph Convolutional Network (GCN)**, a neural network that operates directly on graph-structured data. It also features support for uploading images to cloud storage like Azure or AWS. The primary goal of this project is to offer a web-accessible interface for GCN processing, useful for node classification tasks on graph data (e.g., social networks, citation networks).

## Features

- **Graph Convolutional Network (GCN) Inference**: The server performs node classification using a pre-trained GCN model on input graph data (e.g., `.npz` files).
- **HTTP Request Handling**: The server listens for HTTP POST requests containing graph data and returns results such as training losses, node embeddings, or predictions.
- **Cloud Integration**: Supports optional integration with cloud services (Azure, AWS) for uploading and managing graph data files or images.
- **Real-time Data Processing**: Graph data can be processed in real-time as it is sent to the server, providing immediate feedback on results.

## Prerequisites

Before setting up the server, ensure you have the following dependencies installed:

- **Python 3.6+**
- **PyTorch**: For the GCN model and neural network operations.
- **Flask**: For running the HTTP server.
- **NumPy, SciPy**: Required for numerical and graph operations.
- **Matplotlib**: For visualizing training loss and accuracy.
- **Pandas**: For managing dataframes and results.
- **Scikit-learn**: For accuracy calculation and other ML utilities.
- **Cloud SDKs** (Optional): Azure SDK, Boto3 for AWS S3 integration.

## Installation

You can set up the project using Docker or manually through a Python environment.

### Option 1: Using Docker

1. Clone the repository:

    ```bash
    git clone https://github.com/wildanazz/gcn-http-server.git
    cd gcn-http-server
    ```

2. Build the Docker image:

    ```bash
    docker build -t gcn-http-server .
    ```

3. Run the Docker container:

    ```bash
    docker run -p 5000:5000 gcn-http-server
    ```

This will start the server and bind it to port `5000`.

### Option 2: Manual Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/wildanazz/gcn-http-server.git
    cd gcn-http-server
    ```

2. Set up a virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate  # Linux/MacOS
    # For Windows use: .\env\Scripts\activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Start the server:

    ```bash
    python server.py
    ```

The server will be running on `http://localhost:5000`.

## Configuration

### Environment Variables

You can configure cloud storage keys or other sensitive information through a `.env` file. The following environment variables should be defined if cloud integration is required:

- `AZURE_STORAGE_KEY` – Azure storage access key.
- `AWS_ACCESS_KEY_ID` – AWS access key.
- `AWS_SECRET_ACCESS_KEY` – AWS secret access key.

### Server Configuration

- **Port**: The default port is `5000`. You can change it in `server.py`.
- **Graph Data**: Graph data is sent via POST requests in `.npz` format.

## Usage

Once the server is running, it can process incoming HTTP POST requests containing graph data in `.npz` format. For example, to upload and process a Facebook page graph file:

```bash
curl -X POST -F "data=@/path/to/data/facebook.npz" http://localhost:5000/upload
```

You can also use Python's `requests` library to send data programmatically:

```python
import requests

with open('/path/to/data/facebook.npz', 'rb') as file:
    response = requests.post('http://localhost:5000/upload', files={'data': file})

print(response.json())
```

### Example Input

- **Graph Data**: `.npz` files representing the graph structure, with adjacency matrix, feature matrix, and labels.
- **POST Endpoint**: `/upload`
  
### Example Output

- **Node embeddings** for the graph.
- **Training loss** and **Accuracy plots**.
- **Classification results** in JSON format.

## GCN Model

The server uses a **Graph Convolutional Network (GCN)** model to process the graph data. GCNs are designed to handle graph-structured inputs by leveraging the connectivity patterns (edges) and node features to learn effective representations. 

The input data consists of:
- **Adjacency Matrix**: Represents the graph's connections.
- **Node Features Matrix**: Describes node characteristics.
- **Labels**: Used for supervised training and evaluation.

The server performs training (or inference) based on this input and outputs learned node embeddings and predictions.

## Cloud Storage (Optional)

For users requiring cloud storage, the server supports uploading processed files or images to Azure Blob Storage or AWS S3. Make sure to configure your cloud credentials in the `.env` file.

## Results and Visualizations

The server generates the following outputs:

- **Training Loss**: Displays a plot of the loss over time during training.
- **Accuracy**: Tracks classification accuracy during model evaluation.
- **Node Embeddings**: The GCN's learned representations for each node in the graph.
- **Classification Results**: A JSON file containing the classification of nodes based on input labels.

## References

- [GCN Paper: Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)

---
