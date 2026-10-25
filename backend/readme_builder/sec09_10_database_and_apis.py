"""
Section 9 and 10: Complete Database Schema, SQL DDL, and REST API Specifications.
"""

def generate_sec09_10():
    lines = []
    def p(t=""): lines.append(t)

    # SECTION 9: DATABASE SCHEMA & DDL
    p("## 9. Complete Database Schema, Entity Relationships, & SQL DDL")
    p("")
    p("ReceivIQ uses a normalized relational architecture across 7 core entities:")
    p("")
    p("```")
    p("  +----------------+         1:N          +-------------------+")
    p("  |   customers    |--------------------->|     invoices      |")
    p("  +----------------+                      +-------------------+")
    p("          |                                         |")
    p("          | 1:N                                     | 1:N")
    p("          v                                         +------------------+")
    p("  +----------------+                                | 1:N              | 1:N")
    p("  | communications |                                v                  v")
    p("  +----------------+                      +-------------------+ +--------------+")
    p("                                          |     payments      | |  approvals   |")
    p("                                          +-------------------+ +--------------+")
    p("  +----------------+  +-------------------+")
    p("  | agent_actions  |  |  system_settings  |")
    p("  +----------------+  +-------------------+")
    p("```")
    p("")
    p("### 9.1 Relational Data Definition Language (PostgreSQL SQL DDL)")
    p("```sql")
    p("-- 1. Customers / Debtors Entity")
    p("CREATE TABLE customers (")
    p("    customer_id VARCHAR(50) PRIMARY KEY,")
    p("    name VARCHAR(255) NOT NULL,")
    p("    company_name VARCHAR(255) NOT NULL,")
    p("    email VARCHAR(255) UNIQUE NOT NULL,")
    p("    phone VARCHAR(50),")
    p("    address TEXT,")
    p("    risk_level VARCHAR(20) DEFAULT 'Low' CHECK (risk_level IN ('Low', 'Medium', 'High')),")
    p("    credit_limit NUMERIC(15, 2) DEFAULT 500000.00,")
    p("    total_outstanding NUMERIC(15, 2) DEFAULT 0.00,")
    p("    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,")
    p("    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP")
    p(");")
    p("CREATE INDEX idx_customers_email ON customers(email);")
    p("CREATE INDEX idx_customers_risk ON customers(risk_level);")
    p("")
    p("-- 2. Invoices Entity")
    p("CREATE TABLE invoices (")
    p("    invoice_id VARCHAR(50) PRIMARY KEY,")
    p("    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,")
    p("    invoice_number VARCHAR(100) UNIQUE NOT NULL,")
    p("    invoice_date DATE NOT NULL,")
    p("    due_date DATE NOT NULL,")
    p("    amount NUMERIC(15, 2) NOT NULL,")
    p("    penalty_amount NUMERIC(15, 2) DEFAULT 0.00,")
    p("    total_amount NUMERIC(15, 2) NOT NULL,")
    p("    status VARCHAR(30) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'OVERDUE', 'PAID', 'DISPUTED', 'IN_GRACE_PERIOD', 'VERIFYING_REMITTANCE')),")
    p("    reminder_count INTEGER DEFAULT 0,")
    p("    last_reminder_at TIMESTAMP WITH TIME ZONE,")
    p("    dispute_reason TEXT,")
    p("    grace_period_until DATE,")
    p("    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,")
    p("    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP")
    p(");")
    p("CREATE INDEX idx_invoices_status_due ON invoices(status, due_date);")
    p("CREATE INDEX idx_invoices_customer ON invoices(customer_id);")
    p("")
    p("-- 3. Payments Ledger Entity")
    p("CREATE TABLE payments (")
    p("    payment_id VARCHAR(50) PRIMARY KEY,")
    p("    invoice_id VARCHAR(50) NOT NULL REFERENCES invoices(invoice_id) ON DELETE RESTRICT,")
    p("    amount_paid NUMERIC(15, 2) NOT NULL,")
    p("    payment_date DATE NOT NULL,")
    p("    payment_method VARCHAR(50) NOT NULL,")
    p("    reference_number VARCHAR(100),")
    p("    notes TEXT,")
    p("    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP")
    p(");")
    p("CREATE INDEX idx_payments_invoice ON payments(invoice_id);")
    p("CREATE INDEX idx_payments_reference ON payments(reference_number);")
    p("")
    p("-- 4. Communications Audit Entity")
    p("CREATE TABLE communications (")
    p("    communication_id VARCHAR(50) PRIMARY KEY,")
    p("    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,")
    p("    invoice_id VARCHAR(50) REFERENCES invoices(invoice_id) ON DELETE SET NULL,")
    p("    direction VARCHAR(10) NOT NULL CHECK (direction IN ('INBOUND', 'OUTBOUND')),")
    p("    channel VARCHAR(20) DEFAULT 'EMAIL',")
    p("    subject VARCHAR(255),")
    p("    body TEXT NOT NULL,")
    p("    delivery_status VARCHAR(20) DEFAULT 'DELIVERED',")
    p("    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP")
    p(");")
    p("CREATE INDEX idx_comms_invoice ON communications(invoice_id);")
    p("")
    p("-- 5. Governance Approvals Queue Entity")
    p("CREATE TABLE approvals (")
    p("    approval_id VARCHAR(50) PRIMARY KEY,")
    p("    invoice_id VARCHAR(50) NOT NULL REFERENCES invoices(invoice_id) ON DELETE CASCADE,")
    p("    action_type VARCHAR(50) NOT NULL,")
    p("    reason TEXT NOT NULL,")
    p("    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),")
    p("    approved_by VARCHAR(100),")
    p("    decision_reason TEXT,")
    p("    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,")
    p("    decided_at TIMESTAMP WITH TIME ZONE")
    p(");")
    p("CREATE INDEX idx_approvals_status ON approvals(status);")
    p("")
    p("-- 6. Immutable Agent Actions Telemetry Stream")
    p("CREATE TABLE agent_actions (")
    p("    action_id VARCHAR(50) PRIMARY KEY,")
    p("    action_type VARCHAR(50) NOT NULL,")
    p("    invoice_id VARCHAR(50),")
    p("    customer_id VARCHAR(50),")
    p("    description TEXT NOT NULL,")
    p("    details JSONB,")
    p("    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP")
    p(");")
    p("CREATE INDEX idx_actions_created ON agent_actions(created_at DESC);")
    p("")
    p("-- 7. System Policy Settings Entity")
    p("CREATE TABLE system_settings (")
    p("    setting_id VARCHAR(50) PRIMARY KEY,")
    p("    category VARCHAR(50) NOT NULL,")
    p("    key VARCHAR(100) NOT NULL,")
    p("    value TEXT NOT NULL,")
    p("    description TEXT,")
    p("    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,")
    p("    CONSTRAINT uq_category_key UNIQUE (category, key)")
    p(");")
    p("```")
    p("")
    p("---")
    p("")

    # SECTION 10: REST APIS
    p("## 10. REST API Specification & Endpoint Documentation (26 Endpoints)")
    p("")
    p("Every single REST endpoint exposed by the FastAPI application is documented below with method, path, payloads, and responses:")
    p("")

    apis = [
        ("GET", "/api/invoices", "List Invoices", "None",
         """[{"invoice_id": "INV-1004", "customer_name": "Helios Retail Corp", "amount": 250000.0, "penalty_amount": 12500.0, "total_amount": 262500.0, "status": "OVERDUE", "due_date": "2026-10-04"}]"""),

        ("GET", "/api/invoices/{id}", "Get Invoice Details", "None",
         """{"invoice_id": "INV-1004", "invoice_number": "INV-2026-1004", "customer_id": "CUST-004", "amount": 250000.0, "penalty_amount": 12500.0, "total_amount": 262500.0, "status": "OVERDUE"}"""),

        ("POST", "/api/invoices", "Create Invoice",
         """{"customer_id": "CUST-002", "amount": 150000.0, "due_date": "2026-11-15", "notes": "Q4 Server Infrastructure"}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1099", "message": "Invoice created successfully"}"""),

        ("PUT", "/api/invoices/{id}", "Update Invoice",
         """{"due_date": "2026-11-20", "notes": "Extended commercial terms"}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1004", "message": "Invoice updated successfully"}"""),

        ("POST", "/api/invoices/{id}/pay", "Record Payment",
         """{"amount": 262500.0, "payment_method": "NEFT", "reference_number": "SBIN00928374", "notes": "Full settlement"}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1004", "amount_paid": 262500.0, "new_status": "PAID"}"""),

        ("POST", "/api/invoices/{id}/dispute", "File Dispute",
         """{"reason": "Damaged goods reported on delivery batch #4"}""",
         """{"status": "SUCCESS", "invoice_id": "INV-1005", "new_status": "DISPUTED"}"""),

        ("GET", "/api/customers", "List Customers", "None",
         """[{"customer_id": "CUST-002", "name": "Aditya Verma", "company_name": "Summit Logistics", "email": "ap@summitlog.com", "risk_level": "Medium", "total_outstanding": 315000.0}]"""),

        ("GET", "/api/customers/{id}", "Get Customer Details", "None",
         """{"customer_id": "CUST-002", "name": "Aditya Verma", "company_name": "Summit Logistics", "email": "ap@summitlog.com", "risk_level": "Medium"}"""),

        ("POST", "/api/customers", "Create Customer",
         """{"name": "Rohan Shah", "company_name": "Nexus Dynamics", "email": "billing@nexusdyn.com", "risk_level": "Low"}""",
         """{"status": "SUCCESS", "customer_id": "CUST-104", "message": "Customer onboarded"}"""),

        ("PUT", "/api/customers/{id}", "Update Customer",
         """{"name": "Rohan Shah", "email": "finance@nexusdyn.com", "risk_level": "Medium"}""",
         """{"status": "SUCCESS", "customer_id": "CUST-104", "message": "Customer updated"}"""),

        ("DELETE", "/api/customers/{id}", "Delete Customer", "None",
         """{"status": "SUCCESS", "customer_id": "CUST-099", "message": "Customer deleted"}"""),

        ("GET", "/api/customers/{id}/history", "Customer History", "None",
         """{"customer_id": "CUST-002", "total_invoices": 8, "paid_invoices": 6, "overdue_invoices": 2, "invoices": []}"""),

        ("POST", "/api/agent/chat", "Send Agent Chat Message",
         """{"message": "Show all overdue accounts", "session_id": "session-123"}""",
         """{"reply": "Here are your overdue accounts...", "tool_calls": ["get_overdue_invoices"], "pending_action": null}"""),

        ("GET", "/api/agent/stream", "Stream Agent Thought Chunks (SSE)", "None (query: ?session_id=session-123)",
         """data: {"type": "thought", "content": "Querying PostgreSQL overdue invoices..."}\n\ndata: {"type": "done"}"""),

        ("GET", "/api/agent/active-turn", "Get Background Turn State", "None (query: ?session_id=session-123)",
         """{"is_active": true, "session_id": "session-123", "thoughts": "Evaluating overdue aging..."}"""),

        ("GET", "/api/approvals", "List Pending Approvals", "None",
         """[{"approval_id": "APP-001", "invoice_id": "INV-1004", "action_type": "REMINDER_HIGH_VALUE", "status": "PENDING"}]"""),

        ("POST", "/api/approvals/{id}/action", "Approve or Reject Ticket",
         """{"decision": "APPROVED", "decision_reason": "Verified with CFO"}""",
         """{"status": "SUCCESS", "approval_id": "APP-001", "decision": "APPROVED"}"""),

        ("GET", "/api/activity", "Get Agent Activity Log", "None (query: ?limit=20)",
         """[{"action_id": "ACT-1024", "action_type": "EMAIL_SENT", "description": "Reminder sent for INV-1008", "created_at": "2026-10-25T07:43:00Z"}]"""),

        ("GET", "/api/analytics/dashboard", "Executive Financial Analytics", "None",
         """{"total_receivables": 1250000.0, "total_overdue": 850000.0, "dso_days": 38.5, "collection_velocity_percent": 84.2}"""),

        ("GET", "/api/settings", "Get All System Settings", "None",
         """{"penalty": {"rate": 2.0, "cycle": 30}, "bank": {"beneficiary": "Treasury Department", "ifsc": "SBIN0001234"}}"""),

        ("PUT", "/api/settings/penalty", "Update Penalty Settings",
         """{"calculation_base": "PRINCIPAL_ONLY", "low_risk": {"penalty_rate_percent": 1.5, "grace_period_days": 15}}""",
         """{"status": "SUCCESS", "message": "Penalty settings updated"}"""),

        ("PUT", "/api/settings/reminders", "Update Reminder Settings",
         """{"automation_enabled": true, "low_risk": {"auto_reminders_enabled": true, "reminder_interval_days": 7}}""",
         """{"status": "SUCCESS", "message": "Reminder settings updated"}"""),

        ("PUT", "/api/settings/bank", "Update Bank Remittance Details",
         """{"beneficiary_name": "Treasury Department", "bank_name": "SBI", "account_number": "123456789012", "confirm_account_number": "123456789012", "ifsc_code": "SBIN0001234"}""",
         """{"status": "SUCCESS", "message": "Bank details updated"}"""),

        ("PUT", "/api/settings/agent", "Master Toggle AI Agent",
         """{"agent_enabled": true}""",
         """{"status": "SUCCESS", "agent_enabled": true}"""),

        ("POST", "/api/simulation/inbound-email", "Simulate Inbound Debtor Email",
         """{"invoice_id": "INV-1004", "scenario": "PAYMENT_PROOF_UTR", "body": "Paid ₹2,62,500. UTR is SBIN00928374"}""",
         """{"status": "SUCCESS", "extracted_intent": "PAYMENT_PROOF_UTR", "utr": "SBIN00928374", "new_invoice_status": "VERIFYING_REMITTANCE"}"""),

        ("POST", "/api/automation/run", "Trigger Autonomous Collection Run", "None",
         """{"status": "COMPLETED", "invoices_audited": 12, "penalties_synced": 5, "reminders_dispatched": 2, "approvals_created": 1}""")
    ]

    for m, pth, name, req, res in apis:
        p(f"### {m} `{pth}` ({name})")
        p("```bash")
        p(f"curl -X {m} \"http://127.0.0.1:8000{pth}\" \\")
        p("  -H \"Content-Type: application/json\"" + (f" \\\n  -d '{req}'" if req != "None" else ""))
        p("```")
        p(f"- **Request Body:** `{req}`")
        p(f"- **Response JSON:** `{res}`")
        p("")

    p("---")
    p("")

    return lines
