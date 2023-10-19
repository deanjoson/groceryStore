# Elasticsearch

使用场景：Elasticsearch 搜索引擎搭建

```yaml
version: '3.9'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.2
    container_name: elasticsearch
    privileged: true
    environment:
      # 节点名称
      - node.name=elasticsearch
      # 单节点运行
      - discovery.type=single-node
      # 是否锁住内存，避免交换(swapped)带来的性能损失
      - bootstrap.memory_lock=true
      # 关闭安全校验，避免连接时返回警告信息
      - xpack.security.enabled=false
      - xpack.security.transport.ssl.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - ./data/plugins:/usr/share/elasticsearch/plugins
      - ./data/data:/usr/share/elasticsearch/data:rw
      - ./data/logs:/user/share/elasticsearch/logs:rw
    ports:
      - 9200:9200
      - 9300:9300
    networks:
      - elastic-network
networks:
  elastic-network:
    driver: bridge
```