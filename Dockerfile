FROM python:alpine3.6

COPY requirements.txt /
COPY slack_delete.py /
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "/slack_delete.py" ]