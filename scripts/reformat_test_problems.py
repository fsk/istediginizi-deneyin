#!/usr/bin/env python3
"""Reformat TEST_PROBLEMS.md: only Senaryo + Nasıl tetiklenir per item."""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

BASE = "http://localhost:7070/api"
ROOT = Path(__file__).resolve().parents[1]


def parse_problems(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    order, sections, current_h2 = [], {}, None
    i = 0
    while i < len(lines):
        m = re.match(r"^## (\d+\w*\.?)\s+(.+)$", lines[i])
        if m:
            current_h2 = f"## {m.group(1).strip('.')}. {m.group(2)}"
            if current_h2 not in sections:
                order.append(current_h2)
                sections[current_h2] = []
            i += 1
            continue
        m = re.match(r"^### ([a-z])\)\s+(.+)$", lines[i])
        if m and current_h2:
            sub = f"### {m.group(1)}) {m.group(2)}"
            i += 1
            tags, prob = "", ""
            scenario_lines, trigger_lines = [], []
            mode = None
            while i < len(lines):
                if lines[i].startswith("## "):
                    break
                if lines[i].startswith("### ") and re.match(r"^### [a-z]\)", lines[i]):
                    break
                if lines[i].strip() == "---":
                    i += 1
                    break
                pm = re.match(
                    r"^- \[ \] \*\*((?:Lab(?:\s*\|\s*Prod)?|Prod|Teori(?:\s*→\s*Lab)?(?:\s*\|\s*Prod)?)\s*)?\*\*Problem:\*\*\s*(.+)$",
                    lines[i],
                )
                if not pm:
                    pm2 = re.match(r"^- \[ \] \*\*Problem:\*\*\s*(.+)$", lines[i])
                    if pm2:
                        prob = pm2.group(1).strip()
                else:
                    tags, prob = (pm.group(1) or "").strip(), pm.group(2).strip()
                if re.match(r"^\*\*[123]\)", lines[i]) and "Senaryo" in lines[i]:
                    mode = "scenario"
                    i += 1
                    continue
                if "Nasıl tetiklenir" in lines[i]:
                    mode = "trigger"
                    i += 1
                    continue
                if lines[i].startswith("**1) Problem"):
                    mode = "skip"
                    i += 1
                    continue
                if mode == "scenario" and lines[i].strip():
                    if not lines[i].startswith("**"):
                        scenario_lines.append(lines[i].rstrip())
                elif mode == "trigger":
                    trigger_lines.append(lines[i].rstrip())
                elif mode == "skip" and lines[i].strip() and not lines[i].startswith("**"):
                    i += 1
                    continue
                i += 1
            sections[current_h2].append(
                {
                    "sub": sub,
                    "tags": tags,
                    "prob": prob,
                    "scenario": scenario_lines,
                    "trigger": trigger_lines,
                    "key": (current_h2, sub),
                }
            )
            continue
        i += 1
    return order, sections


def parse_orig_scenarios(path: Path):
    _, sec = parse_problems(path)
    return {item["key"]: item["scenario"] for items in sec.values() for item in items}


def format_scenario(parts: List[str]) -> str:
    if not parts:
        return "—"
    paras = []
    for raw in parts:
        p = raw.strip().lstrip("- ").strip()
        if not p:
            continue
        # Tek satırda birleşik cümleler → paragraflara böl
        if ". " in p and "\n" not in p:
            for sent in re.split(r"(?<=[.!?])\s+", p):
                sent = sent.strip()
                if sent:
                    if sent[-1] not in ".!?":
                        sent += "."
                    paras.append(sent)
        else:
            if p[-1] not in ".!?":
                p += "."
            paras.append(p)
    return "\n\n".join(paras) if paras else "—"


def trigger_is_rich(trigger: List[str]) -> bool:
    joined = "\n".join(trigger)
    return "```" in joined or len(joined) > 350


def order_create_body(items_json: str) -> str:
    return f"""```http
POST {BASE}/orders/create-order
Content-Type: application/json

{{
  "userId": "USER-UUID",
  "items": {items_json},
  "shippingAddressId": "ADDRESS-UUID",
  "billingAddressId": "ADDRESS-UUID"
}}
```"""


def generate_trigger(p: dict) -> str:
    sub, prob, h2 = p["sub"], p["prob"], p["h2"]
    t = (sub + prob + h2).lower()

    if trigger_is_rich(p.get("trigger", [])):
        lines = [ln for ln in p["trigger"] if not re.match(r"^\*\*[23]\)", ln)]
        return "\n".join(lines).strip()

    # --- Rich templates ---
    if "race condition" in sub.lower():
        return f"""Aynı ürüne çok sayıda siparişi **aynı anda** gönder. Stok yeterli görünse bile hepsi geçebilir; sonunda stok eksi veya fazla sipariş oluşabilir.

**Hazırlık:**
```sql
UPDATE products SET stock_quantity = 100 WHERE product_id = 'URUN-UUID';
```

**İstek (her paralel çağrıda aynı — 1 adet):**
{order_create_body('[{ "productId": "URUN-UUID", "quantity": 1 }]')}

`test-scripts/load_test_order.py` ile 150 paralel istek gönderebilirsin.

**Kontrol:** `stock_quantity >= 0` ve başarılı sipariş sayısı ≤ 100."""

    if "deadlock" in sub.lower():
        return """Aynı anda **iki sipariş** gönder; birinde ürün sırası A→B, diğerinde B→A olsun.

**İstek 1** (önce A, sonra B):
""" + order_create_body("""[
    { "productId": "PROD-A-UUID", "quantity": 1 },
    { "productId": "PROD-B-UUID", "quantity": 1 }
  ]""") + """

**İstek 2** (önce B, sonra A):
""" + order_create_body("""[
    { "productId": "PROD-B-UUID", "quantity": 1 },
    { "productId": "PROD-A-UUID", "quantity": 1 }
  ]""") + """

İkisini aynı anda çalıştır. Log: `deadlock detected`."""

    if "lost update" in sub.lower():
        return """**Hazırlık:**
```sql
UPDATE products SET stock_quantity = 100 WHERE product_id = 'URUN-UUID';
```

**İstek 1** (10 adet) ve **İstek 2** (5 adet) — aynı `productId`, **paralel**:
""" + order_create_body('[{ "productId": "URUN-UUID", "quantity": 10 }]') + """

""" + order_create_body('[{ "productId": "URUN-UUID", "quantity": 5 }]') + """

**Kontrol:** Stok **85** olmalı; **95** görürsen lost update."""

    if "pessimistic" in sub.lower():
        return f"""**Lab endpoint** (sipariş `PENDING` iken):
```http
POST {BASE}/orders/{{orderId}}/test-concurrent-pessimistic-update?status1=CONFIRMED&status2=PROCESSING
```

**Normal kullanım:**
```http
PATCH {BASE}/orders/{{orderId}}/status
Content-Type: application/json

{{"status": "CONFIRMED"}}
```
`findByIdForUpdate` ile satır kilitlenir; ikinci istek bekler."""

    if "off-by-one" in sub.lower() or "checkquantity" in sub.lower():
        return f"""**Hazırlık:**
```sql
UPDATE products SET stock_quantity = 5 WHERE product_id = 'URUN-UUID';
```

**İstek** (tam stok kadar sipariş):
{order_create_body('[{ "productId": "URUN-UUID", "quantity": 5 }]')}

Beklenti: İş kuralına göre **başarılı** olmalı; `checkQuantity` `>` kullandığı için **400 / stok yok** dönebilir."""

    if "n+1" in sub.lower() or ("order listesi" in sub.lower()):
        return f"""```http
GET {BASE}/orders/user/USER-UUID
```

SQL log açıkken çağır: 1 `orders` sorgusu + her order için 1 `order_items` sorgusu (N+1)."""

    if "deep pagination" in sub.lower() or ("offset" in t and "pagination" in sub.lower()):
        return f"""```http
GET {BASE}/orders?page=100000&size=20&sortBy=orderDate&direction=DESC
```

Büyük `orders` tablosunda süre artar veya timeout."""

    if "multiplebag" in sub.lower():
        return f"""```http
GET {BASE}/users/USER-UUID/test-multiple-bag-fetch
```

Beklenti: HTTP 400, `MULTIPLE_BAG_FETCH`."""

    if "stalestate" in sub.lower() or ("optimistic lock exception" in sub.lower()):
        return f"""```http
POST {BASE}/products/PRODUCT-UUID/test-concurrent-update?quantity1=10&quantity2=5
```

Beklenti: Biri 409 CONFLICT (`OPTIMISTIC_LOCKING_FAILED`)."""

    if "sql injection" in sub.lower():
        return f"""```http
GET {BASE}/products/search?name=' OR '1'='1
```

JPQL parametreli olduğu için risk düşük; **native query** eklersen tekrar dene."""

    if "missing index" in sub.lower() or "full table scan" in sub.lower() or ("leading wildcard" in sub.lower()):
        return f"""```http
GET {BASE}/products/search?name=laptop
```

`EXPLAIN ANALYZE` ile seq scan / yavaşlık."""

    if "negative stock" in sub.lower():
        return f"""Stok=1 yap:
```sql
UPDATE products SET stock_quantity = 1 WHERE product_id = 'URUN-UUID';
```

Aynı ürüne **paralel** 2+ sipariş:
{order_create_body('[{ "productId": "URUN-UUID", "quantity": 1 }]')}

Kontrol: `stock_quantity` negatif mi?"""

    if "order status" in sub.lower():
        return f"""```http
PATCH {BASE}/orders/ORDER-UUID/status
Content-Type: application/json

{{"status": "CANCELLED"}}
```
`DELIVERED` siparişte 400 beklenir."""

    if "connection pool" in sub.lower():
        return f"""Çok sayıda paralel istek:
{order_create_body('[{ "productId": "URUN-UUID", "quantity": 1 }]')}

`application.yml` içinde Hikari `maximum-pool-size: 5` yapıp tekrarla; timeout artar."""

    if "get-all-users" in t.lower() or ("kullanıcı listesi" in sub.lower()):
        return f"""```http
GET {BASE}/users/get-all-users
```
Çok kullanıcıda yavaş / bellek baskısı."""

    if "bulk" in sub.lower() and "kısmi" in sub.lower():
        return f"""```http
POST {BASE}/orders/bulk
Content-Type: application/json
```
10 kalem gönder, birinde stoksuz ürün kullan; kaç order oluştu say."""

    if "payment" in sub.lower() and "shipment" in sub.lower():
        return f"""{order_create_body('[{ "productId": "URUN-UUID", "quantity": 1 }]')}

```sql
SELECT * FROM payments WHERE order_id = 'ORDER-UUID';
SELECT * FROM shipments WHERE order_id = 'ORDER-UUID';
```
Kayıt yoksa problem doğrulanır."""

    if "report" in sub.lower() or "rapor" in sub.lower():
        return f"""```http
GET {BASE}/orders/report?startDate=2020-01-01T00:00:00&endDate=2026-12-31T23:59:59
```"""

    if "stats" in sub.lower():
        return f"""```http
GET {BASE}/orders/stats
```"""

    if "dirty read" in sub.lower() or "phantom read" in sub.lower() or "non-repeatable" in sub.lower():
        return """Bu projede varsayılan izolasyon çoğu senaryoda bunu göstermez.

**Denemek için:** İki DB oturumu aç; birinde `BEGIN` + `UPDATE` (commit etme), diğerinde `SELECT`. İzolasyon seviyesini bilinçli düşür (`READ UNCOMMITTED` — sadece test DB)."""

    if any(x in h2.lower() for x in ["redis", "rabbit", "docker", "queue", "gateway", "27b"]):
        if "security" not in h2.lower():
            return """**Bu projede hazır HTTP endpoint yok** (veya sadece altyapı üzerinden).

1. `cd demo-project && docker compose up -d`
2. İlgili servis config'ini `application.yml` içinde kontrol et
3. Problem Redis/Rabbit/Docker davranışına bağlıysa o servisle test et"""

    if "ddl-auto" in sub.lower() or "show-sql" in sub.lower():
        return """`demo-project/ecommerce/src/main/resources/application.yml` içinde ilgili ayarı değiştir, uygulamayı yeniden başlat."""

    if "actuator" in sub.lower():
        return """```http
GET http://localhost:7070/actuator/health
```
Production'da expose edilmemeli."""

  # default
    return f"""**Bu repoda en yakın akış:**

{order_create_body('[{ "productId": "URUN-UUID", "quantity": 1 }]')}

```http
GET {BASE}/orders/user/USER-UUID
```

```http
GET {BASE}/products/search?name=test
```

Gerekirse SQL + paralel script ile senaryoyu tamamla. `USER-UUID`, `URUN-UUID`, `ADDRESS-UUID` değerlerini DB'den al."""


def main():
    cur_order, cur_sec = parse_problems(ROOT / "TEST_PROBLEMS.md")

    orig_scenarios = {}
    orig_path = Path("/tmp/tp_orig.md")
    if orig_path.exists():
        orig_scenarios = parse_orig_scenarios(orig_path)
    # section 7-12 may only exist in current file
    cur_scenarios = {item["key"]: item["scenario"] for items in cur_sec.values() for item in items}
    for k, v in cur_scenarios.items():
        if v and (k not in orig_scenarios or len("\n".join(v)) > len("\n".join(orig_scenarios.get(k, [])))):
            orig_scenarios[k] = v

    out = [
        "# E-Commerce Projesi - Test Edilebilecek Problemler",
        "",
        "Her maddede yalnızca **1) Senaryo** ve **2) Nasıl tetiklenir?** vardır. Problem özeti checkbox satırındadır.",
        "",
        f"Öğrenme sırası: [`TEST_PROBLEMS_RANKED.md`](TEST_PROBLEMS_RANKED.md) · Base URL: `{BASE}`",
        "",
    ]

    for h2 in cur_order:
        items = cur_sec.get(h2, [])
        if not items:
            continue
        out += ["---", "", h2, ""]
        for p in items:
            if not p.get("prob"):
                continue
            p["h2"] = h2
            key = p["key"]
            scenario_src = orig_scenarios.get(key, []) or p.get("scenario", [])

            tag = f" `{p['tags']}`" if p.get("tags") else ""
            out.append(p["sub"])
            out.append("")
            out.append(f"- [ ]{tag} **Problem:** {p['prob']}")
            out.append("")
            out.append("**1) Senaryo**")
            out.append("")
            out.append(format_scenario(scenario_src))
            out.append("")
            out.append("**2) Nasıl tetiklenir? (Endpoint / istek)**")
            out.append("")
            out.append(generate_trigger(p))
            out.append("")
            out.append("---")
            out.append("")

    (ROOT / "TEST_PROBLEMS.md").write_text("\n".join(out), encoding="utf-8")
    print("Wrote", sum(len(cur_sec[k]) for k in cur_order), "problems")


if __name__ == "__main__":
    main()
