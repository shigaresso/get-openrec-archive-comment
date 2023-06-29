FROM python:3.11.4-slim

COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt
