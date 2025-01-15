FROM python:3.9-alpine3.13

LABEL maintainer="learning-rest"

ENV PYTHONBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./profile_project /profile_project
COPY ./scripts /scripts
WORKDIR /profile_project
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        subhra-user && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER subhra-user

CMD ["run.sh"]