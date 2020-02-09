FROM python:3.7-alpine

ARG APK_OPTIONS="--no-cache"
ARG FLASK_ENV=production
ARG FLASK_APP=portalbackend
ARG FLASK_PORT=5000

ENV FLASK_ENV=${FLASK_ENV}
ENV FLASK_APP=${FLASK_APP}
ENV FLASK_APP_MODULE=${FLASK_APP}:app
ENV FLASK_PORT=${FLASK_PORT}

# install required system-wide dependencies
RUN apk update ${APK_OPTIONS} && \
    apk add ${APK_OPTIONS} build-base gcc python-dev libffi-dev && \
    apk add ${APK_OPTIONS} postgresql-dev postgresql-client curl

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && \
    set -ex && \
    pipenv install --deploy --system

COPY . .

# //TODO this is probably should be changed
RUN chmod a+rwx -R .

# Run container as non-root user
RUN addgroup -g 6000 ${FLASK_APP} && \
    adduser -D -u 6000 -G ${FLASK_APP} ${FLASK_APP}
USER ${FLASK_APP}

EXPOSE 5000
CMD ["/usr/src/app/docker-entrypoint.sh"]
