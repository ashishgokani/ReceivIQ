"""
Section 6 through 8: All 25 Bedrock Tools, 15 Operational Mandates, and Sequence Workflows.
"""

def generate_sec06_08():
    lines = []
    def p(t=""): lines.append(t)

    # SECTION 6: ALL 25 TOOLS
    p("## 6. Deep-Dive Catalog of All 25 Autonomous Bedrock Tools")
    p("")
    p("Amazon Nova Pro operates through 25 specialized, strictly typed autonomous tools. Each tool is cataloged below with exact JSON parameter schemas, return types, SQL mutations, and prompt invocation examples:")
    p("")

    all_25_tools = [
        ("1. get_overdue_invoices",
         "Queries overdue invoices filtered by aging threshold, risk tier, or debtor ID.",
         """{"type": "object", "properties": {"min_days": {"type": "integer", "description": "Minimum days overdue."}, "risk_level": {"type": "string", "enum": ["Low", "Medium", "High"]}, "customer_id": {"type": "string"}}}""",
         """{"total_count": 3, "invoices": [{"invoice_id": "INV-1004", "customer_name": "Helios Retail Corp", "amount": 250000.0, "penalty_amount": 12500.0, "total_amount": 262500.0, "days_overdue": 21, "status": "OVERDUE"}]}""",
         "Queries `invoices` joined with `customers`; synchronizes accrued late penalties dynamically.",
         "Show all overdue accounts past 15 days."),

        ("2. get_invoice_details",
         "Fetches complete financial balance, payment record, and dispute status for a single invoice.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}}, "required": ["invoice_id"]}""",
         """{"invoice_id": "INV-1004", "invoice_number": "INV-2026-1004", "customer_id": "CUST-004", "company_name": "Helios Retail Corp", "amount": 250000.0, "penalty_amount": 12500.0, "total_amount": 262500.0, "status": "OVERDUE", "due_date": "2026-10-04"}""",
         "Reads `invoices` table and syncs penalty interest.",
         "What is the status and outstanding balance on INV-1004?"),

        ("3. get_customer_history",
         "Retrieves debtor payment track record, credit risk tier, and outstanding balance summary.",
         """{"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]}""",
         """{"customer_id": "CUST-002", "company_name": "Summit Logistics", "name": "Aditya Verma", "risk_level": "Medium", "total_invoices": 8, "paid_invoices": 6, "overdue_invoices": 2, "total_outstanding": 315000.0}""",
         "Queries `customers` with case-insensitive search across company and contact name.",
         "Check customer track record for Summit Logistics."),

        ("4. draft_reminder_email",
         "Composes a contextual, tiered payment reminder email equipped with live bank remittance instructions.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}, "reminder_level": {"type": "integer"}, "tone": {"type": "string", "enum": ["polite", "firm", "urgent"]}}, "required": ["invoice_id"]}""",
         """{"subject": "Second Notice: Overdue Invoice INV-PAID-D3D42C - Aether Media Networks", "body": "Dear Updated Contact Officer,\\n\\nWe are following up regarding outstanding Invoice INV-PAID-D3D42C...\\n\\nBank Remittance Details:\\nBeneficiary: Treasury Department\\nBank: State Bank of India\\nAccount: 123456789012\\nIFSC: SBIN0001234\\n\\nWarm regards,\\nAccounts Receivable Team\\nReceivIQ"}""",
         "Invokes `AIEmailDrafter`, sanitizes placeholders via regex, prepares draft for chat preview.",
         "Draft a firm reminder email for invoice INV-PAID-D3D42C."),

        ("5. send_email",
         "Dispatches a validated email via SMTP, increments reminder counters, and verifies human governance.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}, "recipient": {"type": "string"}}, "required": ["invoice_id", "subject", "body"]}""",
         """{"status": "SENT", "invoice_id": "INV-1008", "reminder_count": 2, "delivery_details": {"recipient_email": "billing@pinnacle.health", "real_smtp_dispatched": true}}""",
         "Checks human approval threshold, dispatches via `EmailService`, increments `reminder_count`, logs `agent_actions` and `communications`.",
         "Confirm and send the drafted reminder email."),

        ("6. create_escalation",
         "Formally escalates delinquent debt to senior finance management or legal counsel.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}, "reason": {"type": "string"}}, "required": ["invoice_id", "reason"]}""",
         """{"status": "PENDING_APPROVAL", "approval_id": "APP-9A8B7C", "message": "Formal legal escalation ticket created for administrator review."}""",
         "Inserts `approvals` ticket with action `ESCALATE`.",
         "Escalate invoice INV-1004 for legal action due to ignored notices."),

        ("7. record_payment",
         "Records full or partial payment against an invoice, adjusting balances and locking settled records.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}, "amount": {"type": "number"}, "payment_method": {"type": "string"}, "reference_number": {"type": "string"}}, "required": ["invoice_id", "amount"]}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1004", "amount_paid": 262500.0, "new_status": "PAID", "message": "Payment recorded successfully. Invoice marked PAID and permanently locked."}""",
         "Inserts `payments` record, updates `invoices.status = 'PAID'`, zeroes `invoices.total_amount`, logs `agent_actions`.",
         "Record payment of 262500 for INV-1004 with reference SBIN00928374."),

        ("8. update_invoice_status",
         "Updates invoice status (e.g. to DISPUTED, IN_GRACE_PERIOD, or PENDING).",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}, "new_status": {"type": "string"}, "reason": {"type": "string"}}, "required": ["invoice_id", "new_status"]}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1005", "previous_status": "OVERDUE", "new_status": "DISPUTED"}""",
         "Updates `invoices.status` and `invoices.dispute_reason` in PostgreSQL.",
         "Mark invoice INV-1005 as disputed due to damaged deliverables."),

        ("9. create_customer",
         "Onboards a new corporate debtor into the directory with initial credit risk tier.",
         """{"type": "object", "properties": {"name": {"type": "string"}, "company_name": {"type": "string"}, "email": {"type": "string"}, "phone": {"type": "string"}, "address": {"type": "string"}, "risk_level": {"type": "string"}}, "required": ["name", "company_name", "email"]}""",
         """{"status": "SUCCESS", "customer_id": "CUST-104", "message": "Customer Nexus Dynamics onboarded successfully."}""",
         "Inserts new `Customer` record into PostgreSQL.",
         "Onboard customer Nexus Dynamics with email billing@nexusdyn.com."),

        ("10. list_customers",
         "Lists debtor directory profiles with keyword search, risk tier filtering, and totals.",
         """{"type": "object", "properties": {"search": {"type": "string"}, "risk_level": {"type": "string"}, "limit": {"type": "integer"}}}""",
         """{"total_customers": 1, "customers": [{"customer_id": "CUST-004", "company_name": "Helios Retail Corp", "contact_name": "Updated Contact Officer", "risk_level": "High"}]}""",
         "Queries `customers` table with ILIKE search across company and contact name.",
         "How many total customers do we have?"),

        ("11. remove_customer",
         "Removes a customer profile if they have zero active or unsettled invoices.",
         """{"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]}""",
         """{"status": "SUCCESS", "customer_id": "CUST-099", "message": "Customer CUST-099 removed successfully."}""",
         "Deletes `customers` record after verifying zero associated invoices.",
         "Delete customer record CUST-099."),

        ("12. create_invoice",
         "Issues a new invoice with line items, due date, and initial principal amount.",
         """{"type": "object", "properties": {"customer_id": {"type": "string"}, "amount": {"type": "number"}, "due_date": {"type": "string"}, "notes": {"type": "string"}}, "required": ["customer_id", "amount", "due_date"]}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1099", "message": "Invoice INV-1099 created successfully."}""",
         "Inserts new `Invoice` record into PostgreSQL, updates debtor outstanding total.",
         "Create an invoice for customer CUST-002 for ₹1,50,000 due on 2026-11-15."),

        ("13. list_invoices",
         "Lists all ledger invoices with filtering across status, overdue days, and pagination.",
         """{"type": "object", "properties": {"status": {"type": "string"}, "customer_id": {"type": "string"}, "limit": {"type": "integer"}}}""",
         """{"total_invoices": 12, "invoices": [{"invoice_id": "INV-1004", "amount": 250000.0, "status": "OVERDUE"}]}""",
         "Queries `invoices` table with dynamic penalty synchronization.",
         "List all open overdue invoices."),

        ("14. update_invoice",
         "Modifies due date, notes, or metadata for an open invoice.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}, "due_date": {"type": "string"}, "notes": {"type": "string"}}, "required": ["invoice_id"]}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1004", "message": "Invoice INV-1004 updated successfully."}""",
         "Updates `invoices` fields; re-evaluates overdue status.",
         "Update due date of invoice INV-1004 to 2026-11-01."),

        ("15. remove_invoice",
         "Deletes an invoice only if it has not received payments and is not settled.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}}, "required": ["invoice_id"]}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1099", "message": "Invoice INV-1099 deleted successfully."}""",
         "Deletes `Invoice` record from PostgreSQL; updates customer balance.",
         "Delete draft invoice INV-1099."),

        ("16. create_payment_commitment",
         "Creates a time-bound early settlement discount offer or commercial payment agreement.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}, "commitment_type": {"type": "string"}, "discount_percent": {"type": "number"}, "promised_date": {"type": "string"}}, "required": ["invoice_id", "commitment_type"]}""",
         """{"status": "SUCCESS", "commitment_id": "COMM-001", "invoice_id": "INV-1004", "discount_percent": 0.5, "settlement_amount": 261187.5}""",
         "Applies discount to invoice, establishes expiry timestamp, logs commitment.",
         "Offer a 0.5% early payment discount on invoice INV-1004 valid for 24 hours."),

        ("17. update_commitment",
         "Modifies or cancels an existing commitment (Revise vs Stack vs Cancel).",
         """{"type": "object", "properties": {"commitment_id": {"type": "string"}, "action": {"type": "string", "enum": ["revise", "stack", "cancel"]}}, "required": ["commitment_id", "action"]}""",
         """{"status": "SUCCESS", "action_taken": "REVISE", "message": "Commitment updated successfully."}""",
         "Updates commitment record; recalculates discounted settlement balance.",
         "Revise the existing discount offer to 0.25%."),

        ("18. get_active_commitments",
         "Lists all unexpired payment commitments and discount offers for an invoice.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}}, "required": ["invoice_id"]}""",
         """{"active_commitments": [{"commitment_id": "COMM-001", "discount_percent": 0.5, "expires_at": "2026-10-26T12:00:00Z"}]}""",
         "Queries active commitments where `expires_at > current_time`.",
         "Are there any active discount offers on invoice INV-1004?"),

        ("19. grant_grace_period",
         "Grants a temporary grace period extension to a debtor, freezing penalty accumulation.",
         """{"type": "object", "properties": {"invoice_id": {"type": "string"}, "days": {"type": "integer"}, "reason": {"type": "string"}}, "required": ["invoice_id", "days"]}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1005", "new_status": "IN_GRACE_PERIOD", "extension_days": 14}""",
         "Updates `invoices.status = 'IN_GRACE_PERIOD'` and sets grace expiry date.",
         "Grant a 14-day grace period extension to Orbit Labs on invoice INV-1005."),

        ("20. update_customer_contact",
         "Updates contact officer name, phone, or billing email for a corporate debtor.",
         """{"type": "object", "properties": {"customer_id": {"type": "string"}, "name": {"type": "string"}, "email": {"type": "string"}, "phone": {"type": "string"}}, "required": ["customer_id"]}""",
         """{"status": "SUCCESS", "customer_id": "CUST-002", "message": "Customer contact details updated successfully."}""",
         "Updates `customers` record in PostgreSQL.",
         "Update contact email for Summit Logistics to accounts@summitlog.com."),

        ("21. update_customer_risk_profile",
         "Adjusts debtor credit risk tier (Low, Medium, High) with formal commercial rationale.",
         """{"type": "object", "properties": {"customer_id": {"type": "string"}, "risk_level": {"type": "string", "enum": ["Low", "Medium", "High"]}, "reason": {"type": "string"}}, "required": ["customer_id", "risk_level"]}""",
         """{"status": "SUCCESS", "customer_id": "CUST-004", "previous_risk": "High", "new_risk": "Medium"}""",
         "Updates `customers.risk_level` and logs risk audit event.",
         "Downgrade risk tier of Helios Retail Corp to Medium."),

        ("22. get_financial_summary",
         "Returns executive financial KPIs: Total Receivables, Total Overdue, DSO, and Collection Velocity.",
         """{"type": "object", "properties": {}}""",
         """{"total_receivables": 1250000.0, "total_overdue": 850000.0, "dso_days": 38.5, "collection_velocity_percent": 84.2}""",
         "Queries `AnalyticsService` for real-time aggregated metrics.",
         "What is our current DSO and total overdue receivables?"),

        ("23. get_audit_trail",
         "Retrieves chronological action history from the PostgreSQL `agent_actions` log.",
         """{"type": "object", "properties": {"limit": {"type": "integer"}, "action_type": {"type": "string"}}}""",
         """{"total_actions": 50, "actions": [{"action_id": "ACT-1024", "action_type": "EMAIL_SENT", "timestamp": "2026-10-25T07:43:00+05:30"}]}""",
         "Queries `agent_actions` table ordered by timestamp descending.",
         "Show recent agent activity log."),

        ("24. get_system_settings",
         "Retrieves active business policy parameters: penalty rates, grace days, bank remittance coordinates.",
         """{"type": "object", "properties": {}}""",
         """{"penalty_rate_percent": 2.0, "penalty_days_cycle": 30, "bank_beneficiary": "Treasury Department", "bank_account": "123456789012", "bank_ifsc": "SBIN0001234"}""",
         "Queries `system_settings` table via `SettingsService`.",
         "Show current bank remittance settings and late penalty rate."),

        ("25. update_system_setting",
         "Modifies a system configuration parameter in PostgreSQL.",
         """{"type": "object", "properties": {"category": {"type": "string"}, "key": {"type": "string"}, "value": {"type": "string"}}, "required": ["category", "key", "value"]}""",
         """{"status": "SUCCESS", "category": "penalty", "key": "rate", "new_value": "2.5"}""",
         "Updates `system_settings` and hot-reloads runtime cache.",
         "Update penalty rate to 2.5% in system settings.")
    ]

    for t_name, t_desc, t_in, t_out, t_db, t_ex in all_25_tools:
        p(f"### {t_name}")
        p(f"- **Purpose:** {t_desc}")
        p(f"- **Input Schema:** `{t_in}`")
        p(f"- **Output Schema:** `{t_out}`")
        p(f"- **Database Mutations:** {t_db}")
        p(f"- **Natural Language Query Example:** *\"{t_ex}\"*")
        p("")

    p("---")
    p("")

    # SECTION 7: 15 OPERATIONAL MANDATES
    p("## 7. System Prompts, 15 Operational Mandates, & Safety Guardrails")
    p("")
    p("The Amazon Nova Pro reasoning engine is strictly constrained by 15 Operational Mandates embedded within `agent_prompts.py`:")
    p("")

    mandates = [
        ("Mandate 1: Live Real-Time Data Sourcing",
         "Never invent or assume invoice IDs, customer names, or balances. Always query live PostgreSQL records using tools (`get_overdue_invoices`, `get_invoice_details`)."),
        ("Mandate 2: Dynamic Late Penalty Invariant",
         "Always calculate late penalties on principal balance at 2.0% per 30-day cycle. Never quote gross balances without separating principal and accrued penalties."),
        ("Mandate 3: Absolute Immutability on Settled Debt",
         "Invoices marked PAID are strictly locked against recalculations, status changes, or reminder dispatches. Any attempt to modify settled debt must be politely rejected."),
        ("Mandate 4: Human-in-the-Loop High-Value Gate",
         "Any invoice exceeding ₹1,00,000 cannot have a collection reminder sent without prior administrator confirmation or approval queue sign-off."),
        ("Mandate 5: Legal Escalation Gating",
         "Threatening legal action, filing insolvency notices, or assigning debt to attorneys requires explicit human approval via `create_escalation`."),
        ("Mandate 6: Time-Bound Commercial Settlement Guardrails",
         "Early settlement discounts must be mathematically bounded between 0.1% and 0.5%, with explicit expiry deadlines (e.g. 24 hours)."),
        ("Mandate 7: Multi-Commitment Conflict Resolution",
         "If an active discount offer already exists on an invoice, never overwrite silently. Present the user with Option 1 (Revise), Option 2 (Stack), or Option 3 (Cancel)."),
        ("Mandate 8: Grace Period Freezes",
         "During an approved grace period, penalty accumulation is frozen and collection reminders are suspended."),
        ("Mandate 9: Dispute Action Freezing",
         "When an invoice is marked DISPUTED, all automated collection communications must cease immediately pending commercial resolution."),
        ("Mandate 10: Fail-Closed Tool Execution Rule",
         "When a user confirms an action (e.g., 'Yes, send it'), you MUST call the appropriate tool (`send_email`, `record_payment`). Never claim an action occurred without executing the tool."),
        ("Mandate 11: Currency Formatting Standards",
         "All monetary amounts must be formatted in Indian Rupees with comma separators (e.g. ₹1,50,000 or ₹2,62,500). Interpret 'Lakh' as 100,000 and 'Crore' as 10,000,000."),
        ("Mandate 12: Bank Remittance Details Mandate",
         "Every drafted reminder email must include complete bank remittance coordinates: Beneficiary Legal Entity, Bank Name, Account Number, and IFSC Code."),
        ("Mandate 13: Zero-Placeholder Guarantee",
         "Never output placeholders like `[Your Name]`, `[Your Company Name]`, or `[Title]`. Sign all communications as 'Accounts Receivable Team' and 'ReceivIQ'."),
        ("Mandate 14: Debtor Customer Identity Verification",
         "Incoming debtor emails must be authenticated against registered customer email records. Reject unknown senders immediately to prevent data leakage."),
        ("Mandate 15: Background Turn Resilience",
         "Long-running reasoning and tool execution must proceed asynchronously on the server. If the user navigates between browser tabs, the state and thought process must remain intact.")
    ]

    for m_num, (m_title, m_desc) in enumerate(mandates, 1):
        p(f"### 7.{m_num} {m_title}")
        p(f"**Operational Rule:** {m_desc}")
        p("")

    p("---")
    p("")

    # SECTION 8: STEP-BY-STEP WORKFLOWS
    p("## 8. Step-by-Step Execution Workflows & Sequence Diagrams")
    p("")
    p("This section illustrates the exact sequence of interactions across the User, Frontend, FastAPI Backend, Bedrock AI, Database, and SMTP/IMAP servers:")
    p("")
    p("### 8.1 Mode B: Interactive Agent Chat Reminder Execution Sequence")
    p("```")
    p("User                 React UI              FastAPI / TurnManager         AWS Bedrock          PostgreSQL / SMTP")
    p(" |                      |                           |                         |                      |")
    p(" |-- 1. 'Draft reminder'->|                         |                         |                      |")
    p(" |   for INV-1004       |-- 2. POST /agent/chat --->|                         |                      |")
    p(" |                      |                           |-- 3. Converse (tool) ->|                      |")
    p(" |                      |                           |                         |-- 4. draft_reminder->|")
    p(" |                      |                           |<-- 5. Tool Call --------|                      |")
    p(" |                      |                           |-- 6. Execute Drafter ------------------------->|")
    p(" |                      |                           |-- 7. SSE Thought Chunks |                      |")
    p(" |                      |<-- 8. Render Preview -----|   + Draft Preview       |                      |")
    p(" |                      |    + PendingAction        |                         |                      |")
    p(" |                      |                           |                         |                      |")
    p(" |-- 9. 'Yes, send it' ->|                         |                         |                      |")
    p(" |                      |-- 10. POST /agent/chat -->|                         |                      |")
    p(" |                      |   (Confirm Action)        |-- 11. State Machine --->|                      |")
    p(" |                      |                           |   Match PendingAction   |                      |")
    p(" |                      |                           |-- 12. send_email(admin_approved=True) -------->|")
    p(" |                      |                           |   (Dispatches SMTP & Logs Audit)               |")
    p(" |                      |<-- 13. Delivery Status ---|                         |                      |")
    p(" |<-- 14. Confirmation -|    (SENT / FAILED)        |                         |                      |")
    p("```")
    p("")
    p("### 8.2 Inbound Debtor Email & UTR Payment Verification Sequence")
    p("```")
    p("Debtor             Gmail IMAP            Inbound Listener            Amazon Nova Pro            Approvals Queue")
    p("  |                    |                        |                           |                          |")
    p("  |-- 1. Sends email ->|                        |                           |                          |")
    p("  |   with UTR #       |-- 2. Fetch UNSEEN ---->|                           |                          |")
    p("  |                    |   (Port 993 SSL)       |-- 3. Extract Headers ---->|                          |")
    p("  |                    |                        |   (Match CUST-004)        |                          |")
    p("  |                    |                        |-- 4. Classify Intent ---->|                          |")
    p("  |                    |                        |<-- 5. PAYMENT_PROOF_UTR --|                          |")
    p("  |                    |                        |   (UTR: SBIN00928374)     |                          |")
    p("  |                    |                        |-- 6. Update Status --------------------------------->|")
    p("  |                    |                        |   VERIFYING_REMITTANCE    |                          |")
    p("  |                    |                        |-- 7. Insert Approval Ticket ------------------------>|")
    p("  |                    |                        |   (Awaiting Bank Match)   |                          |")
    p("  |<-- 8. SMTP Ack ----|<-----------------------|                           |                          |")
    p("  |    Confirmation    |                        |                           |                          |")
    p("```")
    p("")
    p("---")
    p("")

    return lines
