# Elasticsearch

使用场景：Elasticsearch 搜索引擎搭建

## 单节点部署

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

## 多节点伪集群部署

```yaml
version: '3.9'
services:
  elasticsearch01:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.2
    container_name: elasticsearch01
    privileged: true
    environment:
      # 节点名称
      - node.name=elasticsearch01
      # 集群名称
      - cluster.name=elasticsearch
      #指定主机名称
      - discovery.seed_hosts=elasticsearch02,elasticsearch03
      # 从哪里选举主节点
      - cluster.initial_master_nodes=elasticsearch01,elasticsearch02,elasticsearch03
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
      - ./data/elasticsearch01/plugins:/usr/share/elasticsearch/plugins
      - ./data/elasticsearch01/data:/usr/share/elasticsearch/data:rw
      - ./data/elasticsearch01/logs:/user/share/elasticsearch/logs:rw
    ports:
      - 9201:9200
      - 9301:9300
    networks:
      - elastic-network
  elasticsearch02:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.2
    container_name: elasticsearch02
    privileged: true
    environment:
      - node.name=elasticsearch02
      - cluster.name=elasticsearch
      - discovery.seed_hosts=elasticsearch01,elasticsearch03
      - cluster.initial_master_nodes=elasticsearch01,elasticsearch02,elasticsearch03
      - bootstrap.memory_lock=true
      - xpack.security.enabled=false
      - xpack.security.transport.ssl.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - ./data/elasticsearch02/plugins:/usr/share/elasticsearch/plugins
      - ./data/elasticsearch02/data:/usr/share/elasticsearch/data:rw
      - ./data/elasticsearch02/logs:/user/share/elasticsearch/logs:rw
    ports:
      - 9202:9200
      - 9302:9300
    networks:
      - elastic-network
  elasticsearch03:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.2
    container_name: elasticsearch03
    privileged: true
    environment:
      - node.name=elasticsearch03
      - cluster.name=elasticsearch
      - discovery.seed_hosts=elasticsearch01,elasticsearch03
      - cluster.initial_master_nodes=elasticsearch01,elasticsearch02,elasticsearch03
      - bootstrap.memory_lock=true
      - xpack.security.enabled=false
      - xpack.security.transport.ssl.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - ./data/elasticsearch03/plugins:/usr/share/elasticsearch/plugins
      - ./data/elasticsearch03/data:/usr/share/elasticsearch/data:rw
      - ./data/elasticsearch03/logs:/user/share/elasticsearch/logs:rw
    ports:
      - 9203:9200
      - 9303:9300
    networks:
      - elastic-network

networks:
  elastic-network:
    driver: bridge
```