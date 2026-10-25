"""
Section 6 Part 1: Autonomous Bedrock Tools 1 through 13.
"""

def generate_sec06_part1():
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
         [
             ("min_days", "integer", "No", "0", "Filters for invoices overdue by at least this many calendar days."),
             ("risk_level", "string", "No", "ALL", "Restricts results to customers within the specified credit risk tier."),
             ("customer_id", "string", "No", "None", "Optional filter to target a single corporate debtor account.")
         ],
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
         [
             ("invoice_id", "string", "Yes", "None", "Primary key identifier or invoice number (e.g. INV-1004).")
         ],
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
         [
             ("customer_id", "string", "Yes", "None", "Debtor customer ID, company name, or billing email.")
         ],
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
         [
             ("invoice_id", "string", "Yes", "None", "Invoice target identifier."),
             ("reminder_level", "integer", "No", "1", "Cadence notice number: 1 (initial), 2 (firm), 3 (final)."),
             ("tone", "string", "No", "polite", "Tone profile: polite, firm, or urgent.")
         ],
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
         [
             ("invoice_id", "string", "Yes", "None", "Target invoice identifier."),
             ("subject", "string", "Yes", "None", "Email subject header."),
             ("body", "string", "Yes", "None", "Sanitized email body text."),
             ("recipient", "string", "No", "customer.email", "Target recipient email address.")
         ],
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
         [
             ("invoice_id", "string", "Yes", "None", "Target invoice identifier."),
             ("reason", "string", "Yes", "None", "Commercial justification for escalation.")
         ],
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
         [
             ("invoice_id", "string", "Yes", "None", "Target invoice identifier."),
             ("amount", "number", "Yes", "None", "Remitted payment amount in INR."),
             ("payment_method", "string", "No", "NEFT", "Payment method: NEFT, RTGS, IMPS, Cheque."),
             ("reference_number", "string", "No", "None", "Bank UTR or transaction reference number.")
         ],
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
         [
             ("invoice_id", "string", "Yes", "None", "Target invoice identifier."),
             ("new_status", "string", "Yes", "None", "Target status enum."),
             ("reason", "string", "No", "None", "Optional reason or commercial notes.")
         ],
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
         [
             ("name", "string", "Yes", "None", "Primary contact officer name."),
             ("company_name", "string", "Yes", "None", "Debtor company legal entity name."),
             ("email", "string", "Yes", "None", "Corporate billing email address."),
             ("phone", "string", "No", "None", "Direct telephone contact."),
             ("address", "string", "No", "None", "Registered corporate address."),
             ("risk_level", "string", "No", "Low", "Credit risk tier: Low, Medium, High.")
         ],
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
         [
             ("search", "string", "No", "None", "Keyword filter matching company name or contact."),
             ("risk_level", "string", "No", "ALL", "Restricts results by risk tier."),
             ("limit", "integer", "No", "50", "Maximum customer records returned.")
         ],
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
         [
             ("customer_id", "string", "Yes", "None", "Target customer ID to delete.")
         ],
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
         [
             ("customer_id", "string", "Yes", "None", "Debtor customer ID."),
             ("amount", "number", "Yes", "None", "Principal amount in INR."),
             ("due_date", "string", "Yes", "None", "Commercial due date (YYYY-MM-DD)."),
             ("notes", "string", "No", "None", "Invoice notes or line-item description.")
         ],
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
         [
             ("status", "string", "No", "ALL", "Filter by status: PENDING, OVERDUE, PAID, DISPUTED."),
             ("customer_id", "string", "No", "None", "Filter by debtor customer ID."),
             ("limit", "integer", "No", "50", "Max records returned.")
         ],
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
         "Manager: 'List all open overdue invoices.' -> Returns invoice table.")
    ]

    for t_name, t_desc, t_schema, t_params, t_sql, t_ret, t_ex in tools_data:
        p(f"### {t_name}")
        p(f"**Operational Responsibility:** {t_desc}")
        p("")
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
