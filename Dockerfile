FROM python:3.10-bookworm

WORKDIR /workspace/src

RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["sleep", "infinity"]