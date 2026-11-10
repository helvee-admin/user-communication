---
name: customer-reply
description: Use when drafting a copy-ready reply to a user's social comment, direct message, support question, product feedback, or promotion inquiry. 适用于需要回复用户评论、私信、客服咨询、反馈或领奖问题的场景。
---

# 用户回复

按运营者提交的来信起草一条可复制的回复。根据来信选角色，根据当前产品资料给事实，根据渠道和对方状态调整语气。

1. 读取 [回复规则](references/reply-rules.md) 和 [当前配置](references/config.json)。所有路径相对此 `SKILL.md` 所在目录。
2. 看 `roles` 中已启用角色的「适用」行以选主角色。读命中的 [角色文件](references/roles/)，需要兼顾另一项请求时再读对应角色。缺少适用角色时按共用规则处理。
3. 读取选中的 [语气文件](references/voices/)；涉及产品事实时，只读取本条选中的 [产品文件](references/products/)。产品和语气的选用顺序见回复规则。模板是配置示例，只有运营者明确提供或选择的资料才可用于产品答复。
4. 使用回复规则中的输出格式。只有运营者明确补充的记录或资料可以用来确认个人状态。

例如来信只有「这个在哪里领？」时，可以回「你想领的是哪一样呀？」。来信问「我的奖励已经发了吗？」且缺发放记录时，用 `需要你补充｜` 向运营者问这一笔的状态。
