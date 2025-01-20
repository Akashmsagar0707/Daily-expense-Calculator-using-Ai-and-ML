import pandas as pd
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from expenses.models import Expense



import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

# Now you can import the models
from expenses.models import Expense
def get_expenses_data():
    expenses = Expense.objects.all()
    if not expenses.exists():
        print("No expenses found in the database.")  # Debug for empty database
        return pd.DataFrame(columns=["Amount", "Category", "Date"])

    data = {
        "Amount": [expense.amount for expense in expenses],
        "Category": [expense.category for expense in expenses],
        "Date": [expense.date for expense in expenses],
    }
    return pd.DataFrame(data)

def expense_trend_analysis():
    # Fetch the data
    df = get_expenses_data()

    # Convert the 'Date' column to datetime for easier manipulation
    df['Date'] = pd.to_datetime(df['Date'])

    # Group by month and sum up the amounts to see monthly trends
    df['Month'] = df['Date'].dt.month
    monthly_expenses = df.groupby('Month')['Amount'].sum()

    # Plotting the monthly expenses
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_expenses.index, monthly_expenses.values, marker='o', color='b')
    plt.title('Monthly Expense Trends')
    plt.xlabel('Month')
    plt.ylabel('Total Expenses')
    plt.grid(True)
    plt.show()

def category_spending_analysis():
    # Fetch data
    expenses = Expense.objects.all()
    if not expenses.exists():
        print("No data available for analysis.")  # Debug empty data
        return

    # Create DataFrame
    data = {
        'Category': [expense.category for expense in expenses],
        'Amount': [float(expense.amount) for expense in expenses],  # Ensure numeric type
    }
    df = pd.DataFrame(data)

    # Group by category and sum amounts
    category_expenses = df.groupby('Category')['Amount'].sum()

    if category_expenses.empty:
        print("No numeric data available for plotting.")  # Debug empty data
        return

    # Plot data------------------------------------------
    
    category_expenses.plot(kind='bar', color='g')
    plt.title("Category Spending Analysis")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.show()



from sklearn.preprocessing import LabelEncoder
import numpy as np
def clustering_expenses():
    # Fetch the data
    df = get_expenses_data()

    if df.empty:
        print("No expenses to cluster.")
        return

    # Convert categories to numerical values
    le = LabelEncoder()
    df['CategoryEncoded'] = le.fit_transform(df['Category'])

    # Prepare data for clustering
    X = df[['Amount', 'CategoryEncoded']].values

    # Determine optimal clusters using the elbow method
    distortions = []
    K = range(1, 10)
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        distortions.append(kmeans.inertia_)

    # Plot elbow curve
    plt.figure(figsize=(8, 4))
    plt.plot(K, distortions, 'bo-', color='orange')
    plt.title('Elbow Method for Optimal Clusters')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Distortion')
    plt.grid()
    plt.show()

    # Apply KMeans with optimal clusters
    optimal_clusters = 3  # Example; choose dynamically based on the elbow curve
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)

    # Show clustered data
    print(df[['Amount', 'Category', 'Cluster']])

from django.shortcuts import render
import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def plot_expense_trends(request):
    # Call the expense trend analysis function
    expense_trend_analysis()  # Generates a matplotlib plot
    buf = io.BytesIO()
    plt.savefig(buf, format='png')  # Save the plot as an image
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')  # Return as HTTP response

def plot_clustering_expenses(request):
    # Call the clustering function
    clustering_expenses()  # Generates an elbow curve
    buf = io.BytesIO()
    plt.savefig(buf, format='png')  # Save the elbow curve plot as an image
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')



if __name__ == "__main__":
    # Uncomment one of the following functions to see the result
    expense_trend_analysis()
    category_spending_analysis()
    clustering_expenses()
