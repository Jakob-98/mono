#%%
import gzip
import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter
from tqdm import tqdm
from sklearn.metrics import confusion_matrix

from sklearn.datasets import fetch_openml

# Download the MNIST data
mnist = fetch_openml('mnist_784')

# Split data into training and test sets
X = mnist.data.astype('float32')
y = mnist.target.astype('int64')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#%%

# Create training set with 20 samples for each label
training_set_df = X_train.copy()
training_set_df['label'] = y_train
training_set = []

for label in y_train.unique():
    samples_for_label = training_set_df[training_set_df['label'] == label].head(20)
    samples_tuples = [(row.drop('label').values, row['label']) for index, row in samples_for_label.iterrows()]
    training_set.extend(samples_tuples)

# Create test set
test_set_df = X_test.copy()
test_set_df['label'] = y_test
test_set = [(row.drop('label').values, row['label']) for index, row in test_set_df.iterrows()]


#%%
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

# Calculate and display accuracy
accuracy = correct_predictions / len(test_set[:100])
print(f"Accuracy: {accuracy * 100:.2f}%")

# Generate the confusion matrix
cm = confusion_matrix(actual_labels, predicted_labels)
print("Confusion Matrix:")
print(cm)
# %%

import cv2  # For image compression
import numpy as np
from collections import Counter

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Convert dataframes to numpy arrays
# X_train_np = X_train.to_numpy()
# X_test_np = X_test.to_numpy()
# y_train_np = y_train.to_numpy()
# y_test_np = y_test.to_numpy()

# # Create training_set and test_set
# training_set = list(zip(X_train_np, y_train_np))
# test_set = list(zip(X_test_np, y_test_np))

def compress_image(image):
    # Use high JPEG compression
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]  # Quality from 0 to 100; lower means higher compression
    _, img_encoded = cv2.imencode('.jpg', image, encode_param)
    return img_encoded

# Create compressed training set with original size and compressed size
compressed_training_set = [(len(img.tobytes()), len(compress_image(img)), label) for img, label in training_set]

correct_predictions = 0
actual_labels = []
predicted_labels = []

# Prediction
for test_img, actual_label in tqdm(test_set):
    original_size_test = len(test_img.tobytes())
    compressed_size_test = len(compress_image(test_img))
    compression_diff_test = original_size_test - compressed_size_test
    
    distances = []
    for original_size, compressed_size, label in compressed_training_set:
        compression_diff_train = original_size - compressed_size
        distance = abs(compression_diff_train - compression_diff_test)
        distances.append((distance, label))
        
    sorted_distances = sorted(distances, key=lambda x: x[0])
    k = 5  # Number of neighbors to consider
    top_k_class = [label for _, label in sorted_distances[:k]]
    predicted_class = Counter(top_k_class).most_common(1)[0][0]
    
    if predicted_class == actual_label:
        correct_predictions += 1
    actual_labels.append(actual_label)
    predicted_labels.append(predicted_class)


# Calculate accuracy
accuracy = correct_predictions / len(test_set)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Generate the confusion matrix
cm = confusion_matrix(actual_labels, predicted_labels)
print("Confusion Matrix:")
print(cm)

# %%
