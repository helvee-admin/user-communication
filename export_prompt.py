"""Assemble the selected reply modules for a plain-chat host."""

import argparse
import json
from pathlib import Path
import re


REFERENCES = Path(__file__).resolve().parent / ".agents/skills/customer-reply/references"
PROFILE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def profile_ids(value, field):
    if not isinstance(value, list) or any(
        not isinstance(item, str) or PROFILE_ID.fullmatch(item) is None for item in value
    ):
        raise ValueError(f"{field} 需要由小写字母、数字和连字符组成的 ID 列表")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} 中有重复 ID")
    return value


def read_profile(directory, profile_id):
    if not isinstance(profile_id, str) or PROFILE_ID.fullmatch(profile_id) is None:
        raise ValueError(f"无效的 {directory} ID：{profile_id!r}")
    path = REFERENCES / directory / f"{profile_id}.md"
    if not path.is_file():
        raise ValueError(f"找不到资料文件：{directory}/{profile_id}.md")
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"资料文件为空：{directory}/{profile_id}.md")
    return content


def render(product_override):
    config = json.loads((REFERENCES / "config.json").read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("config.json 需要是一个 JSON 对象")
    roles = profile_ids(config.get("roles"), "roles")
    voices = profile_ids(config.get("voices"), "voices")
    if config.get("default_voice") not in voices:
        raise ValueError("default_voice 必须是已启用的语气 ID")
    role_voices = config.get("role_voices", {})
    if not isinstance(role_voices, dict) or any(
        role not in roles or voice not in voices for role, voice in role_voices.items()
    ):
        raise ValueError("role_voices 只能关联已启用的角色和语气")

    product = config.get("product")
    if product_override is not None:
        product = None if product_override == "none" else product_override
    config = {
        "product": product,
        "roles": roles,
        "voices": voices,
        "default_voice": config["default_voice"],
        "role_voices": role_voices,
    }
    sections = [
        "# 用户回复 Skill",
        "使用本文件中的回复规则和配置处理运营者后续贴来的用户消息。以下是完整的规则和已选资料。"
        "运营者明确另行提供的模块也可按其指定范围使用。",
        (REFERENCES / "reply-rules.md").read_text(encoding="utf-8").strip(),
        "# 当前配置\n\n```json\n" + json.dumps(config, ensure_ascii=False, indent=2) + "\n```",
    ]
    for directory, label, ids in (("roles", "角色", roles), ("voices", "语气", voices)):
        for profile_id in ids:
            sections.append(f"## {label} `{profile_id}`\n\n{read_profile(directory, profile_id)}")
    if product is None:
        sections.append("# 产品资料\n\n当前未选择产品。需要产品事实时，请运营者提供相应资料。")
    else:
        sections.append(f"# 产品资料 `{product}`\n\n{read_profile('products', product)}")
    return "\n\n".join(sections) + "\n"


def main():
    parser = argparse.ArgumentParser(description="导出可直接粘贴给其他 AI 的完整回复提示词")
    parser.add_argument("--product", help="本次导出的产品 ID。使用 none 导出无产品资料的版本")
    parser.add_argument("--output", type=Path, help="输出文件。省略时打印到终端")
    args = parser.parse_args()

    try:
        prompt = render(args.product)
        if args.output is None:
            print(prompt, end="")
        else:
            args.output.write_text(prompt, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"导出失败：{error}\n")


if __name__ == "__main__":
    main()
