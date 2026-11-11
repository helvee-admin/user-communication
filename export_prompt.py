"""Assemble the selected reply modules for a plain-chat host."""

import argparse
import json
from pathlib import Path
import re


REFERENCES = Path(__file__).resolve().parent / ".agents/skills/customer-reply/references"
PROFILE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


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
    product = config.get("product")
    if product_override is not None:
        product = None if product_override == "none" else product_override
    sections = [
        "# 用户回复 Skill",
        "使用本文件中的固定人设和规则，处理运营者随后粘贴的用户原话。",
        (REFERENCES / "persona.md").read_text(encoding="utf-8").strip(),
        (REFERENCES / "reply-rules.md").read_text(encoding="utf-8").strip(),
    ]
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
