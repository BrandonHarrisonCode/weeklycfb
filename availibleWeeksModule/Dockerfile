FROM python:3.7-buster
RUN pip install pytest
ADD requirements.txt /app/
RUN pip install -r app/requirements.txt
ADD *.py /app/
CMD [ "python", "-m", "pytest", "app/", "--full-trace"]
