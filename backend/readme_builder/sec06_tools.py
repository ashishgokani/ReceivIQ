"""
Section 6: Comprehensive Deep-Dive Catalog of All 25 Autonomous Bedrock Tools.
"""

def generate_sec06():
    lines = []
    def p(t=""): lines.append(t)

    p("## 6. Deep-Dive Catalog of All 25 Autonomous Bedrock Tools")
    p("")
    p("Amazon Nova Pro operates through 25 specialized, strictly typed autonomous tools. Each tool is cataloged below with parameter breakdown tables, JSON schemas, return payloads, SQL queries executed, error handling, and prompt transcripts:")
    p("")

    tools_data = [
        ("6.1 Tool: get_overdue_invoices",
         "Queries overdue invoices filtered by minimum days overdue, credit risk tier, or specific customer ID.",
         """{
  "name": "get_overdue_invoices",
  "description": "Queries overdue invoices filtered by aging threshold, risk tier, or debtor ID.",
  "parameters": {
    "type": "object",
    "properties": {
      "min_days": {"type": "integer", "description": "Minimum days overdue."},
      "risk_level": {"type": "string", "enum": ["Low", "Medium", "High"]},
      "customer_id": {"type": "string", "description": "Debtor ID."}
    }
  }
}""",
         """SELECT i.invoice_id, i.invoice_number, i.customer_id, c.company_name, c.name as contact_name,
       i.amount, i.due_date, i.status, i.reminder_count
FROM invoices i
JOIN customers c ON i.customer_id = c.customer_id
WHERE i.status = 'OVERDUE' AND (CURRENT_DATE - i.due_date) >= :min_days
ORDER BY (CURRENT_DATE - i.due_date) DESC;""",
         """{
  "total_count": 3,
  "invoices": [
    {
      "invoice_id": "INV-1004",
      "invoice_number": "INV-2026-1004",
      "customer_id": "CUST-004",
      "customer_name": "Updated Contact Officer",
      "company_name": "Helios Retail Corp",
      "amount": 250000.0,
      "penalty_amount": 12500.0,
      "total_amount": 262500.0,
      "days_overdue": 21,
      "status": "OVERDUE",
      "reminder_count": 2
    }
  ]
}""",
         "Manager: 'Show me all overdue accounts past 15 days.' -> Returns Markdown table."),

        ("6.2 Tool: get_invoice_details",
         "Retrieves complete financial balance, reminder history, and dispute details for a single invoice.",
         """{
  "name": "get_invoice_details",
  "description": "Fetches complete financial balance, payment record, and dispute status for a single invoice.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string", "description": "Invoice ID or serial number."}
    },
    "required": ["invoice_id"]
  }
}""",
         """SELECT i.*, c.company_name, c.email, c.phone, c.risk_level
FROM invoices i
JOIN customers c ON i.customer_id = c.customer_id
WHERE i.invoice_id = :invoice_id;""",
         """{
  "invoice_id": "INV-1004",
  "invoice_number": "INV-2026-1004",
  "customer_id": "CUST-004",
  "company_name": "Helios Retail Corp",
  "contact_name": "Updated Contact Officer",
  "amount": 250000.0,
  "penalty_amount": 12500.0,
  "total_amount": 262500.0,
  "due_date": "2026-10-04",
  "status": "OVERDUE",
  "reminder_count": 2,
  "dispute_reason": null
}""",
         "Manager: 'What is the balance and dispute status on INV-1004?' -> Returns detailed metadata block."),

        ("6.3 Tool: get_customer_history",
         "Retrieves debtor background, historical payment track record, credit risk tier, and outstanding balance summary.",
         """{
  "name": "get_customer_history",
  "description": "Retrieves debtor payment track record, credit risk tier, and outstanding balance summary.",
  "parameters": {
    "type": "object",
    "properties": {
      "customer_id": {"type": "string", "description": "Customer ID, company name, or email."}
    },
    "required": ["customer_id"]
  }
}""",
         """SELECT * FROM customers WHERE customer_id = :cid OR company_name ILIKE :search;""",
         """{
  "customer_id": "CUST-002",
  "company_name": "Summit Logistics",
  "name": "Aditya Verma",
  "email": "ap@summitlog.com",
  "risk_level": "Medium",
  "total_invoices": 8,
  "paid_invoices": 6,
  "overdue_invoices": 2,
  "total_outstanding": 315000.0
}""",
         "Manager: 'Check customer track record for Summit Logistics.' -> Returns complete profile."),

        ("6.4 Tool: draft_reminder_email",
         "Generates a contextual, tiered payment reminder email equipped with live bank remittance instructions.",
         """{
  "name": "draft_reminder_email",
  "description": "Composes a contextual, tiered payment reminder email equipped with live bank remittance instructions.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"},
      "reminder_level": {"type": "integer"},
      "tone": {"type": "string", "enum": ["polite", "firm", "urgent"]}
    },
    "required": ["invoice_id"]
  }
}""",
         """SELECT * FROM system_settings WHERE category IN ('bank', 'reminders');""",
         """{
  "subject": "Second Notice: Overdue Invoice INV-PAID-D3D42C - Aether Media Networks",
  "body": "Dear Updated Contact Officer,\\n\\nWe are following up regarding outstanding Invoice INV-PAID-D3D42C for INR 1,57,500.00...\\n\\nBank Remittance Details:\\nBeneficiary: Treasury Department\\nBank: State Bank of India\\nAccount: 123456789012\\nIFSC: SBIN0001234\\n\\nWarm regards,\\nAccounts Receivable Team\\nReceivIQ"
}""",
         "Manager: 'Draft a firm reminder email for invoice INV-PAID-D3D42C.' -> Displays preview draft."),

        ("6.5 Tool: send_email",
         "Dispatches a validated email via SMTP, increments reminder counters, and verifies human governance.",
         """{
  "name": "send_email",
  "description": "Dispatches a validated email via SMTP, increments reminder counters, and verifies human governance.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"},
      "subject": {"type": "string"},
      "body": {"type": "string"},
      "recipient": {"type": "string"}
    },
    "required": ["invoice_id", "subject", "body"]
  }
}""",
         """UPDATE invoices SET reminder_count = reminder_count + 1, last_reminder_at = CURRENT_TIMESTAMP WHERE invoice_id = :inv_id;
INSERT INTO communications (communication_id, customer_id, invoice_id, direction, subject, body, delivery_status) VALUES (...);""",
         """{
  "status": "SENT",
  "invoice_id": "INV-1008",
  "reminder_count": 2,
  "delivery_details": {
    "recipient_email": "billing@pinnacle.health",
    "real_smtp_dispatched": true
  }
}""",
         "Manager: 'Yes, confirm and send the reminder email.' -> Dispatches via SMTP."),

        ("6.6 Tool: create_escalation",
         "Formally escalates delinquent debt to senior finance management or legal counsel.",
         """{
  "name": "create_escalation",
  "description": "Formally escalates delinquent debt to senior finance management or legal counsel.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"},
      "reason": {"type": "string"}
    },
    "required": ["invoice_id", "reason"]
  }
}""",
         """INSERT INTO approvals (approval_id, invoice_id, action_type, reason, status) VALUES (:app_id, :inv_id, 'ESCALATE', :reason, 'PENDING');""",
         """{
  "status": "PENDING_APPROVAL",
  "approval_id": "APP-9A8B7C",
  "message": "Formal legal escalation ticket created for administrator review."
}""",
         "Manager: 'Escalate invoice INV-1004 for legal action due to ignored notices.' -> Queues ticket."),

        ("6.7 Tool: record_payment",
         "Records full or partial payment against an invoice, adjusting balances and locking settled records.",
         """{
  "name": "record_payment",
  "description": "Records full or partial payment against an invoice, adjusting balances and locking settled records.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"},
      "amount": {"type": "number"},
      "payment_method": {"type": "string"},
      "reference_number": {"type": "string"}
    },
    "required": ["invoice_id", "amount"]
  }
}""",
         """INSERT INTO payments (payment_id, invoice_id, amount_paid, payment_date, payment_method, reference_number) VALUES (...);
UPDATE invoices SET status = 'PAID', total_amount = 0.00 WHERE invoice_id = :inv_id;""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1004",
  "amount_paid": 262500.0,
  "new_status": "PAID",
  "message": "Payment recorded successfully. Invoice marked PAID and permanently locked."
}""",
         "Manager: 'Record payment of 262500 for INV-1004 with reference SBIN00928374.' -> Settles invoice."),

        ("6.8 Tool: update_invoice_status",
         "Updates invoice status (e.g. to DISPUTED, IN_GRACE_PERIOD, or PENDING).",
         """{
  "name": "update_invoice_status",
  "description": "Updates invoice status (e.g. to DISPUTED, IN_GRACE_PERIOD, or PENDING).",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": {"type": "string"},
      "new_status": {"type": "string"},
      "reason": {"type": "string"}
    },
    "required": ["invoice_id", "new_status"]
  }
}""",
         """UPDATE invoices SET status = :new_status, dispute_reason = :reason WHERE invoice_id = :inv_id;""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1005",
  "previous_status": "OVERDUE",
  "new_status": "DISPUTED"
}""",
         "Manager: 'Mark invoice INV-1005 as disputed.' -> Freezes reminders."),

        ("6.9 Tool: create_customer",
         "Onboards a new corporate debtor into the directory with initial credit risk tier.",
         """{
  "name": "create_customer",
  "description": "Onboards a new corporate debtor into the directory with initial credit risk tier.",
  "parameters": {
    "type": "object",
    "properties": {
      "name": {"type": "string"},
      "company_name": {"type": "string"},
      "email": {"type": "string"},
      "phone": {"type": "string"},
      "address": {"type": "string"},
      "risk_level": {"type": "string"}
    },
    "required": ["name", "company_name", "email"]
  }
}""",
         """INSERT INTO customers (customer_id, name, company_name, email, phone, address, risk_level) VALUES (...);""",
         """{
  "status": "SUCCESS",
  "customer_id": "CUST-104",
  "message": "Customer Nexus Dynamics onboarded successfully."
}""",
         "Manager: 'Onboard customer Nexus Dynamics with email billing@nexusdyn.com.' -> Creates profile."),

        ("6.10 Tool: list_customers",
         "Lists debtor directory profiles with keyword search, risk tier filtering, and totals.",
         """{
  "name": "list_customers",
  "description": "Lists debtor directory profiles with keyword search, risk tier filtering, and totals.",
  "parameters": {
    "type": "object",
    "properties": {
      "search": {"type": "string"},
      "risk_level": {"type": "string"},
      "limit": {"type": "integer"}
    }
  }
}""",
         """SELECT * FROM customers WHERE company_name ILIKE :q OR name ILIKE :q LIMIT :lim;""",
         """{
  "total_customers": 1,
  "customers": [
    {
      "customer_id": "CUST-004",
      "company_name": "Helios Retail Corp",
      "contact_name": "Updated Contact Officer",
      "risk_level": "High"
    }
  ]
}""",
         "Manager: 'How many total customers do we have?' -> Returns summary counts."),

        ("6.11 Tool: remove_customer",
         "Removes a customer profile if they have zero active or unsettled invoices.",
         """{
  "name": "remove_customer",
  "description": "Removes a customer profile if they have zero active or unsettled invoices.",
  "parameters": {
    "type": "object",
    "properties": {
      "customer_id": {"type": "string"}
    },
    "required": ["customer_id"]
  }
}""",
         """DELETE FROM customers WHERE customer_id = :cid;""",
         """{
  "status": "SUCCESS",
  "customer_id": "CUST-099",
  "message": "Customer CUST-099 removed successfully."
}""",
         "Manager: 'Delete customer record CUST-099.' -> Deletes inactive debtor."),

        ("6.12 Tool: create_invoice",
         "Issues a new invoice with line items, due date, and initial principal amount.",
         """{
  "name": "create_invoice",
  "description": "Issues a new invoice with line items, due date, and initial principal amount.",
  "parameters": {
    "type": "object",
    "properties": {
      "customer_id": {"type": "string"},
      "amount": {"type": "number"},
      "due_date": {"type": "string"},
      "notes": {"type": "string"}
    },
    "required": ["customer_id", "amount", "due_date"]
  }
}""",
         """INSERT INTO invoices (invoice_id, customer_id, invoice_number, invoice_date, due_date, amount, total_amount, status) VALUES (...);""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1099",
  "message": "Invoice INV-1099 created successfully."
}""",
         "Manager: 'Create an invoice for customer CUST-002 for ₹1,50,000 due on 2026-11-15.' -> Issues invoice."),

        ("6.13 Tool: list_invoices",
         "Lists all ledger invoices with filtering across status, overdue days, and pagination.",
         """{
  "name": "list_invoices",
  "description": "Lists all ledger invoices with filtering across status, overdue days, and pagination.",
  "parameters": {
    "type": "object",
    "properties": {
      "status": {"type": "string"},
      "customer_id": {"type": "string"},
      "limit": {"type": "integer"}
    }
  }
}""",
         """SELECT * FROM invoices WHERE status = :status ORDER BY due_date ASC LIMIT :lim;""",
         """{
  "total_invoices": 12,
  "invoices": [
    {
      "invoice_id": "INV-1004",
      "amount": 250000.0,
      "status": "OVERDUE"
    }
  ]
}""",
         "Manager: 'List all open overdue invoices.' -> Returns invoice table."),

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
         """UPDATE system_settings SET value = :val WHERE category = :cat AND key = :key;""",
         """{
  "status": "SUCCESS",
  "category": "penalty",
  "key": "rate",
  "new_value": "2.5"
}""",
         "Manager: 'Update penalty rate to 2.5% in system settings.' -> Reconfigures parameter.")
    ]

    for t_name, t_desc, t_schema, t_sql, t_ret, t_ex in tools_data:
        p(f"### {t_name}")
        p(f"**Operational Responsibility:** {t_desc}")
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
