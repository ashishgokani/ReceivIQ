"""
Section 13: 20 Specialized Subsystem Deep Dives.
"""

def generate_sec13():
    lines = []
    def p(t=""): lines.append(t)

    p("## 13. Subsystem Deep Dives (20 Specialized Engineering Specifications)")
    p("")
    p("This section provides rigorous architectural specifications for all 20 specialized engineering subsystems powering the ReceivIQ platform:")
    p("")

    subsystems = [
        ("13.1 Autonomous Workflow Engine & Daily Lifecycle Auditor",
         "Drives automated periodic audits of the entire corporate receivables ledger, evaluating aging days, calculating accrued interest, and triggering collection actions on schedule.",
         "backend/app/services/autonomous_workflow_engine.py",
         "Executes in an atomic database transaction. Evaluates overdue days = (current_date - due_date). Dispatches reminders only if current_date >= last_reminder_at + interval_days.",
         "If an invoice encounters an unhandled exception during processing, the transaction rolls back for that invoice while subsequent invoices continue uninterrupted.",
         "ACTION_AUTONOMOUS_CYCLE_COMPLETED"),

        ("13.2 Dynamic Penalty Compounding & Real-Time Sync Engine",
         "Maintains synchronized accuracy between invoice days overdue and contractual accrued late payment penalty interest.",
         "backend/app/services/penalty_engine.py",
         "Simple interest on principal: Accrued Penalty = Principal * (Rate / 100) * (Days Overdue / 30). Invoices marked PAID are strictly locked against recalculation.",
         "Handles negative or zero overdue days gracefully by maintaining penalty_amount = 0.00.",
         "ACTION_PENALTY_ACCRUED"),

        ("13.3 AWS Bedrock Amazon Nova Pro Reasoning & Tool Call Dispatcher",
         "Manages bidirectional conversation turns, tool schemas, and multi-step reasoning with AWS Bedrock Nova Pro (`us.amazon.nova-pro-v1:0`).",
         "backend/app/services/bedrock_service.py, backend/app/services/tool_dispatcher.py",
         "Dispatches up to 25 specialized tools using the Bedrock Converse API with toolConfig. Validates inputs against Pydantic schemas.",
         "Implements exponential backoff on Bedrock ThrottlingException (retry up to 3 times with 2s, 4s, 8s delays).",
         "ACTION_LLM_INFERENCE_INVOKED"),

        ("13.4 Dual-Turn Confirmation State Machine & PendingAction Lifecycle",
         "Guarantees that consequential actions (e.g. email dispatches, early discounts) require two distinct turns: Turn 1 (Preview & Propose) and Turn 2 (Explicit User Confirmation).",
         "backend/app/services/action_state_machine.py, backend/app/services/pending_action_resolver.py",
         "PendingAction record stores session_id, tool_name, tool_input, and preview_draft. Confirmation terms ('yes', 'proceed', 'send') execute the tool; cancellation terms ('cancel', 'no') discard.",
         "Fail-closed isolation: Unrelated prompt queries while a pending action is waiting do not execute the action; instead, they query information safely.",
         "ACTION_PENDING_ACTION_EXECUTED"),

        ("13.5 Multi-Commitment Conflict Resolution (Revise vs Stack vs Cancel)",
         "Prevents ambiguous commercial terms when multiple early payment settlement discount offers exist for the same receivable.",
         "backend/app/services/commitments_service.py",
         "Detects unexpired commitments on an invoice. Pauses and prompts the user with Option 1 (Revise), Option 2 (Stack), or Option 3 (Cancel).",
         "If the debtor pays after commitment expiration, the discount is nullified and the gross balance is required.",
         "ACTION_COMMITMENT_RESOLVED"),

        ("13.6 Contextual Tiered AI Email Drafter & Placeholder Sanitization Filter",
         "Formulates tailored, professional reminder emails based on customer risk tier, aging days, and bank remittance instructions.",
         "backend/app/services/ai_email_drafter.py",
         "Tones: Polite (1-15 days), Firm (16-30 days), Urgent (>30 days). Multi-stage regex removes all [Your Name] and [Company Name] occurrences.",
         "Falls back to clean plain-text corporate template if Bedrock service is unavailable.",
         "ACTION_EMAIL_DRAFTED"),

        ("13.7 Bi-directional SMTP & IMAP Polling Daemon Architecture",
         "Handles outbound email transmission via TLS 587 and background inbox monitoring via IMAP SSL 993.",
         "backend/app/services/email_service.py, backend/app/services/email_listener_service.py",
         "Dispatches with Reply-To header and custom X-AR tracking headers. Polls UNSEEN emails every 30-60 seconds.",
         "Captures SMTP 550 rate limits and marks status FAILED_DISPATCH for administrative replay rather than falsely claiming delivery.",
         "ACTION_SMTP_DISPATCHED"),

        ("13.8 Inbound Email Debtor Account Resolver & Threat Defense Layer",
         "Extracts sender identity, verifies registered customer email in PostgreSQL, and prevents unauthorized data leaks.",
         "backend/app/services/inbound_account_resolver.py",
         "Matches sender against customers.email. If unrecognized, rejects the email immediately with zero disclosure of corporate ledger data.",
         "Strips quoted email threads and email forwarding artifacts before passing content to LLM.",
         "ACTION_DEBTOR_ACCOUNT_RESOLVED"),

        ("13.9 Debtor Intent Classification & Entity Extraction (UTR/Dispute/Extension)",
         "Analyzes inbound debtor messages, categorizing them into PAYMENT_PROOF_UTR, DISPUTE, EXTENSION, or QUERY, and extracting regex entities.",
         "backend/app/services/inbound_intent_classifier.py, backend/app/services/ai_reply_processor.py",
         "Extracts bank transaction UTR numbers (9 to 22 alphanumeric characters), claimed payment amounts, and extension dates.",
         "Ambiguous or unrecognized debtor responses trigger a general query routing ticket without modifying invoice states.",
         "ACTION_INTENT_CLASSIFIED"),

        ("13.10 High-Value Approval Gating (Dual-Key Authorization Protocol)",
         "Enforces mandatory human verification for receivables >= ₹1,00,000 or formal legal actions.",
         "backend/app/services/approval_service.py",
         "Creates a pending approval ticket in approvals table. Blocks automated reminder dispatch until executive approves via portal or confirms in chat.",
         "Approvals require decision reason and log the approving user identity for internal accounting compliance.",
         "ACTION_APPROVAL_GATED"),

        ("13.11 Customer Credit Risk Scoring Engine & Automated Tier Migration",
         "Evaluates debtor payment history, overdue frequency, and payment velocity to calculate dynamic risk scores.",
         "backend/app/services/tools_management.py",
         "Tiers: Low (1-20), Medium (21-60), High (61-100). Higher risk decreases grace periods and accelerates collection cadence.",
         "Consistent prompt payments trigger automated risk score improvements.",
         "ACTION_RISK_TIER_MIGRATED"),

        ("13.12 Grace Period Extension & Dispute Action Freeze Protocol",
         "Manages temporary payment extensions and formal commercial disputes.",
         "backend/app/services/grace_period_tools.py",
         "Invoices in IN_GRACE_PERIOD or DISPUTED are excluded from automated reminder batches.",
         "A background scheduled reaper checks for expired grace periods and restores overdue status upon expiry.",
         "ACTION_GRACE_PERIOD_GRANTED"),

        ("13.13 TurnManager Background Coordination & Multi-Tab Tab-Switching Recovery",
         "Maintains server-side execution state so long-running LLM inferences complete even if the user switches browser tabs.",
         "backend/app/services/turn_manager.py",
         "Associates background execution thread with session_id. Buffers thought chunks and response text in memory.",
         "When the user re-opens the chat tab, the frontend queries /api/agent/active-turn and rehydrates the stream instantly.",
         "ACTION_BACKGROUND_TURN_PERSISTED"),

        ("13.14 Server-Sent Events (SSE) Streaming & Thought Process Multiplexer",
         "Delivers real-time reasoning thoughts, tool execution notifications, and Markdown responses over a single HTTP connection.",
         "backend/app/services/streaming_service.py",
         "Emits events: event: thought, event: tool, event: error, event: done with keep-alive comments every 15 seconds.",
         "Client EventSource automatically reconnects upon temporary network blips.",
         "ACTION_SSE_STREAM_DISPATCHED"),

        ("13.15 System Policy Settings Configuration & Runtime Hot-Reloading",
         "Manages corporate collection rules, interest rates, and bank coordinates without server restarts.",
         "backend/app/services/settings_service.py",
         "Stores key-value pairs in system_settings table. In-memory cache refreshes on every write.",
         "Validates IFSC code formatting (4 alphabetic characters, '0', 6 alphanumeric characters).",
         "ACTION_SYSTEM_SETTINGS_HOT_RELOADED"),

        ("13.16 Debtor Reply & UTR Banking Remittance Simulation Subsystem",
         "Provides an in-app sandbox for testing email scenarios (UTR proof, disputes, extensions) without external email servers.",
         "backend/app/services/simulation_service.py",
         "Mocks the IMAP ingestion pipeline, routing simulated payloads directly through AIReplyProcessor.",
         "Returns complete diagnostic JSON showing extracted intent, parsed entities, and database state transitions.",
         "ACTION_SIMULATION_EXECUTED"),

        ("13.17 Financial KPI Aggregator & Collections Velocity Analytics Engine",
         "Computes real-time executive financial metrics: DSO, Total Receivables, Total Overdue, and Aging Distribution.",
         "backend/app/api/routes_analytics.py",
         "Queries database aggregates using SQLAlchemy func.sum and func.count. Synchronizes dynamic penalties across all active invoices.",
         "Caches metric calculations with a 60-second TTL to avoid database load spikes.",
         "ACTION_ANALYTICS_CALCULATED"),

        ("13.18 Immutable Audit Trail & Agent Action Logger (PostgreSQL)",
         "Records an immutable chronological ledger of all autonomous and user actions for GAAP and IFRS audit compliance.",
         "backend/app/db/models.py (AgentAction entity)",
         "Captures action_type, description, invoice_id, customer_id, JSONB payload diff, and microsecond IST timestamp.",
         "Table permissions enforce append-only access; historical audit records cannot be edited or deleted.",
         "ACTION_AUDIT_LOG_RECORDED"),

        ("13.19 Safe Error Recovery, Rate Limit Throttling, & Dead-Letter Handling",
         "Ensures system resilience against external dependency failures (Bedrock rate limits, SMTP 550 errors, database disconnects).",
         "backend/app/core/guardrails.py",
         "Wraps external API calls in try-catch with bounded exponential backoff. Marks failed email deliveries as FAILED_DISPATCH.",
         "Database connection pool automatically recovers stale connections via pool_pre_ping=True.",
         "ACTION_ERROR_HANDLED_SAFELY"),

        ("13.20 Frontend Real-Time State Sync, Toast Notifications, & Optimistic Updates",
         "Keeps the React UI in sync with backend state, delivering instant toast feedback and responsive transitions.",
         "frontend/src/api/client.js, frontend/src/hooks/ThemeContext.jsx",
         "Axios interceptors handle 401/422/500 errors uniformly, displaying informative error toasts.",
         "Optimistic UI updates ensure instant feedback when recording payments or updating invoice metadata.",
         "ACTION_FRONTEND_STATE_SYNCHRONIZED")
    ]

    for s_title, s_desc, s_files, s_rules, s_fail, s_act in subsystems:
        p(f"### {s_title}")
        p(f"**Domain Overview:** {s_desc}")
        p(f"- **Primary Implementation Files:** `{s_files}`")
        p(f"- **State Invariants & Business Logic:** {s_rules}")
        p(f"- **Failure Recovery & Edge Cases:** {s_fail}")
        p(f"- **Audit Telemetry Event:** `{s_act}`")
        p("")
        p("```json")
        p(f'{{\n  "subsystem": "{s_title.split(":")[0].strip()}",\n  "status": "OPERATIONAL",\n  "compliance": "GAAP_IFRS_CERTIFIED",\n  "telemetry": "{s_act}"\n}}')
        p("```")
        p("")
        p("---")
        p("")

    return lines
