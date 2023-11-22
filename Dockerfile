#
FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /django_rest
COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip
RUN pip install eventlet
RUN pip install --upgrade setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
COPY . /django_rest/
