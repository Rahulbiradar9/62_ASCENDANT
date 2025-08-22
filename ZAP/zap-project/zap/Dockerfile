FROM owasp/zap2docker-stable:2.14.0

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    apt-get clean

COPY policies/ /home/zap/policies/

USER zap

WORKDIR /home/zap

CMD ["zap.sh", "-daemon", "-host", "0.0.0.0", "-port", "8080", "-config", "api.disablekey=true"]