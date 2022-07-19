FROM python:3.7
RUN wget https://www.secrepo.com/squid/access.log.gz
RUN gzip -d access.log.gz
ADD testingLog.log /
ADD log-analyzer.py /
ENTRYPOINT [ "python3", "./log-analyzer.py" ]
