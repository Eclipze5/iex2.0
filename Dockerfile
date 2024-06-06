# Use an official lightweight Python image.
FROM python:3.11-slim
#FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to specify where the Flask application is
ENV FLASK_APP=flaskr:create_app
ENV FLASK_ENV=development
ENV SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:@localhost/iex
ENV SECRET_KEY=dev
ENV PER_PAGE=12

# Run the application
CMD ["flask", "--app", "flaskr", "run"]


# docker build -t iex .
# docker run --name deployment -p 4000:5000 iex
# docker stop deployment
# docker rm deployment