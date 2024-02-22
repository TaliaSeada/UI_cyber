# Use the official Python image as base
FROM python:3.9.13

RUN pip install --upgrade pip
# Set the working directory in the container
WORKDIR /docker-flask

# Copy the current directory contents into the container at /docker-flask
# COPY ./app.py .
# COPY ./model.pkl .
# COPY ./selected_features.pkl .
# COPY ./selector.pkl .
# COPY ./vectorizer.pkl .
# COPY ./static/script.js ./static/script.js 
# COPY ./static/styles.css ./static/styles.css
# COPY ./templates/index.html ./templates/index.html

ADD . /docker-flask

# Install dependencies
# RUN pip install --no-cache-dir flask scikit-learn pandas xgboost
RUN pip install flask scikit-learn pandas xgboost
# RUN pip install -r requirements.txt

# Expose the port the app runs on
# EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
