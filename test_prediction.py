from utils.prediction import (
    get_model,
    get_features,
    get_label_encoders,
)

print("Model:")
print(get_model())

print("\nFeatures:")
print(get_features())

print("\nEncoders:")
print(get_label_encoders().keys())