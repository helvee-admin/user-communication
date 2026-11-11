# Customer Reply · 用户沟通 Skill

`customer-reply` 为用户评论、私信和客服咨询起草可直接复制的回复。贴入用户原话，Skill 会判断对方最需要什么，用同一个品牌小助手的口吻回应。你可以把答复复制到原平台发送。

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

在仓库目录里打开新对话即可用 `$customer-reply`。完整项目还包括配置说明和提示词导出工具。 [OpenAI Skills 文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)

**普通 AI 对话。** 把便携提示词的完整内容放进新对话或助手的长期指令，再发用户原话。 [PORTABLE-PROMPT.md](PORTABLE-PROMPT.md)

## 第一次使用

在 Codex 调用 `$customer-reply`，直接贴一条用户来信。产品、人设和回复方式由配置与来信内容确定。

```text
这个封面好可爱，可是我一点保存就闪退。
```

Skill 会优先回应闪退，直接给出一段可发给用户的文字。对方说的对象不清楚时，也会给一句能发给对方的追问。

如果回复以 `需要你补充｜` 开头，那是给运营者的提问。例如来信问「昨天答应我的奖励已经发了吗？」，而这笔发放记录需要你核对。核对后，在同一对话紧接着回复这条补充，Skill 会继续起草上一条来信的答复。

```text
补充上一条｜这笔奖励昨天通过平台私信发出了。
```

每条新来信单独处理。平时直接粘贴原话即可，产品与人设通过配置文件或助手设置调整。如果来信恰好以「补充上一条｜」开头，可以先加「原文：」标明这是一条新来信。

## 配置产品和人设

在 `customer-reply` 技能目录里编辑 `references/`。用 Codex 安装器安装时，默认目录是 `~/.codex/skills/customer-reply/`。直接打开完整仓库时，目录是 `.agents/skills/customer-reply/`。导出工具读取完整仓库里的配置。

| 想调整什么 | 文件 |
| --- | --- |
| 当前产品 | [config.json](.agents/skills/customer-reply/references/config.json) |
| 功能、权益、活动和公开支持入口 | [products/](.agents/skills/customer-reply/references/products/) |
| 品牌小助手的称呼、性格和表达风格 | [persona.md](.agents/skills/customer-reply/references/persona.md) |
| 排障、建议、社区互动、活动、应对骚扰的处理方式 | [reply-rules.md](.agents/skills/customer-reply/references/reply-rules.md) |

### 添加或切换产品

1. 复制产品资料模板，在同一目录改名为 `my-product.md`，填入已核实、可对外使用的事实。文件名用小写英文字母、数字和连字符。 [产品资料模板](.agents/skills/customer-reply/references/products/template.md)
2. 把 `config.json` 的 `"product": null` 改成 `"product": "my-product"`。用纯文字助手时，重新导出并替换助手里的提示词。
3. 产品功能或活动有变化时，更新对应的产品文件。活动写清状态、日期和资格。个案的订单、联系方式、兑换码或发放状态在处理该条来信时按需核对。

默认产品为空，可以先处理普通互动。需要确定功能入口、权益或活动条件时，Skill 会按需请你确认。仓库默认忽略新增的产品资料文件和 `local/` 目录。

### 调整品牌小助手

编辑 `persona.md`，写清小助手的名称、称呼、说话方式和表情使用习惯。排障时的克制和闲聊时的轻松属于同一个人设。想调整某种场景下要解决的事，或想修改什么时候该追问，编辑 `reply-rules.md`。

## 升级与迁移

从旧版升级时，先备份自己的产品资料和定制规则，再用新版的整个 `customer-reply` 文件夹替换旧文件夹。恢复自己的产品 Markdown 文件，并在新版 `config.json` 中填写 `product`。原来保存在语气文件里的称呼和表达偏好可以迁入 `persona.md`，业务场景的定制规则可以迁入 `reply-rules.md`。纯文字助手需要替换成新版导出提示词。

支持 Agent Skills 的工具可以导入完整的 `.agents/skills/customer-reply/` 目录，保留 `SKILL.md` 和 `references/` 的相对位置。复制完整仓库可以一并保留导出工具。

### 导出给其他 AI

使用 Python 3，在完整仓库根目录运行命令。它会把人设、回复规则和当前产品资料组装成一份提示词。

```sh
mkdir -p local
python3 export_prompt.py --output local/customer-reply-prompt.md
```

可用 `--product` 指定本次导出的产品。下面使用虚构示例，也可以换成你自己的产品 ID。

```sh
python3 export_prompt.py --product example-notes --output local/example-notes-prompt.md
```

省略 `--output` 会把提示词打印到终端。用 `--product none` 可导出空产品版本。粘贴到外部助手之前，检查该份文件中的产品资料和规则是否适合共享。

接入其他应用时，可以把导出稿放在助手的指令层，将来信作为独立输入。以 `需要你补充｜` 开头的结果交给运营者核实，其他结果可展示为待复制的回复。

## 试用消息

| 粘贴的原话 | 应有表现 |
| --- | --- |
| 「这个在哪儿领？」 | 给一句能发给对方的追问，确认对方想领什么。 |
| 「这个封面好可爱，可是我一点保存就闪退。」 | 先处理保存问题，给一个有依据的步骤或问一个能帮助排查的问题。 |
| 「昨天答应我的奖励已经发了吗？」 | 缺个案记录时，用 `需要你补充｜` 向运营者核实。 |

## 许可证

[MIT](LICENSE)
