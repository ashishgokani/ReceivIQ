"""
Section 10: REST API Specification & Endpoint Documentation (26 Endpoints).
"""

def generate_sec10():
    lines = []
    def p(t=""): lines.append(t)

    p("## 10. REST API Specification & Endpoint Documentation (26 Endpoints)")
    p("")
    p("Every single REST endpoint exposed by the FastAPI backend application is documented below with HTTP methods, query parameters, request headers, request bodies, success responses, error responses, and complete curl commands:")
    p("")

    api_endpoints = [
        ("10.1 GET /api/invoices", "List Invoices", "GET", "/api/invoices",
         "status (optional): PENDING, OVERDUE, PAID, DISPUTED; customer_id (optional): Debtor ID; min_overdue_days (optional): Integer",
         "None",
         """[
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
    "due_date": "2026-10-04",
    "reminder_count": 2
  }
]""",
         "Returns list of invoices matching query filters with dynamic accrued penalties synchronized in real time."),

        ("10.2 GET /api/invoices/{id}", "Get Invoice Details", "GET", "/api/invoices/INV-1004",
         "id: Invoice identifier (path parameter)",
         "None",
         """{
  "invoice_id": "INV-1004",
  "invoice_number": "INV-2026-1004",
  "customer_id": "CUST-004",
  "company_name": "Helios Retail Corp",
  "amount": 250000.0,
  "penalty_amount": 12500.0,
  "total_amount": 262500.0,
  "status": "OVERDUE",
  "reminder_count": 2,
  "due_date": "2026-10-04",
  "payments": [],
  "communications": []
}""",
         "Retrieves complete financial details, payment ledger, and communication history for a single invoice."),

        ("10.3 POST /api/invoices", "Issue New Invoice", "POST", "/api/invoices",
         "None",
         """{
  "customer_id": "CUST-002",
  "amount": 150000.0,
  "due_date": "2026-11-15",
  "notes": "Q4 Server Infrastructure Consulting"
}""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1099",
  "invoice_number": "INV-2026-1099",
  "amount": 150000.0,
  "total_amount": 150000.0,
  "status": "PENDING",
  "message": "Invoice created successfully"
}""",
         "Issues a new invoice with Pydantic validation, automatically generating unique invoice numbers and updating customer ledger totals."),

        ("10.4 PUT /api/invoices/{id}", "Update Invoice Terms", "PUT", "/api/invoices/INV-1004",
         "id: Invoice identifier (path parameter)",
         """{
  "due_date": "2026-11-20",
  "notes": "Extended commercial terms approved by CFO"
}""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1004",
  "message": "Invoice updated successfully"
}""",
         "Modifies commercial due date or notes for unsettled invoices. Invoices marked PAID reject edits."),

        ("10.5 POST /api/invoices/{id}/pay", "Record Payment Remittance", "POST", "/api/invoices/INV-1004/pay",
         "id: Invoice identifier (path parameter)",
         """{
  "amount": 262500.0,
  "payment_method": "NEFT",
  "reference_number": "SBIN00928374",
  "notes": "Full settlement via corporate banking"
}""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1004",
  "amount_paid": 262500.0,
  "new_status": "PAID",
  "message": "Payment recorded successfully. Invoice marked PAID and permanently locked."
}""",
         "Records full or partial payment, inserts record into `payments`, zeroes total_amount, and locks settled debt."),

        ("10.6 POST /api/invoices/{id}/dispute", "File Invoice Dispute", "POST", "/api/invoices/INV-1005/dispute",
         "id: Invoice identifier (path parameter)",
         """{
  "reason": "Debtor reported delivery batch #4 arrived damaged; commercial credit requested"
}""",
         """{
  "status": "SUCCESS",
  "invoice_id": "INV-1005",
  "previous_status": "OVERDUE",
  "new_status": "DISPUTED",
  "message": "Invoice marked DISPUTED. Automated collection reminders are frozen."
}""",
         "Marks invoice as DISPUTED, halting automated reminder dispatches until commercial resolution."),

        ("10.7 GET /api/customers", "List Customer Directory", "GET", "/api/customers",
         "search (optional): Search company or contact name; risk_level (optional): Low, Medium, High",
         "None",
         """[
  {
    "customer_id": "CUST-002",
    "name": "Aditya Verma",
    "company_name": "Summit Logistics",
    "email": "ap@summitlog.com",
    "phone": "+91-98200-11223",
    "risk_level": "Medium",
    "total_outstanding": 315000.0
  }
]""",
         "Retrieves all debtor accounts with total outstanding balances and risk indicators."),

        ("10.8 GET /api/customers/{id}", "Get Customer Profile", "GET", "/api/customers/CUST-002",
         "id: Customer identifier (path parameter)",
         "None",
         """{
  "customer_id": "CUST-002",
  "name": "Aditya Verma",
  "company_name": "Summit Logistics",
  "email": "ap@summitlog.com",
  "phone": "+91-98200-11223",
  "address": "402 Nariman Point, Mumbai, MH",
  "risk_level": "Medium",
  "credit_limit": 500000.0,
  "total_outstanding": 315000.0
}""",
         "Fetches complete profile metadata and credit risk scoring for a single corporate debtor."),

        ("10.9 POST /api/customers", "Onboard Corporate Debtor", "POST", "/api/customers",
         "None",
         """{
  "name": "Rohan Shah",
  "company_name": "Nexus Dynamics",
  "email": "billing@nexusdyn.com",
  "phone": "+91-99887-76655",
  "address": "Bandra Kurla Complex, Mumbai",
  "risk_level": "Low"
}""",
         """{
  "status": "SUCCESS",
  "customer_id": "CUST-104",
  "message": "Customer Nexus Dynamics onboarded successfully"
}""",
         "Onboards a new corporate debtor with initial risk level and contact parameters."),

        ("10.10 PUT /api/customers/{id}", "Update Debtor Details", "PUT", "/api/customers/CUST-104",
         "id: Customer identifier (path parameter)",
         """{
  "name": "Rohan Shah",
  "email": "finance@nexusdyn.com",
  "phone": "+91-99887-76655",
  "risk_level": "Medium"
}""",
         """{
  "status": "SUCCESS",
  "customer_id": "CUST-104",
  "message": "Customer updated successfully"
}""",
         "Updates contact coordinates or credit risk tier for an existing debtor profile."),

        ("10.11 DELETE /api/customers/{id}", "Delete Debtor Profile", "DELETE", "/api/customers/CUST-099",
         "id: Customer identifier (path parameter)",
         "None",
         """{
  "status": "SUCCESS",
  "customer_id": "CUST-099",
  "message": "Customer CUST-099 removed successfully."
}""",
         "Deletes a debtor profile only if they possess zero associated invoices."),

        ("10.12 GET /api/customers/{id}/history", "Get Debtor Payment History", "GET", "/api/customers/CUST-002/history",
         "id: Customer identifier (path parameter)",
         "None",
         """{
  "customer_id": "CUST-002",
  "company_name": "Summit Logistics",
  "total_invoices": 8,
  "paid_invoices": 6,
  "overdue_invoices": 2,
  "invoices": []
}""",
         "Returns complete historical audit trail of invoices, payment dates, and reminder notices."),

        ("10.13 POST /api/agent/chat", "Send Natural Language Agent Message", "POST", "/api/agent/chat",
         "None",
         """{
  "message": "Show all overdue accounts over 15 days",
  "session_id": "session-123"
}""",
         """{
  "reply": "Here is the list of customers with overdue invoices more than 15 days...",
  "tool_calls": ["get_overdue_invoices"],
  "pending_action": null
}""",
         "Executes multi-turn conversation turn with Amazon Nova Pro, dispatching autonomous tools."),

        ("10.14 GET /api/agent/stream", "Stream Agent Reasoning Thoughts (SSE)", "GET", "/api/agent/stream?session_id=session-123",
         "session_id (query parameter): Unique session identifier",
         "None",
         """data: {"type": "thought", "content": "Querying PostgreSQL overdue invoices..."}\n\ndata: {"type": "done"}""",
         "Streams real-time thought chunks, tool notifications, and Markdown outputs over HTTP SSE."),

        ("10.15 GET /api/agent/active-turn", "Check Background Turn Execution State", "GET", "/api/agent/active-turn?session_id=session-123",
         "session_id (query parameter)",
         "None",
         """{
  "is_active": true,
  "session_id": "session-123",
  "thoughts": "Evaluating overdue aging buckets..."
}""",
         "Enables the frontend to rehydrate active thought streams after browser tab switching."),

        ("10.16 GET /api/approvals", "List Pending Approvals", "GET", "/api/approvals",
         "status (optional): PENDING, APPROVED, REJECTED",
         "None",
         """[
  {
    "approval_id": "APP-001",
    "invoice_id": "INV-1004",
    "action_type": "REMINDER_HIGH_VALUE",
    "reason": "Invoice amount INR 2,62,500.00 exceeds INR 1,00,000 threshold",
    "status": "PENDING"
  }
]""",
         "Lists pending governance tickets awaiting executive review and authorization."),

        ("10.17 POST /api/approvals/{id}/action", "Approve or Reject Ticket", "POST", "/api/approvals/APP-001/action",
         "id: Approval identifier (path parameter)",
         """{
  "decision": "APPROVED",
  "decision_reason": "Verified with VP of Finance"
}""",
         """{
  "status": "SUCCESS",
  "approval_id": "APP-001",
  "decision": "APPROVED",
  "message": "Action executed and reminder dispatched over SMTP."
}""",
         "Approves or rejects a pending ticket, triggering automated dispatch if approved."),

        ("10.18 GET /api/activity", "Get Agent Activity Log", "GET", "/api/activity?limit=20",
         "limit (optional): Max items to return (default 50)",
         "None",
         """[
  {
    "action_id": "ACT-1024",
    "action_type": "EMAIL_SENT",
    "description": "Payment reminder dispatched for INV-1008",
    "created_at": "2026-10-25T07:43:00Z"
  }
]""",
         "Returns chronological audit stream from `agent_actions` table."),

        ("10.19 GET /api/analytics/dashboard", "Executive Financial Analytics", "GET", "/api/analytics/dashboard",
         "None",
         "None",
         """{
  "total_receivables": 1250000.0,
  "total_overdue": 850000.0,
  "dso_days": 38.5,
  "collection_velocity_percent": 84.2,
  "aging_buckets": {
    "1_15_days": 150000.0,
    "16_30_days": 400000.0,
    "31_60_days": 200000.0,
    "61_plus_days": 100000.0
  }
}""",
         "Computes real-time DSO, receivables totals, and aging distributions for dashboard charts."),

        ("10.20 GET /api/settings", "Get All System Settings", "GET", "/api/settings",
         "None",
         "None",
         """{
  "penalty": {
    "rate": 2.0,
    "cycle": 30,
    "calculation_base": "PRINCIPAL_ONLY"
  },
  "bank": {
    "beneficiary": "Treasury Department",
    "account": "123456789012",
    "ifsc": "SBIN0001234"
  }
}""",
         "Retrieves active business rules, late fees, and bank coordinates across all categories."),

        ("10.21 PUT /api/settings/penalty", "Update Penalty Settings", "PUT", "/api/settings/penalty",
         "None",
         """{
  "calculation_base": "PRINCIPAL_ONLY",
  "low_risk": {
    "penalty_rate_percent": 1.5,
    "grace_period_days": 15
  }
}""",
         """{
  "status": "SUCCESS",
  "message": "Penalty settings updated successfully"
}""",
         "Updates late fee interest percentages and grace days per debtor risk tier."),

        ("10.22 PUT /api/settings/reminders", "Update Reminder Settings", "PUT", "/api/settings/reminders",
         "None",
         """{
  "automation_enabled": true,
  "automation_interval_minutes": 15,
  "low_risk": {
    "auto_reminders_enabled": true,
    "reminder_interval_days": 7
  }
}""",
         """{
  "status": "SUCCESS",
  "message": "Reminder settings updated successfully"
}""",
         "Configures collection cadence and instantly reconfigures the background scheduler."),

        ("10.23 PUT /api/settings/bank", "Update Bank Remittance Details", "PUT", "/api/settings/bank",
         "None",
         """{
  "beneficiary_name": "Treasury Department",
  "bank_name": "State Bank of India",
  "account_number": "123456789012",
  "confirm_account_number": "123456789012",
  "ifsc_code": "SBIN0001234",
  "payment_instructions": "Quote invoice number on remittance"
}""",
         """{
  "status": "SUCCESS",
  "message": "Bank details updated successfully"
}""",
         "Updates beneficiary coordinates with IFSC regex and confirmation validation."),

        ("10.24 PUT /api/settings/agent", "Master Toggle AI Agent", "PUT", "/api/settings/agent",
         "None",
         """{
  "agent_enabled": true
}""",
         """{
  "status": "SUCCESS",
  "agent_enabled": true
}""",
         "Master kill-switch to pause or resume autonomous agent dispatches and reasoning."),

        ("10.25 POST /api/simulation/inbound-email", "Simulate Inbound Debtor Email", "POST", "/api/simulation/inbound-email",
         "None",
         """{
  "invoice_id": "INV-1004",
  "scenario": "PAYMENT_PROOF_UTR",
  "body": "We have paid INR 2,62,500.00 via NEFT. Bank reference is SBIN00928374."
}""",
         """{
  "status": "SUCCESS",
  "extracted_intent": "PAYMENT_PROOF_UTR",
  "utr": "SBIN00928374",
  "new_invoice_status": "VERIFYING_REMITTANCE",
  "drafted_acknowledgment": "Thank you for providing payment reference SBIN00928374..."
}""",
         "Runs simulated debtor email through AI parser, updating invoice state without external email tools."),

        ("10.26 POST /api/automation/run", "Trigger Autonomous Run Now", "POST", "/api/automation/run",
         "None",
         "None",
         """{
  "status": "COMPLETED",
  "invoices_audited": 12,
  "penalties_synced": 5,
  "reminders_dispatched": 2,
  "approvals_created": 1
}""",
         "Triggers immediate Mode A background ledger audit, penalty sync, and reminder dispatches.")
    ]

    for title, desc, meth, pth, qparams, req_body, res_body, summary in api_endpoints:
        p(f"### {title} ({desc})")
        p(f"**Functional Overview:** {summary}")
        p(f"- **HTTP Method:** `{meth}`")
        p(f"- **Request Path:** `{pth}`")
        p(f"- **Query Parameters:** {qparams}")
        p("- **Headers:** `Content-Type: application/json`, `Accept: application/json`")
        p("")
        p("#### Sample cURL Command")
        p("```bash")
        p(f"curl -X {meth} \"http://127.0.0.1:8000{pth}\" \\")
        p("  -H \"Content-Type: application/json\"" + (f" \\\n  -d '{req_body}'" if req_body != "None" else ""))
        p("```")
        p("")
        p("#### Request Payload Body (JSON)")
        p("```json")
        p(req_body)
        p("```")
        p("")
        p("#### Success Response Payload Body (HTTP 200 OK)")
        p("```json")
        p(res_body)
        p("```")
        p("")
        p("#### Standard Error Responses")
        p("##### HTTP 422 Unprocessable Content (Schema Validation Failure)")
        p("```json")
        p("{\n  \"detail\": [\n    {\n      \"loc\": [\"body\", \"amount\"],\n      \"msg\": \"Input should be greater than 0\",\n      \"type\": \"greater_than\"\n    }\n  ]\n}")
        p("```")
        p("")
        p("##### HTTP 500 Internal Server Error (External Service Failure)")
        p("```json")
        p("{\n  \"detail\": \"External communication failure: SMTP relay returned temporary error (550). Action recorded for retry.\"\n}")
        p("```")
        p("")
        p("---")
        p("")

    return lines
