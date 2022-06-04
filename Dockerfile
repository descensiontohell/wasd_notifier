FROM python:3.9-slim
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir wasd
WORKDIR /wasd

COPY . .
ENV IS_IN_DOCKER Yes
ENTRYPOINT ["/wasd/entrypoint.sh"]