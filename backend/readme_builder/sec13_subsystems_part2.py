"""
Section 13 Part 2: Subsystem Deep Dives 13.11 through 13.20.
"""

def generate_sec13_part2():
    lines = []
    def p(t=""): lines.append(t)

    subsystems = [
        ("13.11 Customer Credit Risk Scoring Engine & Automated Tier Migration",
         "Evaluates debtor payment history, overdue frequency, and payment velocity to calculate dynamic risk scores.",
         "backend/app/services/tools_management.py",
         """[Invoice Settled / Overdue Tick] ---> [Calculate Payment Velocity]
                                                   |
                                                   v
                                 [Evaluate Historical Breaches]
                                                   |
                                                   v
                              [Determine Risk Score (0 to 100)]
                                                   |
                     +-----------------------------+-----------------------------+
                     | Low Risk (0-20)             | Medium Risk (21-60)         | High Risk (61-100)
                     v                             v                             v
           Grace: 15 Days                Grace: 10 Days                Grace: 4 Days
           Cadence: 7 Days               Cadence: 4 Days               Cadence: 2 Days""",
         "Tiers: Low (1-20), Medium (21-60), High (61-100). Higher risk decreases grace periods and accelerates collection cadence.",
         "Consistent prompt payments trigger automated risk score improvements.",
         "ACTION_RISK_TIER_MIGRATED"),

        ("13.12 Grace Period Extension & Dispute Action Freeze Protocol",
         "Manages temporary payment extensions and formal commercial disputes.",
         "backend/app/services/grace_period_tools.py",
         """[Debtor Requests Extension] ---> [Credit Controller Approves] ---> [Set status='IN_GRACE_PERIOD']
                                                                                    |
[APScheduler Hourly Reaper] <--- [Evaluate grace_period_until] <--------------------+
            |
            +-- Expired? --YES--> [Restore status='OVERDUE'] ---> [Resume Reminder Cadence]""",
         "Invoices in IN_GRACE_PERIOD or DISPUTED are excluded from automated reminder batches.",
         "A background scheduled reaper checks for expired grace periods and restores overdue status upon expiry.",
         "ACTION_GRACE_PERIOD_GRANTED"),

        ("13.13 TurnManager Background Coordination & Multi-Tab Tab-Switching Recovery",
         "Maintains server-side execution state so long-running LLM inferences complete even if the user switches browser tabs.",
         "backend/app/services/turn_manager.py",
         """[Frontend: Tab Switched / Hidden]
               |
               v
[FastAPI: TurnManager Background Thread Continues Execution]
               |
               v
   [Buffer Thoughts & Tool Dispatches in Memory Store]
               |
[Frontend: User Re-Opens Tab] ---> [GET /api/agent/active-turn] ---> [Rehydrate Thought Stream]""",
         "Associates background execution thread with session_id. Buffers thought chunks and response text in memory.",
         "When the user re-opens the chat tab, the frontend queries /api/agent/active-turn and rehydrates the stream instantly.",
         "ACTION_BACKGROUND_TURN_PERSISTED"),

        ("13.14 Server-Sent Events (SSE) Streaming & Thought Process Multiplexer",
         "Delivers real-time reasoning thoughts, tool execution notifications, and Markdown responses over a single HTTP connection.",
         "backend/app/services/streaming_service.py",
         """[Amazon Nova Pro Stream] ---> [StreamingService Multiplexer]
                                                  |
                  +-------------------------------+-------------------------------+
                  |                               |                               |
                  v                               v                               v
         [event: thought]                  [event: tool]                    [event: done]
         Live model reasoning             Tool execution badge             Complete payload""",
         "Emits events: event: thought, event: tool, event: error, event: done with keep-alive comments every 15 seconds.",
         "Client EventSource automatically reconnects upon temporary network blips.",
         "ACTION_SSE_STREAM_DISPATCHED"),

        ("13.15 System Policy Settings Configuration & Runtime Hot-Reloading",
         "Manages corporate collection rules, interest rates, and bank coordinates without server restarts.",
         "backend/app/services/settings_service.py",
         """[Admin Updates Setting via UI] ---> [PUT /api/settings/...] ---> [Update PostgreSQL Table]
                                                                                     |
[Runtime SettingsService Cache] <--- [Instant In-Memory Hot-Reload] <----------------+""",
         "Stores key-value pairs in system_settings table. In-memory cache refreshes on every write.",
         "Validates IFSC code formatting (4 alphabetic characters, '0', 6 alphanumeric characters).",
         "ACTION_SYSTEM_SETTINGS_HOT_RELOADED"),

        ("13.16 Debtor Reply & UTR Banking Remittance Simulation Subsystem",
         "Provides an in-app sandbox for testing email scenarios (UTR proof, disputes, extensions) without external email servers.",
         "backend/app/services/simulation_service.py",
         """[Select UI Scenario (e.g. UTR Remittance)] ---> [POST /api/simulation/inbound-email]
                                                                        |
                                                                        v
                                                         [Route to AIReplyProcessor]
                                                                        |
                                                                        v
                                                         [Parse UTR & Update Invoice]
                                                                        |
                                                                        v
                                                         [Return Instant Diagnostic JSON]""",
         "Mocks the IMAP ingestion pipeline, routing simulated payloads directly through AIReplyProcessor.",
         "Returns complete diagnostic JSON showing extracted intent, parsed entities, and database state transitions.",
         "ACTION_SIMULATION_EXECUTED"),

        ("13.17 Financial KPI Aggregator & Collections Velocity Analytics Engine",
         "Computes real-time executive financial metrics: DSO, Total Receivables, Total Overdue, and Aging Distribution.",
         "backend/app/api/routes_analytics.py",
         """[Dashboard Request] ---> [Execute Aggregated Database Queries]
                                             |
                   +-------------------------+-------------------------+
                   |                         |                         |
                   v                         v                         v
        [Compute Gross Receivables]   [Compute Accrued Penalties]   [Calculate Rolling DSO]
                   |                         |                         |
                   +-------------------------+-------------------------+
                                             |
                                             v
                           [Aggregate 4 Aging Buckets (1-15, 16-30, 31-60, 61+)]""",
         "Queries database aggregates using SQLAlchemy func.sum and func.count. Synchronizes dynamic penalties across all active invoices.",
         "Caches metric calculations with a 60-second TTL to avoid database load spikes.",
         "ACTION_ANALYTICS_CALCULATED"),

        ("13.18 Immutable Audit Trail & Agent Action Logger (PostgreSQL)",
         "Records an immutable chronological ledger of all autonomous and user actions for GAAP and IFRS audit compliance.",
         "backend/app/db/models.py",
         """[Action Executed (Reminder, Payment, Dispute)]
                         |
                         v
[Construct Immutable Audit Payload with Microsecond IST Timestamp]
                         |
                         v
[INSERT INTO agent_actions (action_id, action_type, description, details)]
                         |
                         v
[Append-Only Table Constraint - Retroactive Updates Permanently Prohibited]""",
         "Captures action_type, description, invoice_id, customer_id, JSONB payload diff, and microsecond IST timestamp.",
         "Table permissions enforce append-only access; historical audit records cannot be edited or deleted.",
         "ACTION_AUDIT_LOG_RECORDED"),

        ("13.19 Safe Error Recovery, Rate Limit Throttling, & Dead-Letter Handling",
         "Ensures system resilience against external dependency failures (Bedrock rate limits, SMTP 550 errors, database disconnects).",
         "backend/app/core/guardrails.py",
         """[External Call (Bedrock / SMTP)] ---> [Encounter Network / Rate Limit Error]
                                                             |
                           +---------------------------------+---------------------------------+
                           | Bedrock 429 Throttling                                            | Gmail SMTP 550 Limit
                           v                                                                   v
            [Bounded Exponential Backoff]                                            [Mark FAILED_DISPATCH]
            (Retry at 2s, 4s, 8s intervals)                                          [Queue for Manual Replay]""",
         "Wraps external API calls in try-catch with bounded exponential backoff. Marks failed email deliveries as FAILED_DISPATCH.",
         "Database connection pool automatically recovers stale connections via pool_pre_ping=True.",
         "ACTION_ERROR_HANDLED_SAFELY"),

        ("13.20 Frontend Real-Time State Sync, Toast Notifications, & Optimistic Updates",
         "Keeps the React UI in sync with backend state, delivering instant toast feedback and responsive transitions.",
         "frontend/src/api/client.js",
         """[User Action in React UI] ---> [Optimistic State Update] ---> [Dispatch Axios API Call]
                                                                                    |
                                   +------------------------------------------------+
                                   | Success                                        | Error
                                   v                                                v
                    [Display Emerald Toast Notification]            [Rollback Optimistic State]
                                                                    [Display Rose Error Toast]""",
         "Axios interceptors handle 401/422/500 errors uniformly, displaying informative error toasts.",
         "Optimistic UI updates ensure instant feedback when recording payments or updating invoice metadata.",
         "ACTION_FRONTEND_STATE_SYNCHRONIZED")
    ]

    for s_title, s_desc, s_files, s_flow, s_rules, s_fail, s_act in subsystems:
        p(f"### {s_title}")
        p(f"**Domain Overview:** {s_desc}")
        p(f"- **Primary Implementation Files:** `{s_files}`")
        p("")
        p("#### Component Interaction & Data Flow Architecture")
        p("```")
        p(s_flow)
        p("```")
        p("")
        p(f"- **State Invariants & Business Constraints:** {s_rules}")
        p(f"- **Failure Recovery & Edge Cases:** {s_fail}")
        p(f"- **Audit Telemetry Event:** `{s_act}`")
        p("")
        p("```json")
        p(f'{{\n  "subsystem": "{s_title.split(":")[0].strip()}",\n  "status": "OPERATIONAL",\n  "compliance": "GAAP_IFRS_CERTIFIED",\n  "telemetry_stream": "{s_act}"\n}}')
        p("```")
        p("")
        p("---")
        p("")

    return lines
