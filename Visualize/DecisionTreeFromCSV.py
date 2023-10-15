import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Load your data into a DataFrame
data = pd.read_csv('data.csv', delimiter='|')

# Probably could do it with Pandas, but I was too lazy lol
with open("data.csv", "r") as objFile:
	arrFirstLine = objFile.read().split("\n")[0].split("|")
	

#   Sanitize:

# Encode categorical variables, such as 'strName'
#label_encoder = LabelEncoder()
#data['strName'] = label_encoder.fit_transform(data['strName'])
#data['strPageID'] = label_encoder.fit_transform(data['strPageID'])
#data['strDescription'] = label_encoder.fit_transform(data['strDescription'])

# Extract day, month, and year from the date string
#data['strUpdateTime'] = pd.to_datetime(data['strUpdateTime'])
#data['update_day'] = data['strUpdateTime'].dt.day
#data['update_month'] = data['strUpdateTime'].dt.month
#data['update_year'] = data['strUpdateTime'].dt.year

arrBadColumns = ["strName","strDescription", "strPageID", "strUpdateTime"]
#data = data.drop(arrBadColumns)
for strBadColumn in arrBadColumns:
	del data[strBadColumn]
	arrFirstLine.remove(strBadColumn)

# Define features and target


arrCopyFirstLine = arrFirstLine
for strTargetFeature in arrCopyFirstLine: 
	try:

		arrFirstLine.remove(strTargetFeature)
		X = data[arrFirstLine]
		y = data[strTargetFeature]

		# Split data into training and testing sets
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

		# Create a decision tree classifier
		clf = DecisionTreeClassifier(random_state=42)

		# Train the model
		clf.fit(X_train, y_train)

		# Evaluate the model on the testing set
		accuracy = clf.score(X_test, y_test)
		print(strTargetFeature, f"Accuracy: {accuracy}")


		plt.figure(figsize=(20, 12))
		DecisionTreeClassifier(clf, filled=True, feature_names=X.columns, class_names=['Class 0', 'Class 1'])
		plt.title(f'Decision Tree Visualization ("{strTargetFeature}", accuracy: {accuracy})')
		plt.savefig(f"DecisionTree_{strTargetFeature}.jpg", dpi=600)
    #plt.show()
		plt.close()
	except Exception as ex:
		print(strTargetFeature, "\n\n\n", ex)
	
