# -*- coding: utf-8 -*-
"""Progres3.2.3(use this).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ykjkDZs0an_77wH48V4ECyQjVaX9oPM4
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/MyDrive/Processed/Processed3/cleaned_output_addcolumns_final_merged_cleaned_questions.csv'
df_clean = pd.read_csv(file_path, header = 0)
df_clean = df_clean.dropna()
print(df_clean.shape)
print(list(df_clean.columns))

df_clean.head()

df_clean['answered?'].value_counts()

df_clean.describe()

sns.set_style("whitegrid")
plot = sns.countplot(x='answered?', data=df_clean, palette='hls')

plot.set_xlabel('Answered Status', fontsize=12)
plot.set_ylabel('Count', fontsize=12)

plot.set_xticklabels(['Unanswered (0)', 'Answered (1)'])

plot.set_title('Distribution of Answered Questions', fontsize=15)

for p in plot.patches:
    plot.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                  ha='center', va='baseline', fontsize=11, color='black', xytext=(0, 5),
                  textcoords='offset points')
plt.show()

plt.savefig('count_plot.png')

count_no_sub = len(df_clean[df_clean['answered?']==0])
count_sub = len(df_clean[df_clean['answered?']==1])
pct_of_no_sub = count_no_sub/(count_no_sub+count_sub)
print("percentage of non-answered: ", pct_of_no_sub*100)
pct_of_sub = count_sub/(count_no_sub+count_sub)
print("percentage of answered: ", pct_of_sub*100)

numeric_cols = df_clean.select_dtypes(include=['number']).columns

df_mean = df_clean.groupby('answered?')[numeric_cols].mean()
print(df_mean)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

sns.set_style("whitegrid")

table_x1 = pd.crosstab(df_clean['code_snippet'], df_clean['answered?'])

ax = table_x1.plot(kind='bar', figsize=(10, 6), color=['skyblue', 'salmon'])

plt.title('Answer Distribution Based on Code Snippet', fontsize=16)
plt.xlabel('Code Snippet', fontsize=12)
plt.ylabel('Frequency of Answers', fontsize=12)

ax.set_xticklabels(['No Code Snippet (0)', 'Has Code Snippet (1)'], rotation=0)

plt.legend(title='Answered?', labels=['No', 'Yes'], fontsize=12, title_fontsize=12)

for container in ax.containers:
    ax.bar_label(container, fmt='%d', label_type='edge', fontsize=10, padding=3)

plt.tight_layout()

plt.savefig('answer_distribution_based_on_code_snippet.png', dpi=300)

plt.show()

sns.set_style("whitegrid")

table_x2 = pd.crosstab(df_clean['image'], df_clean['answered?'])

ax = table_x2.plot(kind='bar', figsize=(10, 6), color=['lightcoral', 'lightseagreen'])

plt.title('Answer Distribution Based on Image', fontsize=16)
plt.xlabel('Image', fontsize=12)
plt.ylabel('Frequency of Answers', fontsize=12)

ax.set_xticklabels(['No Image (0)', 'Has Image (1)'], rotation=0)

plt.legend(title='Answered?', labels=['No', 'Yes'], fontsize=12, title_fontsize=12)

for container in ax.containers:
    ax.bar_label(container, fmt='%d', label_type='edge', fontsize=10, padding=3)

plt.tight_layout()

plt.savefig('answer_distribution_based_on_image.png', dpi=300)

plt.show()

df_clean['log_Reputation'] = np.log1p(df_clean['Reputation'])  # log(1 + Reputation) untuk menghindari log(0)
df_clean['sqrt_question_line_count'] = np.sqrt(df_clean['question_line_count'])
df_clean['sqrt_code_line_count'] = np.sqrt(df_clean['code_line_count'])

q99 = df_clean['log_Reputation'].quantile(0.99)
df_subset = df_clean[df_clean['log_Reputation'] <= q99]

sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

sns.boxplot(x='answered?', y='log_Reputation', data=df_subset, palette='Blues')

plt.legend([], [], frameon=False)

plt.title('Logarithmic Reputation Distribution Based on Answered Status', fontsize=16)
plt.xlabel('Answered Status (0 = Unanswered, 1 = Answered)', fontsize=12)
plt.ylabel('Log(Reputation)', fontsize=12)

median_log_reputation = df_subset['log_Reputation'].median()
plt.axhline(median_log_reputation, color='red', linestyle='--', label='Median Log(Reputation)')

plt.text(0.5, median_log_reputation + 0.1, f'Median: {median_log_reputation:.2f}', color='red', fontsize=12, ha='center')

plt.xticks([0, 1], ['Unanswered (0)', 'Answered (1)'])

plt.savefig('answer_distribution_based_on_log_reputation.png', dpi=300)

plt.show()

plt.title('Reputation Distribution Plot')
sns.distplot(df_clean['log_Reputation'])
plt.show()

q99 = df_clean['CommentCount'].quantile(0.99)
df_subset = df_clean[df_clean['CommentCount'] <= q99]

sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

sns.boxplot(x='answered?', y='CommentCount', data=df_clean, palette='deep')

plt.legend([], [], frameon=False)

plt.title('Comment Count Distribution Based on Answered Status', fontsize=16)
plt.xlabel('Answered Status (0 = Unanswered, 1 = Answered)', fontsize=12)
plt.ylabel('Number of Comments', fontsize=12)

median_comment_count = df_subset['CommentCount'].median()
plt.axhline(median_comment_count, color='red', linestyle='--', label='Median Comment Count')

plt.text(0.5, median_comment_count + 10, f'Median: {median_comment_count:.0f}', color='red', fontsize=12, ha='center')

plt.xticks([0, 1], ['Unanswered (0)', 'Answered (1)'])

plt.savefig('boxplot_commentcount.png', dpi=300)

plt.show()

plt.title('Comment Count Distribution Plot')
sns.distplot(df_clean['CommentCount'])
plt.show()

q99 = df_clean['ViewCount'].quantile(0.99)
df_subset = df_clean[df_clean['ViewCount'] <= q99]

sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

sns.boxplot(x='answered?', y='ViewCount', data=df_subset, palette='Blues')

plt.legend([], [], frameon=False)

plt.title('View Count Distribution Based on Answered Status', fontsize=16)
plt.xlabel('Answered Status (0 = Unanswered, 1 = Answered)', fontsize=12)
plt.ylabel('Number of Views', fontsize=12)

view_count_median = df_subset['ViewCount'].median()
print(f'Median ViewCount: {view_count_median}')
plt.axhline(view_count_median, color='red', linestyle='--')

plt.text(0.5, view_count_median, f'Median: {view_count_median:.0f}', color='red', ha='center')

plt.xticks([0, 1], ['Unanswered (0)', 'Answered (1)'])

plt.savefig('view_count_distribution_based_on_answered_status.png', dpi=300)

plt.show()

plt.title('View Count Distribution Plot')
sns.distplot(df_clean['ViewCount'])
plt.show()

q99 = df_clean['sqrt_question_line_count'].quantile(0.99)
df_subset = df_clean[df_clean['sqrt_question_line_count'] <= q99]

sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

sns.boxplot(x='answered?', y='sqrt_question_line_count', data=df_subset, palette='Blues')

plt.legend([], [], frameon=False)

plt.title('Question Line Count Distribution Based on Answered Status', fontsize=16)
plt.xlabel('Answered Status (0 = Unanswered, 1 = Answered)', fontsize=12)
plt.ylabel('Number of Question Lines', fontsize=12)

question_line_count_median = df_subset['sqrt_question_line_count'].median()
print(f'Median sqrt_question_line_count: {question_line_count_median}')
plt.axhline(question_line_count_median, color='red', linestyle='--')

plt.text(0.5, question_line_count_median, f'Median: {question_line_count_median:.0f}', color='red', ha='center')

plt.xticks([0, 1], ['Unanswered (0)', 'Answered (1)'])

plt.savefig('question_line_count_distribution_based_on_answered_status.png', dpi=300)

plt.show()

plt.title('Question Count Distribution Plot')
sns.distplot(df_clean['sqrt_question_line_count'])
plt.show()

q99 = df_clean['sqrt_code_line_count'].quantile(0.99)
df_subset = df_clean[df_clean['sqrt_code_line_count'] <= q99]

sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

sns.boxplot(x='answered?', y='sqrt_code_line_count', data=df_subset, palette='Blues')

plt.legend([], [], frameon=False)

plt.title('Code Line Count Distribution Based on Answered Status', fontsize=16)
plt.xlabel('Answered Status (0 = Unanswered, 1 = Answered)', fontsize=12)
plt.ylabel('Number of Code Lines', fontsize=12)

code_line_count_median = df_subset['sqrt_code_line_count'].median()
print(f'Median sqrt_code_line_count: {code_line_count_median}')
plt.axhline(code_line_count_median, color='red', linestyle='--')

plt.text(0.5, code_line_count_median, f'Median: {code_line_count_median:.0f}', color='red', ha='center')

plt.xticks([0, 1], ['Unanswered (0)', 'Answered (1)'])

plt.savefig('code_line_count_distribution_based_on_answered_status.png', dpi=300)

plt.show()

plt.title('Code Count Distribution Plot')
sns.distplot(df_clean['sqrt_code_line_count'])
plt.show()

cat_vars = ['Tags', 'ReputationCategory']

for var in cat_vars:
    cat_list = pd.get_dummies(df_clean[var], prefix=var, sparse=True)
    df_clean = df_clean.join(cat_list)

df_clean = df_clean.drop(columns=cat_vars)

print("Dataset columns after creating dummy variables: \n", df_clean.columns.values)

X = df_clean[['code_snippet', 'image', 'log_Reputation', 'CommentCount', 'ViewCount', 'sqrt_question_line_count', 'sqrt_code_line_count']]
y = df_clean['answered?']

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X.loc[:, ['log_Reputation', 'CommentCount', 'ViewCount', 'sqrt_question_line_count', 'sqrt_code_line_count']] = scaler.fit_transform(
    X[['log_Reputation', 'CommentCount', 'ViewCount', 'sqrt_question_line_count', 'sqrt_code_line_count']]
)

correlation_matrix = X.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Feature Correlation Matrix')
plt.show()

from imblearn.over_sampling import SMOTE
import statsmodels.api as sm

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

X_train = sm.add_constant(X_train)
X_test = sm.add_constant(X_test)

os = SMOTE(random_state=0)
os_data_X, os_data_y = os.fit_resample(X_train, y_train)

os_data_X = pd.DataFrame(data=os_data_X, columns=X.columns)
os_data_y = pd.DataFrame(data=os_data_y, columns=['answered?'])

print("Length of oversampled data is:", len(os_data_X))
print("Number of unanswered questions in oversampled data:", len(os_data_y[os_data_y['answered?'] == 0]))
print("Number of answered questions in oversampled data:", len(os_data_y[os_data_y['answered?'] == 1]))
print("Proportion of unanswered questions in oversampled data is:", len(os_data_y[os_data_y['answered?'] == 0]) / len(os_data_X))
print("Proportion of answered questions in oversampled data is:", len(os_data_y[os_data_y['answered?'] == 1]) / len(os_data_X))

from sklearn.feature_selection import RFE

logreg = LogisticRegression(max_iter=1000)
rfe = RFE(logreg, n_features_to_select=5)
rfe = rfe.fit(X, y)

print("Features selected by RFE: ", X.columns[rfe.support_].tolist())
print("Feature ranking: ", rfe.ranking_)

selected_columns = X.columns[rfe.support_].tolist()
X_selected = X[selected_columns]

print("Columns selected by RFE: ", selected_columns)

import statsmodels.api as sm

logit_model = sm.Logit(y, sm.add_constant(X))
result = logit_model.fit()
print(result.summary2())

odds_ratio = np.exp(result.params)
print("Odds Ratio:\n", odds_ratio)

from sklearn import metrics

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No', 'Yes'], yticklabels=['No', 'Yes'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix Heatmap')
plt.savefig('confusion_matrix_heatmap.png')
plt.show()

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data["feature"] = X_train.columns
vif_data["VIF"] = [variance_inflation_factor(X_train.values, i) for i in range(X_train.shape[1])]
print(vif_data)

from sklearn.metrics import precision_score, recall_score

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(f'Precision: {precision:.2f}')
print(f'Recall: {recall:.2f}')

plt.figure(figsize=(6,6))
plt.scatter(precision, recall, color='green', s=100)
plt.xlim(0,1)
plt.ylim(0,1)
plt.xlabel('Precision')
plt.ylabel('Recall')
plt.title('Precision vs Recall')
plt.grid(True)
plt.text(precision + 0.01, recall, f'P={precision:.2f}, R={recall:.2f}')
plt.savefig('precision_recall_scatter.png')
plt.show()

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:, 1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

new_data = pd.DataFrame({
    'code_snippet': [0],
    'image': [1],
    'log_Reputation': [np.log1p(3000)],
    'CommentCount': [5],
    'ViewCount': [150],
    'sqrt_question_line_count': [np.sqrt(12)],
    'sqrt_code_line_count': [np.sqrt(20)]
})

new_pred_prob = logreg.predict_proba(new_data)[:, 1]
new_pred = [1 if x > 0.5 else 0 for x in new_pred_prob]
print("Prediction Answered?: ", new_pred)