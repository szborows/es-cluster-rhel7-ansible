FROM elasticsearch:2.3
MAINTAINER slawomir.zborowski@nokia.com

ARG proxy_host
ARG proxy_port
RUN ./bin/plugin install -DproxyPort=$proxy_port -DproxyHost=$proxy_host mobz/elasticsearch-head
