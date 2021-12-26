FROM python:3.7-slim-buster as builder

RUN pip3 install PyGithub

COPY issue_replicator.py /

CMD python /issue_replicator.py
