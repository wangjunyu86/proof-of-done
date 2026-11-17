# Proof of Done

一个用于验证“软件是否真的做完”的 Codex Skill。

它不会因为代码存在、构建通过或界面看起来完整，就直接宣布项目完成。它要求通过可执行检查和可复核证据，区分：

- 代码存在
- 能够干净构建
- 产物真实存在且身份明确
- 能够安装或启动
- 核心用户流程可完成
- 数据能够正确保存和恢复
- 外部集成是真实、模拟还是尚未验证
- 最终产物是否真的适合交付

## 适合解决什么问题

- 验收 AI 或外包交付的软件
- 检查 APK、网站、桌面应用或命令行工具
- 判断“演示版”与“可上线版本”的差距
- 检查支付、登录、消息、AI、上传等功能究竟是真实还是模拟
- 生成带证据的 `Verified / Conditional / Rejected / Inconclusive` 结论

它不是通用代码审查工具，也不能替代专业安全、隐私或合规审计。

## 安装

```bash
git clone https://github.com/wangjunyu86/proof-of-done.git ~/.codex/skills/proof-of-done
```

重新启动 Codex，或让 Codex 重新扫描本地 Skills。

## 使用示例

```text
Use $proof-of-done to verify this APK is genuinely installable and usable.
```

```text
调用 proof-of-done 检查这个项目是否真的可以交付，并保留验收证据。
```

## 输出

Skill 会要求生成一个可复核验收包：

```text
VERDICT.md
proof-manifest.json
claim-matrix.csv
evidence/
logs/
```

初始化验收包：

```bash
python3 scripts/init_evidence_pack.py ./proof-pack --product "Example App"
```

验证验收包：

```bash
python3 scripts/validate_proof_pack.py ./proof-pack
```

## 核心原则

> “构建成功”不等于“用户可以使用”，“按钮存在”也不等于“功能真实完成”。

无法执行的检查必须标记为 `unverified`，不能用推测代替证据。

## License

MIT
