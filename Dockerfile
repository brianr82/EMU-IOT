FROM python:3.6-slim
RUN mkdir app
WORKDIR app
COPY / /app
RUN mkdir ExperimentResults

RUN apt-get update && apt-get install -y build-essential \
    cmake \
    wget \
    git \
    libgtk2.0-dev \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*

RUN pip install opencv-contrib-python-headless
RUN pip install docker
RUN pip install pandas





ENTRYPOINT ["python3", "main.py"]

