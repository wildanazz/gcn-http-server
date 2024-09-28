# Multi-layer GCN on Facebook Large Page-Page Network Dataset (Multi-Class Node Classification)

## Introduction to GCN
A Multi-layer Graph Convolutional Network (GCNs) is a neural network architecture designed for graph-structured data, where nodes represent entities and edges denote relationships between them. GCNs can be utilized for various tasks, including node classification, link prediction, and clustering. The main purpose of this GCNs model is to accurately assign one of several predefined labels to each node in a graph based on its features and the relationships it has with other nodes.
#### Architecture Overview:
- Input Layer: Accepts node features and the adjacency matrix.
- Hidden Layers: Each layer performs a graph convolution operation, aggregating information from neighboring nodes. The number of hidden layers can be adjusted based on task complexity.
- Output Layer: This layer outputs label predictions for each node.
#### Implementation Steps:
1. Create an N x N adjacency matrix (where N is the number of nodes).
2. Create an N x D feature matrix (where D is the number of features).
3. Normalize both the adjacency and feature matrices.
4. Construct a two-layer Graph Convolutional Network model.
5. Train and test the model on the dataset.

## Dependencies:
- Python
- Numpy
- Pytorch
- Matplotlib
- Sklearn
- Scipy
- Pandas

## Notes:
- .env: Contains storage key and secret.

## Installation
To set up this project locally, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/wildanazz/wildanazz.com.git
2. Create a virtual environment:
   ```bash
   python -m venv .venv   
3. Activate the virtual environment:
   ```bash
   .\.venv\Scripts\activate
4. Run the server:
   ```bash
   python .\server.py

## Sending requests:
1. To send a request, use cURL:
   ```bash
   curl --location 'http://localhost:5000' --form 'data=@"/location/to/data/facebook.npz"'

## Results:
#### Loss Plot
![GCN](./data/Loss.png)
#### Training Plot
![GCN](./data/Accuracy.png)
#### Node embeddings
![GCN](./data/Embedding.png)

## References:
[1] https://arxiv.org/abs/1609.02907
