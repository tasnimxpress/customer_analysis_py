import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from io import StringIO

def perform_logistic_regression(file_path,  results_csv_path):
    try:
        # Load the data
        df = pd.read_excel(file_path, sheet_name='EncodedData')
        
        # Check the data
        print("Data loaded successfully")
        
        # Assuming the last column is the target variable
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Create and train the model
        model = LogisticRegression(max_iter=10000)
        model.fit(X_train, y_train)

        # Predict and evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        summary = classification_report(y_test, y_pred)
        coefficients = model.coef_[0]
                # Convert the summary report to a string
        summary_io = StringIO()
        summary_io.write(summary)
        summary_text = summary_io.getvalue()

        # Prepare results
        results = {
            'Metric': ['Accuracy', 'Coefficients', 'Summary'],
            'Value': [accuracy, coefficients.tolist(), summary_text]
        }

        results_df = pd.DataFrame(results)
        
        # Save the data and results to CSV files
        results_df.to_csv(results_csv_path, index=False)  # Save results
        
        print(f"results saved to '{results_csv_path}'.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file_path = r"D:\Nadeem\excel macro project\123.xltm"  # Use .xlsx for testing
    results_csv_path = r"D:\Nadeem\excel macro project\logistic_regression_results.csv"  # New file for results
    perform_logistic_regression(input_file_path, results_csv_path)
