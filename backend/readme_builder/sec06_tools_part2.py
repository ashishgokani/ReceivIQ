"""
Section 6 Part 2: Autonomous Bedrock Tools 14 through 25.
"""

def generate_sec06_part2():
    lines = []
    def p(t=""): lines.append(t)

    tools_data = [
        ("6.14 Tool: update_invoice",
         "Modifies due date, notes, or metadata for an open invoice.",
         """{
  "name": "update_invoice",
  "description": "Modifies due date, notes, or metadata for an open invoice.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"},
      "due_date": {"type": "string"},
      "notes": {"type": "string"}
    },
    "required": ["invoice_id"]
  }
}""",
         [
             ("invoice_id", "string", "Yes", "None", "Target invoice identifier."),
             ("due_date", "string", "No", "None", "New commercial due date."),
             ("notes", "string", "No", "None", "Updated commercial notes.")
         ],
         """UPDATE invoices SET due_date = :due, notes = :notes WHERE invoice_id = :inv_id;""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1004",
  "message": "Invoice INV-1004 updated successfully."
}""",
         "Manager: 'Update due date of invoice INV-1004 to 2026-11-01.' -> Updates record."),

        ("6.15 Tool: remove_invoice",
         "Deletes an invoice only if it has not received payments and is not settled.",
         """{
  "name": "remove_invoice",
  "description": "Deletes an invoice only if it has not received payments and is not settled.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"}
    },
    "required": ["invoice_id"]
  }
}""",
         [
             ("invoice_id", "string", "Yes", "None", "Target invoice ID to delete.")
         ],
         """DELETE FROM invoices WHERE invoice_id = :inv_id;""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1099",
  "message": "Invoice INV-1099 deleted successfully."
}""",
         "Manager: 'Delete draft invoice INV-1099.' -> Deletes invoice."),

        ("6.16 Tool: create_payment_commitment",
         "Creates a time-bound early settlement discount offer or commercial payment agreement.",
         """{
  "name": "create_payment_commitment",
  "description": "Creates a time-bound early settlement discount offer or commercial payment agreement.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"},
      "commitment_type": {"type": "string"},
      "discount_percent": {"type": "number"},
      "promised_date": {"type": "string"}
    },
    "required": ["invoice_id", "commitment_type"]
  }
}""",
         [
             ("invoice_id", "string", "Yes", "None", "Target invoice ID."),
             ("commitment_type", "string", "Yes", "None", "Type of commercial agreement."),
             ("discount_percent", "number", "No", "0.0", "Discount percentage (0.1% to 0.5%)."),
             ("promised_date", "string", "No", "None", "Payment commitment deadline.")
         ],
         """INSERT INTO system_settings (category, key, value) VALUES ('commitments', :comm_id, :dumped);""",
         """{
  "status": "SUCCESS",
  "commitment_id": "COMM-001",
  "invoice_id": "INV-1004",
  "discount_percent": 0.5,
  "settlement_amount": 261187.5
}""",
         "Manager: 'Offer a 0.5% early payment discount on invoice INV-1004 valid for 24 hours.' -> Proposes discount."),

        ("6.17 Tool: update_commitment",
         "Modifies or cancels an existing commitment (Revise vs Stack vs Cancel).",
         """{
  "name": "update_commitment",
  "description": "Modifies or cancels an existing commitment (Revise vs Stack vs Cancel).",
  "parameters": {
    "type": "object",
    "properties": {
      "commitment_id": {"type": "string"},
      "action": {"type": "string", "enum": ["revise", "stack", "cancel"]}
    },
    "required": ["commitment_id", "action"]
  }
}""",
         [
             ("commitment_id", "string", "Yes", "None", "Commitment identifier."),
             ("action", "string", "Yes", "None", "Action enum: revise, stack, or cancel.")
         ],
         """UPDATE system_settings SET value = :val WHERE key = :comm_id;""",
         """{
  "status": "SUCCESS",
  "action_taken": "REVISE",
  "message": "Commitment updated successfully."
}""",
         "Manager: 'Revise the existing discount offer to 0.25%.' -> Modifies commitment."),

        ("6.18 Tool: get_active_commitments",
         "Lists all unexpired payment commitments and discount offers for an invoice.",
         """{
  "name": "get_active_commitments",
  "description": "Lists all unexpired payment commitments and discount offers for an invoice.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"}
    },
    "required": ["invoice_id"]
  }
}""",
         [
             ("invoice_id", "string", "Yes", "None", "Target invoice identifier.")
         ],
         """SELECT value FROM system_settings WHERE category = 'commitments';""",
         """{
  "active_commitments": [
    {
      "commitment_id": "COMM-001",
      "discount_percent": 0.5,
      "expires_at": "2026-10-26T12:00:00Z"
    }
  ]
}""",
         "Manager: 'Are there any active discount offers on invoice INV-1004?' -> Returns active commitments."),

        ("6.19 Tool: grant_grace_period",
         "Grants a temporary grace period extension to a debtor, freezing penalty accumulation.",
         """{
  "name": "grant_grace_period",
  "description": "Grants a temporary grace period extension to a debtor, freezing penalty accumulation.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"},
      "days": {"type": "integer"},
      "reason": {"type": "string"}
    },
    "required": ["invoice_id", "days"]
  }
}""",
         [
             ("invoice_id", "string", "Yes", "None", "Target invoice ID."),
             ("days", "integer", "Yes", "None", "Extension days (e.g. 7, 14)."),
             ("reason", "string", "No", "None", "Commercial justification for extension.")
         ],
         """UPDATE invoices SET status = 'IN_GRACE_PERIOD', grace_period_until = :until WHERE invoice_id = :inv_id;""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1005",
  "new_status": "IN_GRACE_PERIOD",
  "extension_days": 14
}""",
         "Manager: 'Grant a 14-day grace period extension to Orbit Labs on invoice INV-1005.' -> Freezes penalties."),

        ("6.20 Tool: update_customer_contact",
         "Updates contact officer name, phone, or billing email for a corporate debtor.",
         """{
  "name": "update_customer_contact",
  "description": "Updates contact officer name, phone, or billing email for a corporate debtor.",
  "parameters": {
    "type": "object",
    "properties": {
      "customer_id": {"type": "string"},
      "name": {"type": "string"},
      "email": {"type": "string"},
      "phone": {"type": "string"}
    },
    "required": ["customer_id"]
  }
}""",
         [
             ("customer_id", "string", "Yes", "None", "Customer primary key."),
             ("name", "string", "No", "None", "New contact officer name."),
             ("email", "string", "No", "None", "New billing email."),
             ("phone", "string", "No", "None", "New phone number.")
         ],
         """UPDATE customers SET name = :name, email = :email, phone = :phone WHERE customer_id = :cid;""",
         """{
  "status": "SUCCESS",
  "customer_id": "CUST-002",
  "message": "Customer contact details updated successfully."
}""",
         "Manager: 'Update contact email for Summit Logistics to accounts@summitlog.com.' -> Updates contact."),

        ("6.21 Tool: update_customer_risk_profile",
         "Adjusts debtor credit risk tier (Low, Medium, High) with formal commercial rationale.",
         """{
  "name": "update_customer_risk_profile",
  "description": "Adjusts debtor credit risk tier (Low, Medium, High) with formal commercial rationale.",
  "parameters": {
    "type": "object",
    "properties": {
      "customer_id": {"type": "string"},
      "risk_level": {"type": "string", "enum": ["Low", "Medium", "High"]},
      "reason": {"type": "string"}
    },
    "required": ["customer_id", "risk_level"]
  }
}""",
         [
             ("customer_id", "string", "Yes", "None", "Customer primary key."),
             ("risk_level", "string", "Yes", "None", "New risk tier: Low, Medium, High."),
             ("reason", "string", "No", "None", "Commercial justification for adjustment.")
         ],
         """UPDATE customers SET risk_level = :lvl WHERE customer_id = :cid;""",
         """{
  "status": "SUCCESS",
  "customer_id": "CUST-004",
  "previous_risk": "High",
  "new_risk": "Medium"
}""",
         "Manager: 'Downgrade risk tier of Helios Retail Corp to Medium.' -> Updates risk profile."),

        ("6.22 Tool: get_financial_summary",
         "Returns executive financial KPIs: Total Receivables, Total Overdue, DSO, and Collection Velocity.",
         """{
  "name": "get_financial_summary",
  "description": "Returns executive financial KPIs: Total Receivables, Total Overdue, DSO, and Collection Velocity.",
  "parameters": {
    "type": "object",
    "properties": {}
  }
}""",
         [],
         """SELECT SUM(total_amount) FROM invoices;""",
         """{
  "total_receivables": 1250000.0,
  "total_overdue": 850000.0,
  "dso_days": 38.5,
  "collection_velocity_percent": 84.2
}""",
         "Manager: 'What is our current DSO and total overdue receivables?' -> Returns KPI card."),

        ("6.23 Tool: get_audit_trail",
         "Retrieves chronological action history from the PostgreSQL agent_actions log.",
         """{
  "name": "get_audit_trail",
  "description": "Retrieves chronological action history from the PostgreSQL agent_actions log.",
  "parameters": {
    "type": "object",
    "properties": {
      "limit": {"type": "integer"},
      "action_type": {"type": "string"}
    }
  }
}""",
         [
             ("limit", "integer", "No", "50", "Maximum audit events to return."),
             ("action_type", "string", "No", "ALL", "Filter by specific event type.")
         ],
         """SELECT * FROM agent_actions ORDER BY created_at DESC LIMIT :lim;""",
         """{
  "total_actions": 50,
  "actions": [
    {
      "action_id": "ACT-1024",
      "action_type": "EMAIL_SENT",
      "timestamp": "2026-10-25T07:43:00+05:30"
    }
  ]
}""",
         "Manager: 'Show recent agent activity log.' -> Returns audit feed."),

        ("6.24 Tool: get_system_settings",
         "Retrieves active business policy parameters: penalty rates, grace days, bank remittance coordinates.",
         """{
  "name": "get_system_settings",
  "description": "Retrieves active business policy parameters: penalty rates, grace days, bank remittance coordinates.",
  "parameters": {
    "type": "object",
    "properties": {}
  }
}""",
         [],
         """SELECT * FROM system_settings;""",
         """{
  "penalty_rate_percent": 2.0,
  "penalty_days_cycle": 30,
  "bank_beneficiary": "Treasury Department",
  "bank_account": "123456789012",
  "bank_ifsc": "SBIN0001234"
}""",
         "Manager: 'Show current bank remittance settings and late penalty rate.' -> Returns settings."),

        ("6.25 Tool: update_system_setting",
         "Modifies a system configuration parameter in PostgreSQL.",
         """{
  "name": "update_system_setting",
  "description": "Modifies a system configuration parameter in PostgreSQL.",
  "parameters": {
    "type": "object",
    "properties": {
      "category": {"type": "string"},
      "key": {"type": "string"},
      "value": {"type": "string"}
    },
    "required": ["category", "key", "value"]
  }
}""",
         [
             ("category", "string", "Yes", "None", "Setting domain category (penalty, reminders, bank)."),
             ("key", "string", "Yes", "None", "Parameter configuration key."),
             ("value", "string", "Yes", "None", "New stringified value.")
         ],
         """UPDATE system_settings SET value = :val WHERE category = :cat AND key = :key;""",
         """{
  "status": "SUCCESS",
  "category": "penalty",
  "key": "rate",
  "new_value": "2.5"
}""",
         "Manager: 'Update penalty rate to 2.5% in system settings.' -> Reconfigures parameter.")
    ]

    for t_name, t_desc, t_schema, t_params, t_sql, t_ret, t_ex in tools_data:
        p(f"### {t_name}")
        p(f"**Operational Responsibility:** {t_desc}")
        p("")
        if t_params:
            p("#### Parameter Specification")
            p("| Parameter | Type | Required | Default | Description |")
            p("| :--- | :--- | :--- | :--- | :--- |")
            for p_name, p_type, p_req, p_def, p_desc in t_params:
                p(f"| `{p_name}` | `{p_type}` | {p_req} | `{p_def}` | {p_desc} |")
            p("")
        p("#### AWS Bedrock Tool Specification (JSON Schema)")
        p("```json")
        p(t_schema)
        p("```")
        p("")
        p("#### Relational Query Executed")
        p("```sql")
        p(t_sql)
        p("```")
        p("")
        p("#### Structured Return Payload")
        p("```json")
        p(t_ret)
        p("```")
        p("")
        p(f"- **Conversational Interaction Example:** *\"{t_ex}\"*")
        p("")
        p("---")
        p("")

    return lines
