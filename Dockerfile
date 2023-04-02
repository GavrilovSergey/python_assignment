FROM python:3.10

WORKDIR /financial

COPY ./requirements.txt /financial/requirements.txt
COPY ./get_raw_data.py /get_raw_data.py

RUN pip install --no-cache-dir --upgrade -r /financial/requirements.txt

COPY ./financial /financial/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888"]