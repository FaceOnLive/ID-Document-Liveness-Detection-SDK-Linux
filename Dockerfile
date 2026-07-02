FROM ubuntu:22.04
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt-get update && \
    apt-get install -y binutils python3 python3-pip python3-opencv && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app
COPY --chown=user . .
COPY --chown=user ./dependency/* /usr/lib

RUN pip3 install -r requirements.txt
RUN chmod a+x run.sh
CMD (cd /app && exec python3 app.py & sleep 10 && exec python3 demo.py)
EXPOSE 9000 7860

ENTRYPOINT ["./run.sh"]
