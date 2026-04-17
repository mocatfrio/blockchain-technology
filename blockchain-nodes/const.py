TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ node_name }} - Blockchain 3 Nodes</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f4f7fb; color: #1f2937; }
    .container { max-width: 1250px; margin: 0 auto; padding: 24px; }
    .topbar { display:flex; justify-content:space-between; gap:16px; align-items:center; flex-wrap:wrap; }
    .grid { display:grid; grid-template-columns: 360px 1fr; gap: 20px; margin-top: 18px; }
    .card { background:#fff; border-radius:16px; padding:18px; box-shadow:0 8px 24px rgba(0,0,0,.08); margin-bottom:18px; }
    .message { padding:12px; border-radius:12px; margin: 14px 0; }
    .success { background:#dcfce7; color:#166534; }
    .error { background:#fee2e2; color:#991b1b; }
    .warning { background:#fef3c7; color:#92400e; }
    h1, h2, h3 { margin-top:0; }
    input, textarea, button { width:100%; box-sizing:border-box; padding:10px 12px; margin-top:8px; margin-bottom:12px; border:1px solid #d1d5db; border-radius:10px; }
    button { cursor:pointer; background:#111827; color:#fff; font-weight:700; }
    button:hover { opacity:.94; }
    .secondary { background:#2563eb; }
    .danger { background:#dc2626; }
    .pill { display:inline-block; padding:6px 10px; border-radius:999px; font-size:12px; font-weight:700; }
    .valid { background:#dcfce7; color:#166534; }
    .invalid { background:#fee2e2; color:#991b1b; }
    .muted { color:#6b7280; font-size:14px; }
    .block { border:1px solid #e5e7eb; border-radius:14px; padding:16px; margin-bottom:16px; background:#fff; }
    .hash { font-family: monospace; font-size:12px; word-break:break-all; background:#f3f4f6; padding:8px; border-radius:8px; }
    ul { padding-left:18px; }
    .row { display:grid; grid-template-columns: 1fr 1fr; gap:12px; }
    @media (max-width: 900px) { .grid, .row { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="container">
    <div class="topbar">
      <div>
        <h1>{{ node_name }}</h1>
        <div class="muted">UI sederhana untuk simulasi blockchain 3 node berbasis Flask.</div>
      </div>
      <div>
        {% if valid %}
          <span class="pill valid">VALID</span>
        {% else %}
          <span class="pill invalid">INVALID</span>
        {% endif %}
      </div>
    </div>

    {% if message %}
      <div class="message {{ category }}">{{ message }}</div>
    {% endif %}

    <div class="grid">
      <div>
        <div class="card">
          <h2>Tambah / Broadcast Transaksi</h2>
          <form method="post" action="/ui/transaction">
            <label>Sender</label>
            <input name="sender" placeholder="Alice" required>
            <label>Recipient</label>
            <input name="recipient" placeholder="Bob" required>
            <label>Amount</label>
            <input name="amount" type="number" step="0.01" placeholder="10" required>
            <label><input type="checkbox" name="broadcast" checked style="width:auto; margin-right:8px;"> Broadcast ke node lain</label>
            <button type="submit">Kirim Transaksi</button>
          </form>
        </div>

        <div class="card">
          <h2>Mining</h2>
          <form method="post" action="/ui/mine">
            <label>Miner Address</label>
            <input name="miner" placeholder="Miner-A" required>
            <button class="secondary" type="submit">Mine Pending Transactions</button>
          </form>
          <p class="muted">Difficulty: <strong>{{ difficulty }}</strong></p>
        </div>

        <div class="card">
          <h2>Register Node</h2>
          <form method="post" action="/ui/register_nodes">
            <label>Daftar node (satu per baris)</label>
            <textarea name="nodes" rows="4" placeholder="http://127.0.0.1:5002\nhttp://127.0.0.1:5003"></textarea>
            <button type="submit">Register Nodes</button>
          </form>
        </div>

        <div class="card">
          <h2>Consensus</h2>
          <form method="post" action="/ui/resolve">
            <button class="secondary" type="submit">Resolve Conflicts</button>
          </form>
        </div>

        <div class="card">
          <h2>Simulasi Tamper</h2>
          <form method="post" action="/ui/tamper">
            <div class="row">
              <div>
                <label>Index Block</label>
                <input name="index" type="number" min="1" placeholder="1" required>
              </div>
              <div>
                <label>New Amount</label>
                <input name="new_amount" type="number" step="0.01" placeholder="9999" required>
              </div>
            </div>
            <button class="danger" type="submit">Tamper Block</button>
          </form>
        </div>
      </div>

      <div>
        <div class="card">
          <h2>Status Node</h2>
          <p><strong>Chain length:</strong> {{ chain|length }}</p>
          <p><strong>Pending transactions:</strong> {{ pending|length }}</p>
          <p><strong>Connected nodes:</strong> {{ nodes|length }}</p>
          <p><strong>Validation:</strong> {{ validation_message }}</p>
        </div>

        <div class="card">
          <h2>Connected Nodes</h2>
          {% if nodes %}
            <ul>
              {% for node in nodes %}
                <li>{{ node }}</li>
              {% endfor %}
            </ul>
          {% else %}
            <p class="muted">Belum ada node terhubung.</p>
          {% endif %}
        </div>

        <div class="card">
          <h2>Pending Transactions</h2>
          {% if pending %}
            <ul>
              {% for tx in pending %}
                <li>{{ tx.sender }} → {{ tx.recipient }} : {{ tx.amount }}</li>
              {% endfor %}
            </ul>
          {% else %}
            <p class="muted">Belum ada transaksi pending.</p>
          {% endif %}
        </div>

        <div class="card">
          <h2>Blockchain Explorer</h2>
          {% for block in chain %}
            <div class="block">
              <h3>Block #{{ block.index }}</h3>
              <p><strong>Timestamp:</strong> {{ block.timestamp }}</p>
              <p><strong>Nonce:</strong> {{ block.nonce }}</p>
              <p><strong>Previous Hash:</strong></p>
              <div class="hash">{{ block.previous_hash }}</div>
              <p><strong>Hash:</strong></p>
              <div class="hash">{{ block.hash }}</div>
              <p><strong>Transactions:</strong></p>
              <ul>
                {% if block.transactions %}
                  {% for tx in block.transactions %}
                    <li>{{ tx.sender }} → {{ tx.recipient }} : {{ tx.amount }}</li>
                  {% endfor %}
                {% else %}
                  <li>Genesis block tidak punya transaksi.</li>
                {% endif %}
              </ul>
            </div>
          {% endfor %}
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""
