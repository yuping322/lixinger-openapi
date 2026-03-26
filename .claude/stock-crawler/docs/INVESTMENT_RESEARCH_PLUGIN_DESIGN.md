# 投研数据抓取 Plugin 设计文档

## 1. 设计定位

这份设计文档的目标不是把 `stock-crawler` 做成一个很重的平台，也不是一次性解决数据抽象、统一存储、安全治理、结构化标准化等所有问题。

目标只有一个：

把现有 `stock-crawler` 整理成一个**给 Claude Code 使用的数据抓取插件**，用于补充现有 API 方案覆盖不到的投研数据。

当前仓库里已经有 API 方式的数据获取能力：

- [query_data README](/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/query_data/README.md)

因此 `stock-crawler` 的定位应当非常明确：

- 不替代现有 API 插件
- 不做统一数据平台
- 不优先解决安全、存储、规范化等长期问题
- 只做 API 之外的补充抓取能力

## 2. 要解决的问题

`stock-crawler` 主要补三类数据：

1. 时效性更高的数据
   - 网站先更新，但 API 还没出
   - 网站页面有更快的公告、快讯、异动、论坛、新闻流

2. 现有接口没提供或收费的数据
   - 某些页面可见，但 API 不开放
   - 某些数据 API 收费高，但页面能读到核心信息

3. 非结构化数据
   - 公告正文
   - 新闻正文
   - 研报列表页和摘要
   - 页面上的说明文字、备注、脚注、解释性内容

一句话概括：

`query_data` 负责“能直接调 API 的数据”，`stock-crawler` 负责“只能从网页拿、或者网页更合适拿的数据”。

## 3. 设计原则

这次设计遵循下面几个原则：

1. 轻量优先
   - 少量工作先可用，不做大工程。

2. 以网站为入口
   - 接口设计从“哪个网站、抓什么内容”出发，而不是先做统一 dataset 抽象。

3. Markdown 优先
   - 输出主要给大模型和人看，先保证可读性。

4. 尽量复用现有 spider
   - 不在当前代码上再套复杂的 Tool API / Registry / Policy 层。

5. 先解决核心抓取
   - 存储、安全、统一 schema、权限治理先不展开。

## 4. 对现有 stock-crawler 的判断

结论很简单：

- `stock-crawler` 可以继续用
- 不建议大改
- 不建议再包一层很重的抽象
- 更适合做成几个简单、直接的 Claude Code 可调用入口

现有项目已经具备这些能力：

- 配置驱动抓取
- Playwright 登录和动态页面处理
- 链接发现
- 多 parser 解析
- Markdown 输出

这些已经足够支撑第一版插件。

## 5. Plugin 的边界

这个插件只做网页抓取，不负责以下事情：

- 不负责统一数据湖
- 不负责做通用投研数据标准
- 不负责替代现有 API 插件
- 不负责复杂任务编排
- 不负责凭据安全重构
- 不负责下游聚合、回测、统一检索

Claude Code 的使用方式应该是：

1. 先优先尝试 `query_data`
2. 如果 API 不合适，再调用 `stock-crawler`
3. 把抓回来的 Markdown 交给大模型继续分析

## 6. 推荐的接口设计

接口不从“通用数据域”出发，而从“网站 + 目标数据”出发。

不建议做很多工具，第一版建议只保留 3 个核心入口。

### 6.1 `crawl_site_data`

这是主入口。

用途：

- 抓取指定网站的指定数据类型
- 返回 Markdown 结果和抓取产物路径

输入示例：

```json
{
  "site": "lixinger",
  "target": "announcement_list",
  "url": "https://www.lixinger.com/profile/center/my-followed/latest-messages",
  "mode": "single_page"
}
```

另一个示例：

```json
{
  "site": "eastmoney",
  "target": "news_article",
  "url": "https://finance.eastmoney.com/a/202603252345678.html",
  "mode": "single_page"
}
```

返回建议：

```json
{
  "site": "lixinger",
  "target": "announcement_list",
  "url": "https://example.com",
  "status": "completed",
  "summary": "抓取到 20 条公告列表项",
  "markdown_path": "output/.../page.md",
  "artifacts": [
    "output/.../page.md"
  ]
}
```

### 6.2 `crawl_site_links`

用途：

- 从一个入口页发现可继续抓取的链接
- 适合先看某个网站当前有哪些内容值得抓

输入示例：

```json
{
  "site": "cninfo",
  "url": "https://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search",
  "limit": 50
}
```

返回建议：

```json
{
  "site": "cninfo",
  "url": "https://example.com",
  "discovered": [
    {
      "title": "公司公告",
      "url": "https://example.com/a1"
    },
    {
      "title": "业绩快报",
      "url": "https://example.com/a2"
    }
  ]
}
```

### 6.3 `crawl_site_search`

用途：

- 站内按关键词抓搜索结果
- 适合新闻、公告、研报、问答、社区帖子

输入示例：

```json
{
  "site": "xueqiu",
  "target": "search_results",
  "keyword": "宁德时代 年报",
  "limit": 20
}
```

返回建议：

```json
{
  "site": "xueqiu",
  "keyword": "宁德时代 年报",
  "summary": "找到 20 条结果",
  "markdown_path": "output/.../search-results.md"
}
```

## 7. 参数设计原则

参数尽量少，不要设计成一个大而全的系统。

第一版建议只保留这些通用参数：

- `site`
- `target`
- `url`
- `keyword`
- `mode`
- `limit`
- `headless`

说明：

- `site`：网站标识，比如 `lixinger`、`eastmoney`、`xueqiu`
- `target`：想抓的数据类型，比如 `news_article`、`announcement_list`
- `url`：明确页面时直接传 URL
- `keyword`：需要站内搜索时使用
- `mode`：如 `single_page`、`list_page`
- `limit`：最多抓多少条
- `headless`：是否无头浏览器

不要在第一版里引入：

- 通用 query schema
- 数据域枚举体系
- source registry
- 统一 normalizer
- job queue
- 权限策略系统

## 8. 网站配置建议

仍然以网站配置文件为主，不需要改成复杂注册中心。

建议一个网站一个配置文件，继续沿用当前思路，例如：

```text
config/
  lixinger.json
  eastmoney.json
  xueqiu.json
  cninfo.json
```

每个配置文件只回答几个问题：

1. 网站入口是什么
2. URL 规则是什么
3. 是否需要登录
4. 默认 parser 是什么
5. 输出目录是什么

如果后续要更细一点，可以在一个网站下补几个 target 配置，但也不用引入复杂层次。

例如：

```json
{
  "name": "xueqiu-crawler",
  "site": "xueqiu",
  "targets": {
    "news_article": {
      "parser": "article-parser"
    },
    "search_results": {
      "parser": "search-result-parser"
    }
  }
}
```

这个层级已经够用了。

## 9. 输出设计

输出以 Markdown 为主。

原因：

- Claude Code 和大模型可以直接读
- 适合做快速分析
- 不需要先做复杂结构化建模
- 与当前 `stock-crawler` 现状一致

第一版建议输出：

1. 主 Markdown 文件
   - 页面正文
   - 表格
   - 列表
   - 链接
   - 关键信息摘要

2. 可选附加产物
   - 原始 URL
   - 页面标题
   - 抓取时间
   - 截图或原始 HTML

不强制要求：

- 统一 JSON schema
- 全量结构化字段
- 向量化入库
- 检索索引

## 10. 推荐支持的 target 类型

不从大的 dataset 分类出发，而从实际抓取页面类型出发。

第一版建议只支持下面几类：

- `news_article`
- `news_list`
- `announcement_article`
- `announcement_list`
- `report_article`
- `report_list`
- `company_profile`
- `table_page`
- `search_results`
- `api_doc_page`

这些 target 足够覆盖绝大多数补充型投研抓取需求。

## 11. 与现有 query_data 的关系

这部分需要在设计上明确，不然后面容易重复建设。

### 11.1 优先顺序

推荐 Claude Code 的调用顺序：

1. 优先尝试 `query_data`
2. 如果 API 不支持、太贵、太慢或拿不到正文，再走 `stock-crawler`

### 11.2 适合 query_data 的场景

- 标准化行情
- 财务指标
- 历史价格
- 宏观时间序列
- 明确 API 已支持的数据

### 11.3 适合 stock-crawler 的场景

- 公告正文
- 新闻正文
- 页面列表流
- 网站快讯
- 社区内容
- API 没有但页面上有的数据
- 收费 API 的网页替代信息

## 12. 最小实现方案

为了少量工作先达到目标，建议第一版只做下面三件事。

### 12.1 保留现有 crawler 主体

不要大改：

- `CrawlerMain`
- `BrowserManager`
- `ParserManager`
- 各类 parser

### 12.2 加一个很薄的 Claude Code 调用入口

只需要一个轻量入口，把用户输入映射到现有 config 和执行逻辑。

例如增加一个简单入口：

```js
runSiteCrawl({
  site: 'xueqiu',
  target: 'search_results',
  url: 'https://xueqiu.com',
  keyword: '宁德时代',
  limit: 20
})
```

这里的重点是“薄适配”，不是新建一整套平台。

### 12.3 补几个高价值 parser / config

优先做价值最高的网站和页面类型，不要一下铺太开。

建议优先顺序：

1. `lixinger`
   - 公告流、动态页、列表页

2. `cninfo`
   - 公告列表、公告正文

3. `eastmoney`
   - 新闻列表、新闻正文

4. `xueqiu`
   - 搜索结果、讨论页、文章页

## 13. 不建议现在做的事

以下事情都合理，但现在不值得优先做：

- 复杂 Tool API 体系
- Source Registry
- Normalized Output
- Credential & Policy
- 统一 dataset 模型
- 存储平台化
- 任务编排系统
- 全站通用抽象

这些会显著增加设计复杂度，但不会明显提升第一版可用性。

## 14. 推荐文档化方式

为了让 Claude Code 更容易用，文档应重点描述：

1. 支持哪些网站
2. 每个网站支持哪些 target
3. 典型输入示例是什么
4. 典型输出 Markdown 长什么样
5. 什么情况应该优先用 `query_data`
6. 什么情况应该改用 `stock-crawler`

也就是说，这个插件的文档重点不是“架构有多漂亮”，而是“什么时候该用、怎么用、能抓什么”。

## 15. 最终结论

结合你现在的系统，最合适的方案是：

- 保留 `query_data` 作为 API 主通道
- 把 `stock-crawler` 定位成网页补充抓取插件
- 接口从“网站 + 目标数据”出发设计
- 输出以 Markdown 为主
- 不做复杂包装
- 不提前解决安全和存储

所以这份插件设计的核心不是“统一一切”，而是：

**用最少的工作，把网页抓取能力补到现有投研数据体系里。**

## 16. 下一步建议

如果继续推进，建议只做下面两步：

1. 先补文档里的“支持网站 + target 清单”
2. 再做一个很薄的调用入口，把 Claude Code 的参数映射到现有 crawler

这样工作量最小，也最符合现在的目标。

