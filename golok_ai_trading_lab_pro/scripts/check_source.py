import ast
import re
from pathlib import Path
from xml.etree import ElementTree

roots = (Path("models"), Path("services"), Path("wizard"), Path("views"), Path("security"), Path("static"))
sources = sorted(path for root in roots for path in root.rglob("*") if path.suffix in {".py", ".xml", ".js", ".csv", ".scss"})
sources.extend(Path(name) for name in ("__manifest__.py", "__init__.py"))
order_api = re.compile(r"placeOrder|modifyOrder|cancelOrder|(?:^|/)order/v\d|transferFunds", re.I)
credential = re.compile(r"""(?:api_key|password|pin|jwt_token|refresh_token|totp_secret)\s*[:=]\s*["'][^"']+["']""", re.I)
for path in sources:
    content = path.read_text(encoding="utf-8")
    assert not order_api.search(content), f"Order API pattern in {path}"
    assert not credential.search(content), f"Credential literal pattern in {path}"
    if path.suffix == ".py":
        ast.parse(content, filename=str(path))
    if path.suffix == ".xml":
        ElementTree.fromstring(content)
manifest = ast.literal_eval(Path("__manifest__.py").read_text())
assert manifest["depends"] == ["web"]
assert "external_dependencies" not in manifest
print(f"PASS: inspected {len(sources)} runtime source files")
print("PASS: Python AST and XML basic parsing")
print("PASS: no matches for broker order methods, versioned order paths or credential literal patterns")
print("PASS: Odoo web is the only manifest dependency")
