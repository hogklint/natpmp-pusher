# docker build . gitea.mnx.se/hogklint/pusher:0.1.0
FROM python:3.11.5-alpine3.18 as build

ENV PYTHONPATH ${PYTHONPATH}:/pusher/lib/python3.11/site-packages
COPY . /tmp/pusher/
RUN python3 -O -m pip install /tmp/pusher --prefix=/pusher

FROM python:3.11.5-alpine3.18 as runtime

COPY --from=build /pusher /pusher
ENV PYTHONPATH ${PYTHONPATH}:/pusher/lib/python3.11/site-packages
RUN apk add --no-cache git

ENTRYPOINT ["/pusher/bin/pusher"]
