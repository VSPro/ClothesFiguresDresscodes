FROM postgres:11

LABEL "Product"="PostgreSQL 11 with SSL enabled"

COPY create_db.sh /docker-entrypoint-initdb.d/create_db.sh

RUN chown postgres docker-entrypoint-initdb.d/create_db.sh && \
    chmod 0755 docker-entrypoint-initdb.d/create_db.sh
