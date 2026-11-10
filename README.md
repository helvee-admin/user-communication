# Customer Reply · 用户沟通 Skill

`customer-reply` 用来起草可直接复制的评论、私信和客服回复。你可以只贴原话，也可以把平台、类型和上文一起贴。Skill 按消息内容选用角色，并用当前产品资料和语气写出一条回复。发送由你在原平台完成。

## 安装

**Codex 快速安装。** 在对话中选用 `$skill-installer`，再发这段话。

```text
请从 https://github.com/helvee-admin/user-communication/tree/main/.agents/skills/customer-reply 安装 customer-reply。
```

如果技能没有出现在选择器里，重启 Codex 后在新对话里调用 `$customer-reply`。

**下载完整项目。** 在 GitHub 仓库点击 **Code → Download ZIP**，解压后用 Codex 打开仓库根目录。也可以用 Git 克隆。

```sh
git clone https://github.com/helvee-admin/user-communication.git
cd user-communication
```

仓库自带工作区技能。在这个目录里打开新对话即可用 `$customer-reply`。完整项目还包括产品模板、配置说明和提示词导出工具。安装路径见 [OpenAI Skills 文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。

**普通 AI 对话。** 把 [PORTABLE-PROMPT.md](PORTABLE-PROMPT.md) 的完整内容粘贴到新对话或助手的长期指令里，再发用户原话。

## 第一次使用

在 Codex 里调用 `$customer-reply`，然后贴来信。平台和类型可以省略。

```text
平台：小红书
类型：评论
原文：哈哈这个封面也太萌啦！
```

需要使用特定产品或口吻时，可以把下面这些字段放在「原文」前。原文可以有多行；把它作为最后一项。

```text
平台：抖音
类型：私信
产品：example-notes
语气：natural
上文：对方正在问任务详情里的分享功能。
原文：这个能导出 PDF 吗？
```

这个例子可直接用于 Codex。普通对话若使用带示例产品的版本，先按下方的导出方法把 `example-notes` 一起带过去。

Skill 默认输出一段给用户的话。开头出现 `需要你补充｜` 时，这条问题是给你看的。例如 AI 缺少某笔奖励的发放记录，可以回复 `补充：这笔已经发了，昨天通过平台私信送达。` 它会据此接着写同一条回复。处理多条时，先注明要逐条回复并给原文编号；补充时带上相应编号。

## 配置角色、语气和产品

在已安装的 `customer-reply` 技能目录里编辑 `references/`。用 Codex 安装器安装时，默认目录是 `~/.codex/skills/customer-reply/`。直接打开仓库使用时，对应目录是仓库下的 `.agents/skills/customer-reply/`。如果用的是完整仓库，导出工具读取仓库里的配置。

| 想调整什么 | 文件 |
| --- | --- |
| 默认产品、启用角色、默认语气、角色常用语气 | [config.json](.agents/skills/customer-reply/references/config.json) |
| 不同类型的消息该怎么办 | [角色目录](.agents/skills/customer-reply/references/roles/) |
| 怎么称呼、写多长、用几个表情、说话风格 | [语气目录](.agents/skills/customer-reply/references/voices/) |
| 功能入口、权益、活动条件、公开支持方式 | [产品目录](.agents/skills/customer-reply/references/products/) |
| 何时直接回、何时向谁追问、输出格式 | [共用回复规则](.agents/skills/customer-reply/references/reply-rules.md) |

`config.json` 中的 ID 对应文件名去掉 `.md`。用小写英文字母、数字和连字符。初始配置启用社区互动、客服答疑、反馈沟通、活动运营四个角色，默认语气是自然亲切，产品为空。空产品可以处理普通互动；涉及具体功能或活动条件时，AI 会使用你随消息提供的已核实资料，缺事实时才问你。

### 添加或切换产品

1. 复制 [产品资料模板](.agents/skills/customer-reply/references/products/template.md)，在同一目录改名为 `my-product.md`，写入可对外使用的事实。
2. 常用这个产品时，把 `config.json` 的 `"product": null` 改成 `"product": "my-product"`。偶尔切换时，在该条消息加 `产品：my-product`。想在当前对话连续用它，可以发「配置：接下来都用 my-product」。
3. 产品功能或活动有变化时，更新对应的产品文件。给活动标上生效状态和日期，个人申请进度按单条个案补充。仓库默认忽略新增的产品资料文件。分享仓库改动或导出稿前，检查它们是否包含内部信息。

### 增删角色

复制一份现有角色到 `references/roles/`，改名后写清「适用、目标、依据、写法、示例」，再把新 ID 加到 `roles`。例如可以新增 `partnership.md`，设定遇到合作邀约时先确认合作形式和发布时间，报价以你给的资料为准。

停用角色时，从 `roles` 列表移除它，并删除 `role_voices` 里对应的映射。原文件可以保留以便日后启用。多个角色同样合适时，列表靠前的作为主角色；有具体求助时，先解决眼前的问题。

### 调整语气

内置 [自然亲切](.agents/skills/customer-reply/references/voices/natural.md)和[轻松可爱](.agents/skills/customer-reply/references/voices/playful.md)。复制一个语气文件即可添加自己的版本。写清称呼、句长、表情数量或频率，以及一两句你愿意直接发的示例；新 ID 加到 `voices`。

- 调整常用语气时，改 `default_voice`。
- 想让社区互动默认可爱一点，可以在 `role_voices` 中设置 `"community": "playful"`。
- 单条想换口吻，在原文前加 `语气：playful`。产品资料可单独设置品牌对外称谓。
- 遇到投诉、内容丢失或付费争议时，共用规则会把回复收回到清楚、克制的表达。

## 迁移和接入

支持 Agent Skills 文件夹的工具可以导入完整的 `.agents/skills/customer-reply/` 子目录。带上 `SKILL.md` 和 `references/`，保留相对目录。复制整个 `user-communication` 目录也会保留本说明书和导出工具。

只支持文字指令的工具使用 [PORTABLE-PROMPT.md](PORTABLE-PROMPT.md)。它是导出稿，配置以各模块的源文件为准。修改模块后，在本目录运行下列命令刷新导出稿，使用 Python 3 标准库即可。

```sh
python3 export_prompt.py --product none --output PORTABLE-PROMPT.md
```

也可以为某个产品单独导出一份。下面是虚构产品的例子。

```sh
mkdir -p local
python3 export_prompt.py --product example-notes --output local/example-notes-prompt.md
```

省略 `--output` 会直接把提示词打印到终端。目标 AI 会以你粘贴进去的配置和产品资料作答。切换到另一产品时，重新导出或在对话里明确提供该产品的资料。给外部 AI 粘贴前，检查导出稿里有哪些对外事实和内部规则；个案的订单、联系方式和兑换码留在单次处理里。

接入其他应用时，可以把导出稿放在助手的指令层，把平台、类型、上文、原文作为本条输入。可将以 `需要你补充｜` 开头的结果展示给运营者，其余结果显示为待复制的用户回复。

## 三条试用消息

| 输入 | 应有表现 |
| --- | --- |
| 「这个在哪儿领？」 | 给一句能发给对方的追问。 |
| 「这个封面好可爱，可是我一点保存就闪退。」 | 优先处理保存问题，最多问一个能帮助排查的信息。 |
| 「昨天答应我的奖励已经发了吗？」 | 缺个案记录时，用「需要你补充｜」向你核实状态。 |

更新语气时，用几条你平常会收到的来信对照输出。把你愿意直接复制的句子留作语气示例，比反复调整「更活泼」「更专业」这类形容词更容易复用。

## 许可证

[MIT](LICENSE)
