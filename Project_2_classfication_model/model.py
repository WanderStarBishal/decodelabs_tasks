import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
 
df = pd.read_csv("Iris.csv")
 

if "Id" in df.columns:
    df = df.drop(columns=["Id"])
 
print("=" * 60)
print("STEP 1: Understanding the dataset")
print("=" * 60)
print(f"\nShape of dataset: {df.shape}  (rows, columns)")
print(f"\nColumns: {list(df.columns)}")
 
print("\nFirst 5 rows:")
print(df.head())
 
print("\nClass distribution (how many samples per species):")
print(df["Species"].value_counts())
 
print("\nBasic statistics per feature:")
print(df.describe())
 

X = df.drop(columns=["Species"]).values
y_labels = df["Species"].values    
 

encoder = LabelEncoder()
y = encoder.fit_transform(y_labels)
 

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
 
print("\n" + "=" * 60)
print("STEP 2: Splitting the data")
print("=" * 60)
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples:  {X_test.shape[0]}")
 

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
 

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_scaled, y_train)
 
predictions = model.predict(X_test_scaled)
 
print("\n" + "=" * 60)
print("STEP 3: Training and evaluating the model (KNN, k=5)")
print("=" * 60)
 
accuracy = accuracy_score(y_test, predictions)
print(f"\nAccuracy on test set: {accuracy:.2%}")
 
print("\nConfusion matrix (rows=actual, columns=predicted):")
print(confusion_matrix(y_test, predictions))
 
print("\nDetailed classification report:")
print(classification_report(y_test, predictions, target_names=encoder.classes_))
 


sample = [[5.1, 3.5, 1.4, 0.2]]
sample_scaled = scaler.transform(sample)
predicted_class = model.predict(sample_scaled)[0]
 
print("\n" + "=" * 60)
print("BONUS: Predicting a new sample")
print("=" * 60)
print(f"Measurements: {sample[0]}")
print(f"Predicted species: {encoder.classes_[predicted_class]}")