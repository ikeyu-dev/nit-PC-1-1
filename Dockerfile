FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip install -r /code/requirements.txt

COPY ./src /code/src

CMD ["uvicorn", "src.api.main:app", "--reload",  "--host", "0.0.0.0", "--port", "5001"]
