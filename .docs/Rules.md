# Rules & Guardrails

## 1. Technical Guardrails & Constraints
- **Cross-Platform Compatibility**: Always normalize path separators using forward slashes (`/`) and `os.path.relpath(..., root_dir).replace("\\", "/")` to prevent Windows drive letter (`G:`) / separator issues.
- **Tree-sitter AST Traversal**:
  - Always extract function names from declarator hierarchies in C/C++ (`function_declarator`).
  - Always filter out forward-declarations / type references without body for `struct_specifier` and `class_specifier`.
  - Always resolve variable declaration names for JavaScript arrow functions.
- **Error Handling**: All API route handlers and parsers must have defensive try/catch blocks with logging via `utils.logger.logger`.
- **No Mock / Placeholder Code**: Never leave `// TODO` or empty placeholder logic in production paths. Always provide complete, verifiable implementations.
- **Testing Standard**: Every new component or bug fix must be accompanied by automated tests in `tests/` verifying nominal and edge cases.

## 2. Coding Style & Conventions
- **Python**: PEP 8 standards, explicit type annotations (`typing.List`, `typing.Dict`, `typing.Any`, `typing.Optional`).
- **Pydantic**: Use Pydantic BaseModel for request payloads.
- **Plotly**: Use `plotly.graph_objects.Figure` with consistent color palettes and hover tooltips.
