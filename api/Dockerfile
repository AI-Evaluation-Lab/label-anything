# Use the official Python image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

RUN mkdir models
RUN wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -P models/

# Install any dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the Flask app code to the container
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py", "--reset"]

