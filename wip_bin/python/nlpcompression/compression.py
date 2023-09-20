import gzip
from nltk.corpus import reuters
from sklearn.model_selection import train_test_split

# Get the list of file IDs and their corresponding categories (labels)
file_ids = reuters.fileids()
categories = [reuters.categories(file_id) for file_id in file_ids]

# Consider only the first category for each file (for simplicity)
single_categories = [cat[0] for cat in categories]

# Get the raw text data
text_data = [reuters.raw(file_id) for file_id in file_ids]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(text_data, single_categories, test_size=0.2, random_state=42)

# Zip them into tuples like (text, label)
training_set = list(zip(X_train, y_train))
test_set = list(zip(X_test, y_test))

# k = 5

import numpy as np

# for (x1, _) in test_set:
#     Cx1 = len(gzip.compress(x1.encode()))
#     distance_from_x1 = []
#     for (x2, _) in training_set:
#         Cx2 = gzip.compress(x2.encode())
#         x1x2 = "".join([x1, x2])
#         Cx1x2 = gzip.compress(x1x2. encode())
#         ncd = (Cx1x2 - min(Cx1,Cx2)) / max( Cx1 , Cx2)
#         distance_from_x1.append(ncd)
#         sorted_idx = np.argsort(np.array(distance_from_x1))
#         top_k_class = training_set[sorted_idx [:k], 1]
#         predict_class = max(set(top_k_class), key=top_k_class.count)
#         print(f"Predicted class: {predict_class}")

correct_predictions = 0  # Counter for correct predictions
total_samples = len(test_set)  # Total number of samples in the test set

k = 5  # You can set this to any integer value, doesn't need to be the number of unique labels

for (x1, actual_label) in test_set:
    Cx1 = len(gzip.compress(x1.encode()))
    distance_from_x1 = []
    
    for (x2, label) in training_set:
        Cx2 = len(gzip.compress(x2.encode()))
        x1x2 = "".join([x1, x2])
        Cx1x2 = len(gzip.compress(x1x2.encode()))
        
        ncd = (Cx1x2 - min(Cx1, Cx2)) / max(Cx1, Cx2)
        print(ncd, label)
        distance_from_x1.append((Cx1x2, x1x2))

    # Sort and take top k
    sorted_distances = sorted(distance_from_x1, key=lambda x: x[0])
    top_k_class = [label for _, label in sorted_distances[:k]]

    # Predict the class based on majority vote
    predict_class = max(set(top_k_class), key=top_k_class.count)
    
    # Check if the prediction is correct
    if predict_class == actual_label:
        correct_predictions += 1

    print(f"Predicted class: {predict_class}, Actual class: {actual_label}")

# Calculate accuracy
accuracy = correct_predictions / total_samples
print(f"Accuracy: {accuracy * 100:.2f}%")
