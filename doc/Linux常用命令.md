# Linux 常用命令

#### Linux关机，重启
```shell
# 关机 
shutdown -h now

# 重启
shutdown -r now
```

#### 查看系统，CPU信息
```shell
# 查看系统内核信息
uname -a

# 查看系统内核版本
cat /proc/version

# 查看当前用户环境变量
env

cat /proc/cpuinfo

# 查看有几个逻辑cpu, 包括cpu型号
cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c

# 查看有几颗cpu,每颗分别是几核
cat /proc/cpuinfo | grep physical | uniq -c

# 查看当前CPU运行在32bit还是64bit模式下, 如果是运行在32bit下也不代表CPU不支持64bit
getconf LONG_BIT

# 结果大于0, 说明支持64bit计算. lm指long mode, 支持lm则是64bit
cat /proc/cpuinfo | grep flags | grep ' lm ' | wc -l
```

#### 建立软连接
```shell
ln -s /usr/local/jdk1.8/ jdk
```

#### rpm相关
```shell
# 查看是否通过rpm安装了该软件
rpm -qa | grep 软件名
```

#### sshkey
```shell
# 创建sshkey
ssh-keygen -t rsa -C your_email@example.com

#id_rsa.pub 的内容拷贝到要控制的服务器的 home/username/.ssh/authorized_keys 中,如果没有则新建(.ssh权限为700, authorized_keys权限为600)
```

#### 命令重命名
```shell
# 在各个用户的.bash_profile中添加重命名配置
alias ll='ls -alF'
```

#### 同步服务器时间
```shell
sudo ntpdate -u ntp.api.bz
```

#### 后台运行命令
```shell
# 后台运行,并且有nohup.out输出
nohup xxx &

# 后台运行, 不输出任何日志
nohup xxx > /dev/null &

# 后台运行, 并将错误信息做标准输出到日志中 
nohup xxx >out.log 2>&1 &
```