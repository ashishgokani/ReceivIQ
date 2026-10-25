"""
Section 7 and 8: 15 Operational Mandates and 5 Complete Sequence Workflows.
"""

def generate_sec07_08():
    lines = []
    def p(t=""): lines.append(t)

    # SECTION 7: 15 OPERATIONAL MANDATES
    p("## 7. System Prompts, 15 Operational Mandates, & Safety Guardrails")
    p("")
    p("The Amazon Nova Pro reasoning engine is strictly constrained by 15 Operational Mandates embedded within `agent_prompts.py`:")
    p("")

    mandates = [
        ("Mandate 1: Live Real-Time Data Sourcing",
         "Never invent, assume, or hallucinate invoice IDs, customer names, or ledger balances. Always query live PostgreSQL records using tools (`get_overdue_invoices`, `get_invoice_details`). If no records exist, explicitly state that zero records were found."),
        ("Mandate 2: Dynamic Late Penalty Invariant",
         "Always calculate late penalties on principal balance at 2.0% per 30-day cycle. Never quote gross balances without separating principal and accrued penalties. Ensure penalties evaluate to ₹0.00 if within grace period."),
        ("Mandate 3: Absolute Immutability on Settled Debt",
         "Invoices marked PAID are strictly locked against recalculations, status changes, or reminder dispatches. Any attempt to modify settled debt must be politely rejected with a reference to GAAP accounting standards."),
        ("Mandate 4: Human-in-the-Loop High-Value Gate",
         "Any invoice with balance >= ₹1,00,000 cannot have a collection reminder sent without prior administrator confirmation or approval queue sign-off. The system must create an approval ticket rather than dispatching autonomously."),
        ("Mandate 5: Legal Escalation Gating",
         "Threatening legal action, filing insolvency notices, or assigning debt to attorneys requires explicit human approval via `create_escalation`. Autonomous models cannot initiate legal processes."),
        ("Mandate 6: Time-Bound Commercial Settlement Guardrails",
         "Early settlement discounts must be mathematically bounded between 0.1% and 0.5%, with explicit expiry deadlines (e.g. 24 hours). Proposing discounts outside this range violates corporate treasury guidelines."),
        ("Mandate 7: Multi-Commitment Conflict Resolution",
         "If an active discount offer already exists on an invoice, never overwrite silently. Present the user with Option 1 (Revise), Option 2 (Stack), or Option 3 (Cancel) before modifying commercial terms."),
        ("Mandate 8: Grace Period Freezes",
         "During an approved grace period, penalty accumulation is frozen and collection reminders are suspended. Debtors with active extensions must not receive automated collection notices."),
        ("Mandate 9: Dispute Action Freezing",
         "When an invoice is marked DISPUTED, all automated collection communications must cease immediately pending commercial resolution. Reminders remain paused until the dispute is resolved."),
        ("Mandate 10: Fail-Closed Tool Execution Rule",
         "When a user confirms an action (e.g., 'Yes, send it'), you MUST call the appropriate tool (`send_email`, `record_payment`). Never claim an action occurred in text without actually executing the tool call."),
        ("Mandate 11: Currency Formatting Standards",
         "All monetary amounts must be formatted in Indian Rupees with comma separators (e.g. ₹1,50,000 or ₹2,62,500). Interpret 'Lakh' as 100,000 and 'Crore' as 10,000,000 in user prompts."),
        ("Mandate 12: Bank Remittance Details Mandate",
         "Every drafted reminder email must include complete bank remittance coordinates: Beneficiary Legal Entity, Bank Name, Account Number, and IFSC Code from system settings."),
        ("Mandate 13: Zero-Placeholder Guarantee",
         "Never output placeholders like `[Your Name]`, `[Your Company Name]`, or `[Title]`. Sign all communications as 'Accounts Receivable Team' and 'ReceivIQ'."),
        ("Mandate 14: Debtor Customer Identity Verification",
         "Incoming debtor emails must be authenticated against registered customer email records. Reject unknown senders immediately to prevent unauthorized disclosures."),
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
    p("This section illustrates 5 complete execution sequences across the User, Frontend, FastAPI Backend, Bedrock AI, Database, and SMTP/IMAP servers:")
    p("")
    p("### 8.1 Mode A: Autonomous Periodic Background Collection Cycle")
    p("```")
    p("APScheduler Daemon        PostgreSQL Ledger         Penalty Engine         Approval Gate         SMTP Relay")
    p("      |                         |                         |                      |                    |")
    p("      |-- 1. Trigger Cron ----->|                         |                      |                    |")
    p("      |   (Every 15 mins)       |-- 2. Fetch Overdue ---->|                      |                    |")
    p("      |                         |   Invoices              |                      |                    |")
    p("      |                         |                         |-- 3. Calculate ----->|                    |")
    p("      |                         |                         |   Accrued Penalties  |                    |")
    p("      |                         |<-- 4. Update Balances --|                      |                    |")
    p("      |                         |                                                |                    |")
    p("      |                         |-- 5. Evaluate Thresholds --------------------->|                    |")
    p("      |                         |   If Balance >= ₹1,00,000                      |                    |")
    p("      |                         |<-- 6. Insert Pending Approval Ticket ----------|                    |")
    p("      |                         |                                                                     |")
    p("      |                         |-- 7. Invoices < ₹1,00,000 ----------------------------------------->|")
    p("      |                         |   Dispatch Overdue Reminder Notice via Port 587 STARTTLS            |")
    p("      |                         |<-- 8. Increment reminder_count & log communication -----------------|")
    p("      |-- 9. Log Audit Event -->|")
    p("      |   ACTION_AUTONOMOUS_CYCLE_COMPLETED")
    p("```")
    p("")
    p("### 8.2 Mode B: Interactive Agent Chat Reminder Execution Sequence")
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
    p("### 8.3 Inbound Debtor Email & UTR Payment Verification Sequence")
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
    p("### 8.4 Multi-Commitment Conflict Resolution (Revise vs Stack vs Cancel)")
    p("```")
    p("User                 Agent Chat               Commitments Engine              State Machine        PostgreSQL")
    p(" |                       |                            |                            |                    |")
    p(" |-- 1. 'Offer 0.5% ---->|                            |                            |                    |")
    p(" |   discount on INV-1'  |-- 2. Check Existing ------>|                            |                    |")
    p(" |                       |   Commitments              |-- 3. Found Active 0.25% -->|                    |")
    p(" |                       |                            |   Offer Expiring in 12h    |                    |")
    p(" |                       |<-- 4. Prompt 3 Choices ----|                            |                    |")
    p(" |<-- 5. 'Choose: -------|    (1: Revise, 2: Stack,   |                            |                    |")
    p(" |    1, 2, or 3'        |     3: Cancel)'            |                            |                    |")
    p(" |                       |                            |                            |                    |")
    p(" |-- 6. 'Option 1' ----->|                            |                            |                    |")
    p(" |                       |-- 7. Execute Revoke & ---->|                            |                    |")
    p(" |                       |   Create New 0.5% Offer    |                            |-- 8. UPDATE ------>|")
    p(" |                       |<-- 9. Confirm New Terms ---|                            |   system_settings  |")
    p(" |<-- 10. Success -------|                            |                            |                    |")
    p("```")
    p("")
    p("### 8.5 Human Approval Workflow for High-Value Invoices (>= ₹1,00,000)")
    p("```")
    p("Credit Controller              Approvals Portal              Approval Service              SMTP Dispatcher")
    p("       |                              |                              |                            |")
    p("       |-- 1. Open Approvals Page --->|                              |                            |")
    p("       |                              |-- 2. GET /api/approvals ---->|                            |")
    p("       |                              |<-- 3. Return Pending Queue --|                            |")
    p("       |                              |   (Ticket #APP-001)          |                            |")
    p("       |                              |   (Invoice INV-1004: ₹2.62L) |                            |")
    p("       |-- 4. Click 'Approve' ------->|                              |                            |")
    p("       |   Enter reason               |-- 5. POST /approvals/{id} -->|                            |")
    p("       |                              |   decision='APPROVED'        |-- 6. Dispatch Email ------>|")
    p("       |                              |                              |<-- 7. SMTP Success --------|")
    p("       |                              |<-- 8. Return Updated State --|                            |")
    p("       |<-- 9. Toast Notification ----|                              |                            |")
    p("```")
    p("")
    p("---")
    p("")

    return lines
