# Use the official Python image as base
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app.py .
COPY ./model.pkl .
COPY ./selected_features.pkl .
COPY ./selector.pkl .
COPY ./vectorizer.pkl .
COPY ./static/script.js ./static/script.js 
COPY ./static/styles.css ./static/styles.css
COPY ./templates/index.html ./templates/index.html

# Install dependencies
RUN pip install --no-cache-dir flask scikit-learn pandas xgboost

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
