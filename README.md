## SQL 审核 审计 执行 备份 索引优化 ，代码质量管理等。

[更新日志](https://github.com/ss1917/do_mg/releases) 

[在线访问](http://demo.opendevops.cn/)

### 代码质量管理
#### 为什么要使用：
```
糟糕的复杂度分布
  文件、类、方法等，如果复杂度过高将难以改变，这会使得开发人员难以理解它们，
  且如果没有自动化的单元测试，对于程序中的任何组件的改变都将可能导致需要全面的回归测试
重复
 显然程序中包含大量复制粘贴的代码是质量低下的，sonar可以展示源码中重复严重的地方
缺乏单元测试
  sonar可以很方便地统计并展示单元测试覆盖率
没有代码标准
  sonar可以通过PMD,CheckStyle,Findbugs等等代码规则检测工具规范代码编写
没有足够的或者过多的注释
  没有注释将使代码可读性变差，特别是当不可避免地出现人员变动时，程序的可读性将大幅下降
  而过多的注释又会使得开发人员将精力过多地花费在阅读注释上，亦违背初衷
潜在的bug
  sonar可以通过PMD,CheckStyle,Findbugs等等代码规则检测工具检测出潜在的bug
糟糕的设计
  通过sonar可以找出循环，展示包与包、类与类之间的相互依赖关系
  可以检测自定义的架构规则，可以检测单个任务规则的应用情况
  检测耦合
```
#### 简介
**SonarQube 是一个开源的代码分析平台, 用来持续分析和评测项目源代码的质量。 通过SonarQube我们可以检测出项目中重复代码， 潜在bug， 代码风格问题，缺乏单元测试等问题， 并通过一个web ui展示出来**

#### 环境部署

[SonarQube 介绍 部署 配置](https://github.com/opendevops-cn/codo-check/tree/master/doc/sonarqube.md)

#### 脚本部署

- 脚本下载
  ```
  mkdir -p  /opt/ops_scripts/ && cd  /opt/ops_scripts/ && git clone https://github.com/opendevops-cn/codo-check.git
  ```
- 配置 settings
- 安装依赖  pip3 install -r requirements.txt

**约束**
- 当前主机可以执行 /usr/local/sonar-scanner/bin/sonar-scanner 命令。如何部署请看部署文档
- 当前注意可以 拉取 相关git仓库的代码。可以使用git的 deploy_keys

#### 使用说明
**待完善**

### SQL 审核 审计 执行 备份
#### Inception简介：
**Inception是集审核、执行、回滚于一体的一个自动化运维系统，它是根据MySQL代码修改过来的，用它可以很明确的，详细的，准确的审核MySQL的SQL语句，它的工作模式和MySQL完全相同，可以直接使用MySQL客户端来连接，但不需要验证权限，它相对应用程序（上层审核流程系统等）而言，是一个服务器，在连接时需要指定服务器地址及Inception服务器的端口即可，而它相对要审核或执行的语句所对应的线上MySQL服务器来说，是一个客户端，它在内部需要实时的连接数据库服务器来获取所需要的信息，或者直接在在线上执行相应的语句及获取binlog等，Inception就是一个中间性质的服务**
**本项目使用inception 结合CMDB，把SQL审核接入运维自动化平台，方便直接在运维平台使用，拥有审计，审核，执行，备份功能，并且可以结合代码发布使用**

#### 部署 配置
**待完善**

### SQL索引优化
#### 为什么要使用：
```
例行 SQL 优化，不仅可以提升程序性能，还能够降低线上故障的概率。
目前常用的 SQL 优化方式包括但不限于：业务层优化、SQL逻辑优化、索引优化等。其中索引优化通常通过调整索引或新增索引从而达到 SQL 优化的目的。索引优化往往可以在短时间内产生非常巨大的效果。如果能够将索引优化转化成工具化、标准化的流程，减少人工介入的工作量，无疑会大大提高的工作效率。
```

#### SQLAdvisor简介
**SQLAdvisor 是由美团点评公司北京DBA团队开发维护的 SQL 优化工具：输入SQL，输出索引优化建议。 它基于 MySQL 原生词法解析，再结合 SQL 中的 where 条件以及字段选择度、聚合条件、多表 Join 关系等最终输出最优的索引优化建议。目前 SQLAdvisor 在公司内部大量使用，较为成熟、稳定。**

#### 环境部署
[SQLAdvisor 部署 配置](https://github.com/opendevops-cn/codo-check/tree/master/doc/SQLAdvisor.md)

#### 脚本部署

- 脚本下载 如果已经下载，则可以省略当前步骤
  ```
  mkdir -p  /opt/ops_scripts/ && cd  /opt/ops_scripts/ && git clone https://github.com/opendevops-cn/codo-check.git
  ```
- 配置 settings
- 安装依赖  pip3 install -r requirements.txt

**约束**
- 当前主机可以执行 /usr/local/sonar-scanner/bin/sonar-scanner 命令。如何部署请看部署文档
- 当前注意可以 拉取 相关git仓库的代码。可以使用git的 deploy_keys

## License

Everything is [GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html).