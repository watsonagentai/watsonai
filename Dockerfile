FROM python:3.9-slim
WORKDIR /app

# 1) Create the venv
RUN python -m venv /app/venv

# 2) Copy requirements first
COPY requirements.txt /app/

# 3) Install dependencies inside the venv
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel sherlock-project sherlock
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# 4) Copy the rest of your code
COPY src/ /app/src/
COPY .env /app/

# 5) Let PATH or ENTRYPOINT ensure we use the venv's python
ENV PATH="/app/venv/bin:$PATH"
ENTRYPOINT ["/app/venv/bin/python", "/app/src/main.py"]
