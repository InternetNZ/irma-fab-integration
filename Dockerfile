FROM python:3.8-slim-buster AS prepare

ENV PYTHONPATH=/app:$PYTHONPATH
ENV PATH=/scripts:$PATH

WORKDIR /app

COPY requirements.txt /app/

# Dependencies
RUN pip install -r requirements.txt

COPY runserver.py /app/
COPY scripts/ /scripts/
COPY fab/ /app/fab
COPY fab_irma.py /app/fab_irma.py

# Dev dependencies
COPY requirements.dev.txt /app/
RUN pip install -r requirements.dev.txt

# Make port 5050 available to the world outside this container
EXPOSE 5050

# Run app.py when the container launches
CMD ["python", "runserver.py"]
