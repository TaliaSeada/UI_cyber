# Use the official Python image as base
FROM python:3.9.13

RUN pip install --upgrade pip
# Set the working directory in the container
WORKDIR /docker-flask

ADD . /docker-flask

# Install dependenc
RUN pip install flask scikit-learn pandas xgboost
# RUN pip install -r requirements.txt

# Command to run the application
CMD ["python", "app.py"]

# TODO run this:
# docker build -t powershell-detector .
# docker run -d -p 5000:5000 powershell-detector