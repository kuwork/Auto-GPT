# 网站和文档站点 📰📖
请查看*https://agpt.co*，这是Auto-GPT官方的新闻和更新站点！文档也在这里，位于*https://docs.agpt.co*

# 对于贡献者 👷🏼
自发布v0.3.0以来，我们一直在重新构建Auto-GPT核心，使其更具可扩展性，并为结构性能导向的研发腾出空间。
同时，我们有较少的时间处理传入的拉取请求和问题，因此我们专注于高价值的贡献：
 * 重大的错误修复
 * 对现有功能和/或文档的*主要*改进（因此不包括单个拼写错误修复）
 * 对我们进行重新架构和其他路线图条目的贡献
为了不断取得进展，我们必须有所选择，但这并不意味着您无法做出贡献。请查看我们维基上的贡献指南:
https://github.com/Significant-Gravitas/Auto-GPT/wiki/Contributing

# 🚀 v0.4.0 发布 🚀
自v0.3.1版本发布以来，两周时间过去了，共有76个请求合并，我们很高兴地宣布
发布了v0.4.0！

自v0.3.0以来的亮点和显着变化：

## ⚠️ 命令 `send_tweet` 已被删除
Twitter 功能（及更多功能）现在已由插件覆盖。

## ⚠️ 内存后端弃用 💾
Milvus、Pinecone 和 Weaviate 内存后端与内存系统的工作不兼容，已在主分支中删除。Redis
内存存储也暂时删除；我们将尽快合并新的实现。是否在未来再次添加其他后端的内置支持还有待讨论，请随时加入: https://github.com/Significant-Gravitas/Auto-GPT/discussions/4280

## `read_file` 支持文档 📄
Auto-GPT 现在可以从文档文件中读取文本，支持 PDF、DOCX、CSV、HTML、TeX 等格式！

## 管理 Auto-GPT 对命令的访问 ❌🔧
您现在可以通过.env 中的 *DISABLED_COMMAND_CATEGORIES* 变量禁用一组内置命令。也可以使用 *DENY_COMMANDS* 禁用特定的 shell 命令，
或使用 *ALLOW_COMMANDS* 有选择地启用它们。

## 更多修复和更改 🛠️
其他亮点包括 self-feedback 模式和连续模式、文档、Docker 和 devcontainer 设置等方面的改进，以及许多其他改进。
大部分改进对用户尚不可见，但从长远来看将会有所回报。请查看Github上的发布说明获取完整的更新日志！
https://github.com/Significant-Gravitas/Auto-GPT/releases