import gzip

def calculate_ncd(str1, str2):
    C_str1 = len(gzip.compress(str1.encode()))
    C_str2 = len(gzip.compress(str2.encode()))
    C_str1_str2 = len(gzip.compress((str1 + str2).encode()))

    ncd = (C_str1_str2 - min(C_str1, C_str2)) / max(C_str1, C_str2)
    return ncd

def evaluate_answer(ground_truth, generated_answer, threshold=0.3):
    ncd_value = calculate_ncd(ground_truth, generated_answer)

    print(f"NCD between ground truth and generated answer: {ncd_value}")

    if ncd_value < threshold:
        print("The generated answer is considered correct based on the NCD value.")
    else:
        print("The generated answer is considered incorrect based on the NCD value.")

# Example
ground_truth = "The capital of France is Paris."
generated_answer1 = "Paris is the capital of France."
generated_answer2 = "Berlin is the capital of Germany."

# Evaluate the generated answers
evaluate_answer(ground_truth, generated_answer1)  # Should be considered "correct"
evaluate_answer(ground_truth, generated_answer2)  # Should be considered "incorrect"

# Example 2
ground_truth2 = "The Theory of Relativity was formulated by Albert Einstein."
generated_answer2_1 = "Albert Einstein is the scientist behind the Theory of Relativity."
generated_answer2_2 = "Isaac Newton created the Theory of Relativity."

print("Example 2")
evaluate_answer(ground_truth2, generated_answer2_1)
evaluate_answer(ground_truth2, generated_answer2_2)
print("---")

# Example 3
ground_truth3 = "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll pigments."
generated_answer3_1 = "Green plants and some organisms use photosynthesis to create food, thanks to chlorophyll."
generated_answer3_2 = "Osmosis is how plants get their nutrients."

print("Example 3")
evaluate_answer(ground_truth3, generated_answer3_1)
evaluate_answer(ground_truth3, generated_answer3_2)
print("---")