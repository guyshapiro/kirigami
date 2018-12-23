From python:3

WORKDIR /usr/src/app

copy . .

RUN pip install --no-cache-dir -e .

CMD ["kirigami"]
