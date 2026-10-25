"""
Section 11 and 12: Frontend Architecture & Component Directory, Mathematical Specifications.
"""

def generate_sec11_12():
    lines = []
    def p(t=""): lines.append(t)

    # SECTION 11: FRONTEND DIRECTORY
    p("## 11. Frontend UI/UX Architecture & Component Directory (18 Components)")
    p("")
    p("The React 18 single-page application is structured cleanly into feature pages, modal dialogs, and reusable UI components:")
    p("")

    components = [
        ("Layout.jsx", "Root Application Wrapper", "Shell containing responsive sidebar, top navbar, dynamic route outlet, and toast provider.",
         "useLocation for active route detection; ThemeContext for dark/light mode toggle.",
         """// Layout.jsx - Responsive application shell with glassmorphism sidebar
export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const toggleSidebar = () => setSidebarOpen(prev => !prev);

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans antialiased overflow-hidden">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Navbar toggleSidebar={toggleSidebar} />
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
          <div className="max-w-7xl mx-auto space-y-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}"""),

        ("Navbar.jsx", "Global Navigation Header", "Top navigation bar showing current page breadcrumbs, system operational status badge, quick actions, and user profile.",
         "useState for user dropdown menu; ThemeContext for theme styling.",
         """// Navbar.jsx - Global navigation header with status indicators
export default function Navbar({ toggleSidebar }) {
  const location = useLocation();
  const getPageTitle = (path) => {
    switch (path) {
      case "/": return "Executive Dashboard";
      case "/invoices": return "Invoice Management Ledger";
      case "/customers": return "Debtor Customer Directory";
      case "/approvals": return "Executive Approvals Queue";
      case "/activity": return "Agent Activity & Audit Trail";
      case "/chat": return "Interactive AR Intelligence Assistant";
      case "/settings": return "System Policy Settings";
      default: return "ReceivIQ Platform";
    }
  };

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/60 backdrop-blur-md px-6 flex items-center justify-between z-10">
      <div className="flex items-center gap-3">
        <button onClick={toggleSidebar} className="lg:hidden p-2 text-slate-400 hover:text-white rounded-lg">
          <Menu className="w-5 h-5" />
        </button>
        <h1 className="text-lg font-semibold text-white tracking-tight">{getPageTitle(location.pathname)}</h1>
        <span className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          Operational
        </span>
      </div>
    </header>
  );
}"""),

        ("Sidebar.jsx", "Main Sidebar Navigation", "Collapsible navigation sidebar with icons for Dashboard, Invoices, Customers, Approvals, Activity, Agent Chat, and Settings.",
         "NavLink hooks for active URL route highlighting.",
         """// Sidebar.jsx - Main navigation sidebar with active route highlighting
export default function Sidebar({ isOpen, toggleSidebar }) {
  const links = [
    { to: "/", label: "Dashboard", icon: LayoutDashboard },
    { to: "/invoices", label: "Invoices", icon: FileText },
    { to: "/customers", label: "Customers", icon: Users },
    { to: "/approvals", label: "Approvals", icon: ShieldAlert },
    { to: "/activity", label: "Activity", icon: Activity },
    { to: "/chat", label: "Agent Chat", icon: MessageSquare },
    { to: "/settings", label: "Settings", icon: Settings },
  ];

  return (
    <aside className={`fixed lg:static inset-y-0 left-0 z-30 w-64 bg-slate-900 border-r border-slate-800 p-4 transition-transform ${isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}`}>
      <div className="flex items-center gap-3 mb-8 px-2">
        <img src="/logo.png" className="w-9 h-9 rounded-lg shadow-lg" alt="ReceivIQ" />
        <div>
          <span className="font-bold text-white text-lg tracking-tight block">ReceivIQ</span>
          <span className="text-xs text-slate-400 block -mt-1">AR Intelligence</span>
        </div>
      </div>
      <nav className="space-y-1">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} className={({ isActive }) => `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${isActive ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white hover:bg-slate-800"}`}>
            <Icon className="w-4 h-4" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}"""),

        ("ChatMessageItem.jsx", "Chat Message Renderer", "Renders user prompts, AI replies, streaming thought processes, and pending action confirmation dialogs.",
         "useState for thought collapse/expand toggle; MarkdownRenderer for table and bold styling.",
         """// ChatMessageItem.jsx - Renders markdown messages with collapsible thought traces
export default function ChatMessageItem({ message, onConfirmAction, onCancelAction }) {
  const isUser = message.sender === "user";
  const [showThoughts, setShowThoughts] = useState(true);

  return (
    <div className={`flex gap-4 p-4 rounded-xl ${isUser ? "bg-indigo-600/10 border border-indigo-500/20" : "bg-slate-900 border border-slate-800"}`}>
      <div className="flex-1 space-y-3">
        {message.thought && (
          <div className="bg-slate-950/60 rounded-lg p-3 border border-slate-800/80">
            <button onClick={() => setShowThoughts(prev => !prev)} className="text-xs font-medium text-indigo-400 flex items-center gap-1.5">
              Thought process · {showThoughts ? "Hide" : "Show"}
            </button>
            {showThoughts && <div className="mt-2 text-xs text-slate-400 font-mono whitespace-pre-wrap">{message.thought}</div>}
          </div>
        )}
        <MarkdownRenderer content={message.text} />
        {message.pendingAction && (
          <div className="flex gap-3 pt-2">
            <button onClick={() => onConfirmAction(message.pendingAction)} className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg">Confirm & Dispatch</button>
            <button onClick={() => onCancelAction(message.pendingAction)} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-lg">Cancel</button>
          </div>
        )}
      </div>
    </div>
  );
}"""),

        ("ChatInputBar.jsx", "Chat Input & Action Controls", "Auto-resizing text area with submit button, credit balance counter, and suggested quick prompt chips.",
         "useState for input text; onKeyDown handler for Enter-to-send.",
         """// ChatInputBar.jsx - Natural language input with shortcut chips
export default function ChatInputBar({ onSend, isStreaming }) {
  const [input, setInput] = useState("");
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && !isStreaming) {
        onSend(input);
        setInput("");
      }
    }
  };

  return (
    <div className="border-t border-slate-800 bg-slate-900/80 p-4 space-y-3">
      <div className="flex gap-2">
        <textarea rows={1} value={input} onChange={e => setInput(e.target.value)} onKeyDown={handleKeyDown} placeholder="Ask about overdue accounts, customer risks, or draft reminders..." className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none" />
        <button onClick={() => { if (input.trim() && !isStreaming) { onSend(input); setInput(""); } }} disabled={isStreaming || !input.trim()} className="px-5 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-lg font-medium text-sm transition">
          {isStreaming ? <Loader2 className="w-4 h-4 animate-spin" /> : "Send"}
        </button>
      </div>
    </div>
  );
}"""),

        ("ChatSidebar.jsx", "Chat Session History Panel", "Lists historical multi-turn chat sessions with timestamps, title editing, and session switching.",
         "useState for sessions list; onSelectSession callback.",
         """// ChatSidebar.jsx - Multi-session history sidebar
export default function ChatSidebar({ sessions, activeSessionId, onSelectSession, onNewSession }) {
  return (
    <div className="w-64 border-r border-slate-800 bg-slate-900/50 p-4 flex flex-col h-full">
      <button onClick={onNewSession} className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-indigo-600/20 text-indigo-300 hover:bg-indigo-600/30 border border-indigo-500/30 rounded-lg text-sm font-semibold transition mb-4">
        + New Session
      </button>
      <div className="flex-1 overflow-y-auto space-y-1">
        {sessions.map(s => (
          <button key={s.id} onClick={() => onSelectSession(s.id)} className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium truncate ${s.id === activeSessionId ? "bg-slate-800 text-white" : "text-slate-400 hover:text-white hover:bg-slate-800/50"}`}>
            {s.title || "New Chat"}
          </button>
        ))}
      </div>
    </div>
  );
}"""),

        ("MarkdownRenderer.jsx", "Markdown & Table Formatter", "Parses agent Markdown output into rich HTML tables, bulleted lists, and formatted code snippets.",
         "React-markdown plugin pipeline.",
         """// MarkdownRenderer.jsx - Renders tables and bold text cleanly
export default function MarkdownRenderer({ content }) {
  return (
    <div className="prose prose-invert max-w-none text-sm leading-relaxed prose-table:border prose-table:border-slate-800 prose-th:bg-slate-800/50 prose-th:p-2 prose-td:p-2 prose-td:border-t prose-td:border-slate-800">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
}"""),

        ("ActivityCard.jsx", "Audit Feed Event Item", "Renders a single immutable audit event with action badge, debtor name, IST timestamp, and expandable JSON details.",
         "useState for modal payload inspection.",
         """// ActivityCard.jsx - Immutable audit record item
export default function ActivityCard({ action, onInspectPayload }) {
  return (
    <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition flex items-start gap-4">
      <div className="p-2.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
        <Activity className="w-5 h-5" />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-white truncate">{action.description}</p>
        <span className="text-xs text-slate-500 font-mono mt-1 block">{action.time_ist}</span>
      </div>
      <button onClick={() => onInspectPayload(action.details)} className="px-3 py-1.5 text-xs text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg">Inspect</button>
    </div>
  );
}"""),

        ("CreateInvoiceModal.jsx", "Invoice Creation Dialog", "Form modal for creating new receivables with debtor select, principal amount, invoice date, and due date.",
         "useState for formData; Pydantic error validation.",
         """// CreateInvoiceModal.jsx - Issues new invoice with validation
export default function CreateInvoiceModal({ isOpen, onClose, customers, onInvoiceCreated }) {
  const [formData, setFormData] = useState({ customer_id: "", amount: "", due_date: "", notes: "" });
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl">
        <h2 className="text-lg font-bold text-white mb-4">Issue New Commercial Invoice</h2>
        <form onSubmit={e => { e.preventDefault(); onInvoiceCreated(formData); onClose(); }} className="space-y-4">
          <select value={formData.customer_id} onChange={e => setFormData({...formData, customer_id: e.target.value})} className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white" required>
            <option value="">Select Debtor...</option>
            {customers.map(c => <option key={c.customer_id} value={c.customer_id}>{c.company_name}</option>)}
          </select>
          <input type="number" placeholder="Principal Amount (₹)" value={formData.amount} onChange={e => setFormData({...formData, amount: e.target.value})} className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white" required />
          <input type="date" value={formData.due_date} onChange={e => setFormData({...formData, due_date: e.target.value})} className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white" required />
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm text-slate-400 hover:text-white">Cancel</button>
            <button type="submit" className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold">Issue Invoice</button>
          </div>
        </form>
      </div>
    </div>
  );
}"""),

        ("EditInvoiceModal.jsx", "Invoice Term Modification Dialog", "Form modal allowing credit controllers to adjust due dates, notes, and commercial terms for unsettled invoices.",
         "useState for edited fields; onSubmit PUT to /api/invoices/{id}.",
         """// EditInvoiceModal.jsx - Modifies due date and notes
export default function EditInvoiceModal({ isOpen, onClose, invoice, onSaved }) {
  const [dueDate, setDueDate] = useState(invoice?.due_date || "");
  const [notes, setNotes] = useState(invoice?.notes || "");
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4">Edit Invoice {invoice?.invoice_id}</h2>
        <input type="date" value={dueDate} onChange={e => setDueDate(e.target.value)} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white mb-4" />
        <textarea value={notes} onChange={e => setNotes(e.target.value)} placeholder="Commercial notes" className="w-full bg-slate-800 rounded p-2.5 text-sm text-white mb-4" />
        <button onClick={() => { onSaved({ due_date: dueDate, notes }); onClose(); }} className="w-full py-2 bg-indigo-600 text-white rounded font-medium">Save Changes</button>
      </div>
    </div>
  );
}"""),

        ("CreateCustomerModal.jsx", "Debtor Onboarding Dialog", "Form modal to onboard a new corporate debtor with company name, contact officer, billing email, phone, and credit limit.",
         "useState for customer data; Pydantic validation error handling.",
         """// CreateCustomerModal.jsx - Onboards new debtor
export default function CreateCustomerModal({ isOpen, onClose, onCreated }) {
  const [customer, setCustomer] = useState({ name: "", company_name: "", email: "", phone: "", risk_level: "Low" });
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <h2 className="text-lg font-bold text-white">Onboard New Corporate Debtor</h2>
        <input placeholder="Company Name" value={customer.company_name} onChange={e => setCustomer({...customer, company_name: e.target.value})} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white" />
        <input placeholder="Contact Officer Name" value={customer.name} onChange={e => setCustomer({...customer, name: e.target.value})} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white" />
        <input placeholder="Billing Email" type="email" value={customer.email} onChange={e => setCustomer({...customer, email: e.target.value})} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white" />
        <button onClick={() => { onCreated(customer); onClose(); }} className="w-full py-2 bg-indigo-600 text-white rounded font-medium">Onboard Debtor</button>
      </div>
    </div>
  );
}"""),

        ("EditCustomerModal.jsx", "Debtor Profile Editor", "Form modal allowing updates to contact officer coordinates, phone, address, and risk tier.",
         "useState for edited customer fields; PUT to /api/customers/{id}.",
         """// EditCustomerModal.jsx - Updates contact details and risk tier
export default function EditCustomerModal({ isOpen, onClose, customer, onUpdated }) {
  const [data, setData] = useState({ ...customer });
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <h2 className="text-lg font-bold text-white">Edit Debtor Profile</h2>
        <input value={data.name} onChange={e => setData({...data, name: e.target.value})} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white" />
        <select value={data.risk_level} onChange={e => setData({...data, risk_level: e.target.value})} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white">
          <option value="Low">Low Risk</option><option value="Medium">Medium Risk</option><option value="High">High Risk</option>
        </select>
        <button onClick={() => { onUpdated(data); onClose(); }} className="w-full py-2 bg-indigo-600 text-white rounded font-medium">Update Profile</button>
      </div>
    </div>
  );
}"""),

        ("PaymentModal.jsx", "Payment Remittance Dialog", "Form modal to record direct payments with amount paid, payment method (NEFT/RTGS/IMPS/Cheque), and bank UTR reference.",
         "useState for payment fields; POST to /api/invoices/{id}/pay.",
         """// PaymentModal.jsx - Records payment remittance with UTR
export default function PaymentModal({ isOpen, onClose, invoice, onPaymentRecorded }) {
  const [amount, setAmount] = useState(invoice?.total_amount || 0);
  const [method, setMethod] = useState("NEFT");
  const [utr, setUtr] = useState("");
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <h2 className="text-lg font-bold text-white">Record Remittance - {invoice?.invoice_id}</h2>
        <input type="number" value={amount} onChange={e => setAmount(Number(e.target.value))} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white" />
        <input placeholder="Bank UTR Number (e.g. SBIN00928374)" value={utr} onChange={e => setUtr(e.target.value)} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white" />
        <button onClick={() => { onPaymentRecorded({ amount, payment_method: method, reference_number: utr }); onClose(); }} className="w-full py-2 bg-emerald-600 text-white rounded font-medium">Record Payment</button>
      </div>
    </div>
  );
}"""),

        ("ReplySimulatorModal.jsx", "Debtor Email Simulator Modal", "Interactive testing sandbox allowing team members to simulate incoming debtor emails with UTR proofs or disputes.",
         "useState for scenarioId, customBody, simulationResult; POST to /api/simulation/inbound-email.",
         """// ReplySimulatorModal.jsx - Sandbox for inbound debtor replies
export default function ReplySimulatorModal({ isOpen, onClose, invoices, onSimulate }) {
  const [invId, setInvId] = useState("");
  const [scenario, setScenario] = useState("PAYMENT_PROOF_UTR");
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <h2 className="text-lg font-bold text-white">Simulate Inbound Debtor Email</h2>
        <select value={invId} onChange={e => setInvId(e.target.value)} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white">
          <option value="">Select Invoice...</option>
          {invoices.map(i => <option key={i.invoice_id} value={i.invoice_id}>{i.invoice_id} - {i.company_name}</option>)}
        </select>
        <button onClick={() => { onSimulate({ invoice_id: invId, scenario }); }} className="w-full py-2 bg-indigo-600 text-white rounded font-medium">Run Simulation</button>
      </div>
    </div>
  );
}"""),

        ("PenaltySettingsTab.jsx", "Late Penalty Settings Form", "Settings form for configuring late penalty interest rate percentage (default: 2.0%) and compounding cycle duration (default: 30 days).",
         "Controlled form state synced with parent Settings page.",
         """// PenaltySettingsTab.jsx - Configure late penalty calculation rules
export default function PenaltySettingsTab({ settings, onSave }) {
  const [rate, setRate] = useState(settings?.rate || 2.0);
  return (
    <div className="p-6 space-y-4">
      <input type="number" step="0.1" value={rate} onChange={e => setRate(Number(e.target.value))} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white" />
      <button onClick={() => onSave({ rate })} className="px-4 py-2 bg-indigo-600 text-white rounded text-sm font-semibold">Save Penalty Rules</button>
    </div>
  );
}"""),

        ("RemindersSettingsTab.jsx", "Collection Cadence Form", "Settings form to configure reminder intervals, maximum notices before legal escalation, and dispute pausing per risk tier.",
         "Controlled form state synced with parent Settings page.",
         """// RemindersSettingsTab.jsx - Configure collection cadence
export default function RemindersSettingsTab({ settings, onSave }) {
  const [interval, setInterval] = useState(settings?.interval_days || 7);
  return (
    <div className="p-6 space-y-4">
      <input type="number" value={interval} onChange={e => setInterval(Number(e.target.value))} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white" />
      <button onClick={() => onSave({ interval_days: interval })} className="px-4 py-2 bg-indigo-600 text-white rounded text-sm font-semibold">Save Cadence</button>
    </div>
  );
}"""),

        ("BankSettingsTab.jsx", "Bank Remittance Settings Form", "Settings form for beneficiary legal entity name, bank name, account number, confirm account number, and IFSC code.",
         "Controlled form state with IFSC regex validation.",
         """// BankSettingsTab.jsx - Manage corporate remittance coordinates
export default function BankSettingsTab({ bank, onSave }) {
  const [ifsc, setIfsc] = useState(bank?.ifsc_code || "");
  return (
    <div className="p-6 space-y-4">
      <input placeholder="IFSC Code (e.g. SBIN0001234)" value={ifsc} onChange={e => setIfsc(e.target.value.toUpperCase())} className="w-full bg-slate-800 rounded p-2.5 text-sm text-white" />
      <button onClick={() => onSave({ ifsc_code: ifsc })} className="px-4 py-2 bg-indigo-600 text-white rounded text-sm font-semibold">Save Bank Details</button>
    </div>
  );
}"""),

        ("AgentSettingsTab.jsx", "AI Agent Master Control Form", "Settings form featuring master toggle switch to pause autonomous operations, background polling, and chat reasoning.",
         "Controlled toggle switch synced with PUT /api/settings/agent.",
         """// AgentSettingsTab.jsx - Master toggle for AI agent operations
export default function AgentSettingsTab({ enabled, onToggle }) {
  return (
    <div className="p-6 space-y-4">
      <label className="flex items-center gap-3 cursor-pointer">
        <input type="checkbox" checked={enabled} onChange={e => onToggle(e.target.checked)} className="w-4 h-4 text-indigo-600 rounded" />
        <span className="text-white font-medium">Autonomous Agent Operations Enabled</span>
      </label>
    </div>
  );
}""")
    ]

    for c_file, c_name, c_desc, c_state, c_jsx in components:
        p(f"### 11.{components.index((c_file, c_name, c_desc, c_state, c_jsx))+1} Component: `{c_file}` ({c_name})")
        p(f"- **File Location:** `frontend/src/components/{c_file}` (or `pages/{c_file}`)")
        p(f"- **Purpose:** {c_desc}")
        p(f"- **React State & Hooks:** {c_state}")
        p("")
        p("```jsx")
        p(c_jsx)
        p("```")
        p("")

    p("---")
    p("")

    # SECTION 12: MATHEMATICAL FORMULAS
    p("## 12. Mathematical & Financial Computation Specifications")
    p("")
    p("All financial algorithms in ReceivIQ are specified below with strict algebraic definitions:")
    p("")
    p("### 12.1 Dynamic Simple Interest Late Penalty Formula")
    p("```")
    p("If Days Overdue <= Grace Period Days:")
    p("    Accrued Penalty = ₹0.00")
    p("Else:")
    p("    Accrued Penalty = Principal * (Penalty Rate % / 100) * (Days Overdue / Cycle Days)")
    p("    Total Outstanding = Principal + Accrued Penalty")
    p("```")
    p("**Worked Example:**")
    p("- Principal: ₹2,50,000.00")
    p("- Due Date: 2026-10-04; Evaluation Date: 2026-10-25 (21 Days Overdue)")
    p("- Grace Period: 4 Days (High Risk); Late Penalty Rate: 2.0% per 30 Days")
    p("- Accrued Penalty = 250,000 * 0.02 * (21 / 30) = ₹3,500.00 (or ₹12,500 under 5.0% high-risk tier)")
    p("- Total Balance Due = ₹2,53,500.00")
    p("")
    p("### 12.2 Days Sales Outstanding (DSO) Formula")
    p("```")
    p("DSO = (Total Outstanding Accounts Receivable / Total Gross Credit Sales in Period) * Number of Days in Period")
    p("```")
    p("**Standard Period:** 90 Days (rolling quarterly). Lower DSO reflects superior credit collection velocity.")
    p("")
    p("### 12.3 Time-Bound Early Settlement Discount Formula")
    p("```")
    p("Discount Amount = Principal * (Discount Percentage / 100)")
    p("Settlement Balance = Total Outstanding - Discount Amount")
    p("```")
    p("**Constraint:** `0.1% <= Discount Percentage <= 0.5%`. Enforces minimum gross margin preservation.")
    p("")
    p("### 12.4 Partial Payment Allocation Waterfall")
    p("When a debtor remits partial payment ($P_{remit} < Total Outstanding$):")
    p("1. First allocated to accrued late penalties: $P_{penalty} = \\min(P_{remit}, Accrued Penalty)$.")
    p("2. Remainder allocated to principal: $P_{principal} = P_{remit} - P_{penalty}$.")
    p("3. Residual principal balance remains in status `OVERDUE` with accrued penalty reset for subsequent cycles.")
    p("")
    p("---")
    p("")

    return lines
