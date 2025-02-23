FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install httpx pytest

CMD ["pytest", "test_api.py"]