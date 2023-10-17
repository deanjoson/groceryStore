# MySQL Server

使用场景：MySQL 数据库搭建

参数说明：

- MYSQL_ROOT_PASSWORD ： ROOT用户密码
- character-set-server ： 服务端字符集
- collation-server ：服务端字符排序规则
- lower_case_table_names : 大小写敏感配置
- max_allowed_packet ： 数据包大小（过小会导致insert/update失败）
- mem_limit ： 内存限制

```yaml
version: '3'
services:
  mysql:
    image: mysql:5.7.28
    container_name: mysql
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - TZ=Asia/Shanghai
    command:
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_general_ci
      --lower_case_table_names=1
      --max_allowed_packet=128M
    restart: always
    ports:
      - 3306:3306
    volumes:
      - ./data:/var/lib/mysql
    mem_limit: 1g
    networks:
      - mysql-network
networks:
  mysql-network:
    driver: bridge
```
