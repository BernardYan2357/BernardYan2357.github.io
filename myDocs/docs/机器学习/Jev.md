# Jev

Reference:
- [typesafe.ai](https://typesafe.ai/)
- [如何看待前 OpenAI 研究员发布的新模型 Jev？| 知乎](https://www.zhihu.com/question/2083549123160925836/answer/2083567663226405584)

**TypeSafe AI** 开发的一款决策模型，与生成文本的常规语言模型不同，Jev 专门用于根据你提供的“状态”做出结构化的“判断”

它的输入主要由两部分组成：**状态（state）** 和 **问题（questions）**

- **状态（State）** 是 Jev 需要评估的对象。它可以是一段**文本字符串**，也可以是一个结构化的 **JSON 对象或数组**
- **问题（Questions）** 是一个**问题映射（Map）**，每个问题都有一个唯一的名称（key），并指定了问题类型和评判标准。Jev 支持三种类型的问题原语：

| 问题类型               | 用途        | 输入参数                                                                                   | 返回结果                                                         |
| :----------------- | :-------- | :------------------------------------------------------------------------------------- | :----------------------------------------------------------- |
| **Boolean / Noul** | 是/否判断     | `type: "boolean"`<br>`instructions`: 问题描述<br>`criteria`: 定义真/假的标准                      | `probability`: 一个 0 到 1 之间的概率值，表示答案为“是”的可能性                  |
| **Choice**         | 从一组选项中选一个 | `type: "choice"`<br>`instructions`: 问题描述<br>`criteria`: 选项名称到描述的映射（**最多支持 255 个选项**）   | `choice`: 被选中的选项名称<br>`probabilities`: 每个选项的概率分布             |
| **Score**          | 在有序的尺度上评分 | `type: "score"`<br>`instructions`: 问题描述<br>`criteria`: 一个有序的等级描述数组（**至少 2 个，最多 10 个**） | `score`: 一个可以落在等级之间的评分（如 `2.97`）<br>`probabilities`: 每个等级的概率 |

## 调用

当前仍属于测试阶段（26.9.18），可以在 Vercel 里面调用

## 用途

任何复杂的，可被文本化的，要求在几秒内响应的判断语境都可以试试 Jev

- Browser Use 官方集成 jev-ultrafast，使用 Jev 进行网页查询，例如查询航班等
- 更智能的 Ctrl+F：[Ctrl+F Finds Words. I Wanted It to Find Answers. :: The Tymscar Blog](https://blog.tymscar.com/posts/hunchsemanticfind/)
- Agent 工具中的命令安全审查分类器
- fast-jev-compaction 长上下文压缩，删除一些 BUG 修复这些与主线无关的上下文
- Jev Codex Router 任务难度分流，在任务发起前由 Jev 预判该代码编辑任务的逻辑复杂度，简单改动直接路由到便宜的小模型，复杂跨文件重构才激活大模型；这种思路也可以应用到思考强度上
- 垃圾邮件、短信的分类，客服工单的分类等，涉及到语言理解

## 原理

有人说它是高级版的 BERT

## 引发的思考

著名开发者西蒙·威利斯（Simon Willison）在 [Jev introduces a new shape of LLM—System One, aka Decision Models](https://simonwillison.net/2026/Sep/21/jev/) 中评价：“Jev 实际上代表着机器学习系统的倒退，走向黑箱系统。以前的大模型虽然不能保证正确，但至少你可以要求它们解释它们的决定。Jev 甚至连这点都不给你：你只会得到一个浮点数，这个数字是怎么来的，不知道。”

他很担忧，有人会用 Jev 给求职者排名。有了 Jev 以后，公司筛选简历、挑选面试人从未如此容易，复杂的评估被简化成一个评分题。模型是否会藏有价值观的偏见，对特定身份的歧视？当这种新的评价标准被广泛使用，是否可以称得上是 “算法的暴政”？