# ChangeLog

## [1.0.0] - 2026-03-10

### Added
- **README.md** - Project overview with quick start guide
- **getting-started.md** - Beginner guide with Markdown slide format (convertible to PPTX)
- **Project structure documentation** - Emphasis on `.claude` directory importance and MCP/Skill integration
- **LLM portability documentation** - Appendix D explaining technical feasibility of supporting other LLMs beyond Claude

## [Unreleased]

### Changed
- **how-to-start-LLM-base-scan.md**: Removed redundant "install serena in advance" instruction. Section 1-b (`claude mcp add serena`) already handles serena installation, making the introductory text unnecessary. Clarified that uv is required as a prerequisite for the installation command in section 1-b. (2026-03-10)
- **how-to-start-LLM-base-scan.md**: Added Appendix D explaining LLM portability and flexibility. Documents that the tool architecture supports migration to other LLMs (Codex, Gemini, Llama) beyond Claude, with technical rationale and migration strategies. (2026-03-10)
- **how-to-start-LLM-base-scan.md** and **getting-started.md**: Clarified automatic project detection mechanism. Project type (language/framework/architecture) is auto-detected within the launch directory. Added Footnote [3] in how-to-start explaining cwd-based exploration logic. (2026-03-10)
- **getting-started.md**: Changed "入力と出力の流れ" section to clarify that auto-detection happens within the launch directory, not that LLM selects which repo to scan. (2026-03-10)

### Removed
- **how-to-start-LLM-base-scan.md**: Removed Appendix D (WIP Web version example) as it was incomplete/under construction. (2026-03-10)
- **getting-started.md**: Removed "将来の拡張可能性" (future expansion possibilities) subsection from v1.0.0 scope to focus on current JavaScript/Node.js support. (2026-03-10)
- **getting-started.md**: Removed "付録 C：Python 拡張概要" (Appendix C: Python expansion overview). Detailed implementation approaches not relevant for beginner guide. (2026-03-10)
