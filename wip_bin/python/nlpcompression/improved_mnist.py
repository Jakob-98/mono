import gzip
import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter
from tqdm import tqdm
from sklearn.metrics import confusion_matrix
from sklearn.datasets import fetch_openml

# Fetch and split MNIST data
print("Fetching and splitting MNIST data...")
mnist = fetch_openml('mnist_784')
X, y = mnist.data.astype('float32'), mnist.target.astype('int64')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a training set with 20 samples for each label
print("Creating a training set...")
training_set = []
for label in np.unique(y_train):
    label_data = X_train[y_train == label].head(20)
    samples = [(row.values, label) for _, row in label_data.iterrows()]
    training_set.extend(samples)

# Create a test set
print("Creating a test set...")
test_set_df = X_test.copy()
test_set_df['label'] = y_test
test_set = [(row.drop('label').values, row['label']) for index, row in test_set_df.iterrows()]

# K-NN Classification
print("Classifying test samples...")
k = 5  # Number of neighbors to consider
correct_predictions = 0  # Counter for correct predictions
actual_labels = []
predicted_labels = []

for (x1, actual_label) in tqdm(test_set[:100]):
    Cx1 = len(gzip.compress(x1.tobytes()))
    distance_from_x1 = []
    
    # Compute NCD with each training sample
    for (x2, label) in training_set:
        Cx2 = len(gzip.compress(x2.tobytes()))
        x1x2 = x1 + x2
        Cx1x2 = len(gzip.compress(x1x2.tobytes()))
        
        ncd = (Cx1x2 - min(Cx1, Cx2)) / max(Cx1, Cx2)
        distance_from_x1.append((ncd, label))
    
    # Find k nearest neighbors and predict label
    sorted_distances = sorted(distance_from_x1, key=lambda x: x[0])
    top_k_class = [label for _, label in sorted_distances[:k]]
    predict_class = Counter(top_k_class).most_common(1)[0][0]
    
    # Append the actual and predicted labels for each test sample
    actual_labels.append(actual_label)
    predicted_labels.append(predict_class)
    
    if predict_class == actual_label:
        correct_predictions += 1

# Accuracy and Confusion Matrix
print(f"Accuracy: {correct_predictions / 100 * 100:.2f}%")
print("Generating confusion matrix...")
cm = confusion_matrix(actual_labels, predicted_labels)
print(cm)

