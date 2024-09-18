FROM python:3.11

WORKDIR /app

ENV PYTHOPATH=/app

COPY ./pyproject.toml /pyproject.toml 

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry lock && \
    bash -c "\
    if [ $INSTALL_DEV == 'true' ] ; \
    then poetry install --no-root ; \
    else poetry install --no-root --no-dev ; \
    fi " 


COPY . .

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
