FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./main.py slr.pkl auth.py /app/

EXPOSE 8000

CMD ["python", "main.py"]