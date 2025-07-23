FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN python --version
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
