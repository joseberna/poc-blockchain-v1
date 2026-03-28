# ==========================================
# MASTER ENTRY POINT: FORENSIC KERNEL v4.0
# ==========================================

from flask import Flask, jsonify, request, render_template_string
from core.blockchain import BlockchainProtocol
from core.audit import log_event

# 1. UI DEFINITION (ATOMIC COMPONENT)
# ==========================================
MASTER_UI = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S.F.B.S | Forensic Blockchain Lab v.4</title>
    
    <!-- Pro Typography & Styling -->
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <script src="https://unpkg.com/@popperjs/core@2"></script>
    <script src="https://unpkg.com/tippy.js@6"></script>
    <link rel="stylesheet" href="https://unpkg.com/tippy.js@6/animations/scale.css"/>

    <style>
        :root {
            --bg: #0b0f1a;
            --glass: rgba(18, 24, 39, 0.85);
            --neon: #00f2fe;
            --neon-glow: rgba(0, 242, 254, 0.3);
            --danger: #ff4b2b;
            --purple: #8b5cf6;
            --text-main: #f1f5f9;
            --text-dim: #64748b;
            --mono: 'JetBrains Mono', monospace;
        }

        * { margin:0; padding:0; box-sizing: border-box; }
        body { 
            background: var(--bg); color: var(--text-main); font-family: 'Outfit', sans-serif;
            background-image: radial-gradient(circle at 10% 20%, rgba(0, 242, 254, 0.05), transparent 40%);
            min-height: 100vh; overflow-x: hidden; padding: 20px;
        }

        .workspace-grid {
            max-width: 1600px; margin: 0 auto;
            display: grid; grid-template-columns: repeat(12, 1fr); gap: 30px;
        }

        header { 
            grid-column: span 12; display: flex; justify-content: space-between; 
            align-items: center; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px;
        }
        .header-logo { font-family: var(--mono); font-weight: 700; color: var(--neon); letter-spacing: -1px; text-transform: uppercase; }

        .tower { 
            grid-column: span 4; background: var(--glass); backdrop-filter: blur(20px);
            border-radius: 24px; border: 1px solid rgba(255,255,255,0.05); padding: 40px;
            height: fit-content; box-shadow: 0 10px 40px rgba(0,0,0,0.6); position: sticky; top: 20px;
        }
        @media (max-width: 1200px) { .tower { grid-column: span 12; position: static; } }

        .control-group { margin-bottom: 24px; }
        .control-group label { display: block; font-size: 0.75rem; color: var(--text-dim); margin-bottom: 10px; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; }
        .control-group input { 
            width: 100%; background: #000; border: 1px solid rgba(255,255,255,0.1); padding: 14px 18px;
            border-radius: 12px; color: #fff; font-family: var(--mono); transition: 0.4s;
        }
        .control-group input:focus { border-color: var(--neon); outline: none; box-shadow: 0 0 20px var(--neon-glow); }

        .action-btn { 
            width: 100%; padding: 16px; border-radius: 14px; border: none; font-weight: 800; cursor: pointer; transition: 0.3s;
            text-transform: uppercase; letter-spacing: 1.5px;
        }
        .btn-neon { background: var(--neon); color: #000; box-shadow: 0 0 15px rgba(0,242,254,0.1); }
        .btn-neon:hover { transform: translateY(-3px); box-shadow: 0 10px 30px var(--neon-glow); background: #00e0ed; }
        .btn-mempool { background: transparent; border: 1px solid var(--purple); color: var(--purple); margin-top: 15px; }
        .btn-mempool:hover { background: var(--purple); color: white; }

        .timeline { grid-column: span 8; display: flex; flex-direction: column; gap: 40px; }
        @media (max-width: 1200px) { .timeline { grid-column: span 12; } }

        .protocol-bar { 
            background: rgba(255,255,255,0.02); padding: 25px 40px; border-radius: 20px;
            display: flex; align-items: center; justify-content: space-between; border: 1px dashed rgba(255,255,255,0.15);
        }

        .node { 
            background: var(--glass); border-radius: 28px; padding: 40px; border: 2px solid rgba(255,255,255,0.04);
            position: relative; transition: 0.7s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .node-secure { border-color: var(--neon); box-shadow: 0 0 60px rgba(0, 242, 254, 0.05); }
        .node-compromised { border-color: var(--danger); box-shadow: 0 0 60px rgba(255, 75, 43, 0.2); animation: glitching 0.15s infinite; }
        @keyframes glitching { 0% { transform: translate(1px, 1px); } 100% { transform: translate(-1px, -1px); } }

        .node-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .node-id { font-family: var(--mono); font-size: 2.2rem; font-weight: 900; color: var(--neon); }
        .node-badge { padding: 5px 15px; border-radius: 40px; font-size: 0.75rem; font-weight: 900; background: rgba(0,242,254,0.15); color: var(--neon); }

        .node-content { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        @media (max-width: 800px) { .node-content { grid-template-columns: 1fr; } }
        .info-label { text-transform: uppercase; font-size: 0.7rem; color: var(--text-dim); letter-spacing: 2px; margin-bottom: 15px; }
        .crypto-log { background: rgba(0,0,0,0.6); padding: 20px; border-radius: 16px; font-family: var(--mono); font-size: 0.8rem; word-break: break-all; color: #5eead4; border: 1px solid rgba(255,255,255,0.05); line-height: 1.6; }

        .node-connector { 
            position: absolute; left: 50%; bottom: -40px; width: 4px; height: 40px; 
            background: var(--neon); opacity: 0.2; transform: translateX(-50%);
        }
        .connector-alert { background: var(--danger); opacity: 1; animation: connector-pulse 1s infinite alternate; }
        @keyframes connector-pulse { from { opacity: 0.5; } to { opacity: 1; } }

        #mining-overlay {
            position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(11,15,26,0.98);
            z-index: 10000; display: none; align-items: center; justify-content: center; flex-direction: column;
        }
        .ring-spinner { width: 120px; height: 120px; border: 4px solid rgba(0,242,254,0.1); border-top: 4px solid var(--neon); border-radius: 50%; animation: rotation 0.7s linear infinite; }
        @keyframes rotation { to { transform: rotate(360deg); } }
        .swal2-dark-popup { background: var(--bg) !important; color: white !important; border: 1px solid var(--neon) !important; border-radius: 25px !important; }
    </style>
</head>
<body>
    <div id="mining-overlay">
        <div class="ring-spinner"></div>
        <h2 style="margin-top:30px; font-family: var(--mono); letter-spacing: 10px; color: var(--neon);">MINING_NODE</h2>
        <div id="live-hash-stream" style="margin-top:15px; font-family: var(--mono); font-size: 0.9rem; color: #2dd4bf; opacity: 0.6; word-break: break-all; max-width: 600px; text-align: center;"></div>
    </div>

    <div class="workspace-grid">
        <header>
            <div class="header-logo">FORENSIC_KERNEL <span style="opacity: 0.3;">NETWORK_V4</span></div>
            <div id="integrity-label" style="font-size: 0.75rem; font-weight: 900; color: var(--neon); border: 1px solid var(--neon); padding: 5px 15px; border-radius: 50px;">
                ● SYSTEM_HEALTH: 100%
            </div>
        </header>

        <aside class="tower">
            <h3 style="margin-bottom: 30px; font-size: 1.25rem; display: flex; align-items: center; gap: 10px;">
                Secure Transmitter <span data-tippy-content="Inyecta transacciones en el pool de memoria del nodo.">(?)</span>
            </h3>
            <div class="control-group"><label>Asset Origin</label><input type="text" id="tx-from" placeholder="User_Alfa_01"></div>
            <div class="control-group"><label>Asset Recipient</label><input type="text" id="tx-to" placeholder="Node_Gamma_Target"></div>
            <div class="control-group"><label>Quantum Value (CORE)</label><input type="number" id="tx-val" placeholder="0.00"></div>
            <button class="action-btn btn-neon" onclick="commitTransaction()">Initialize Transfer</button>
            <div style="margin-top: 50px;">
                <label>Pending Mempool <span data-tippy-content="Transacciones verificadas esperando ser minadas en un bloque.">(?)</span></label>
                <div id="mempool-stream" style="margin-top:15px; max-height: 250px; overflow-y: auto; padding-right: 5px;"></div>
                <button class="action-btn btn-mempool" onclick="triggerMining()">START_PROTOCOL_CONCENSUS</button>
            </div>
        </aside>

        <main class="timeline">
            <div class="protocol-bar">
                <div style="display: flex; align-items: center; gap: 20px;">
                    <label style="margin:0; font-size: 0.7rem; letter-spacing: 1px;">HAZARD_DIFFICULTY <span data-tippy-content="Dificultad del PoW.">(?)</span></label>
                    <input type="range" id="diff-slider" min="1" max="6" value="4" oninput="document.getElementById('diff-val').innerText = this.value" style="width: 180px; accent-color: var(--neon);">
                    <span id="diff-val" style="font-family: var(--mono); color: var(--neon); font-size: 1.2rem; font-weight: 700;">4</span>
                </div>
                <div style="font-size: 0.65rem; color: var(--text-dim); font-family: var(--mono);">CIPHER: SHA-256</div>
            </div>
            <div id="ledger-flow"></div>
        </main>
    </div>

    <script>
        tippy('[data-tippy-content]', { animation: 'scale', theme: 'custom' });
        const swalConfig = { background: '#0b0f1a', color: '#ffffff', customClass: { popup: 'swal2-dark-popup' }, confirmButtonColor: '#00f2fe' };

        async function request(path, method = 'GET', payload = null) {
            try {
                const config = { method };
                if (payload) { config.body = JSON.stringify(payload); config.headers = { 'Content-Type': 'application/json' }; }
                const response = await fetch(path, config);
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || 'Server Failure');
                return data;
            } catch (err) { Swal.fire({ ...swalConfig, icon: 'error', title: 'COMM_FAULT', text: err.message }); return null; }
        }

        async function commitTransaction() {
            const sender = document.getElementById('tx-from').value;
            const receiver = document.getElementById('tx-to').value;
            const amount = document.getElementById('tx-val').value;
            if(!sender || !receiver || !amount) return;
            const res = await request('/api/tx', 'POST', { sender, receiver, amount });
            if(res) { Swal.fire({ ...swalConfig, icon: 'success', title: 'PACKET_INJECTED', text: res.message, timer: 1200, showConfirmButton: false }); updateNodeState(); }
        }

        async function triggerMining() {
            const diff = document.getElementById('diff-slider').value;
            const overlay = document.getElementById('mining-overlay');
            const stream = document.getElementById('live-hash-stream');
            overlay.style.display = 'flex';
            const hashSim = setInterval(() => { stream.innerText = Array.from({length:64}, () => Math.floor(Math.random()*16).toString(16)).join(''); }, 60);
            const startTime = Date.now();
            const result = await request('/api/mine', 'POST', { difficulty: diff });
            clearInterval(hashSim); overlay.style.display = 'none';
            if(result) {
                const elapsed = ((Date.now() - startTime)/1000).toFixed(3);
                Swal.fire({ ...swalConfig, icon: 'success', title: 'BLOCK_INTEGRATED', html: `<div style="text-align:left; font-family: monospace; font-size:0.85rem; padding:10px;">ID: #${result.index}<br>NONCE: ${result.proof}<br>TIME: ${elapsed}s</div>` });
                updateNodeState();
            }
        }

        async function launchBreach(idx) {
            const { value: injection } = await Swal.fire({ ...swalConfig, title: 'CYBER_ATTACK_VECTOR', input: 'text', inputLabel: 'Insert malware data:', showCancelButton: true, confirmButtonColor: '#ff4b2b' });
            if (injection) {
                const res = await request('/api/hack', 'POST', { index: idx, malware: injection });
                if(res) { Swal.fire({ ...swalConfig, icon: 'warning', title: 'INFILTRATION_SUCCESS' }); updateNodeState(); }
            }
        }

        async function updateNodeState() {
            const node = await request('/api/status'); if(!node) return;
            document.getElementById('mempool-stream').innerHTML = node.mempool.map(tx => `<div style="font-size:0.75rem; padding:10px; background:rgba(255,255,255,0.04); border-radius:10px; margin-bottom:8px; border-left:3px solid var(--purple);"><strong>${tx.sender}</strong> → ${tx.receiver}<br><span style="color:var(--neon); opacity:0.8;">VALUE: ${tx.amount} CORE</span></div>`).join('');
            const intLabel = document.getElementById('integrity-label'); intLabel.innerText = node.integrity ? '● SYSTEM_HEALTH: 100%' : '● SYSTEM_HEALTH: COMPROMISED'; intLabel.style.color = node.integrity ? 'var(--neon)' : 'var(--danger)'; intLabel.style.borderColor = node.integrity ? 'var(--neon)' : 'var(--danger)';
            container = document.getElementById('ledger-flow');
            container.innerHTML = node.chain.map((block, i) => {
                const isCorrupt = node.invalid_indices.includes(i);
                return `
                <div style="position:relative;">
                    <div class="node ${isCorrupt ? 'node-compromised' : 'node-secure'}">
                        <div class="node-header"><div class="node-id">LEDGER_#${block.index}</div><span class="node-badge" ${isCorrupt ? 'style="color:var(--danger); background:rgba(255,75,43,0.15);"' : ''}>${isCorrupt ? '⚠️ ALERT_CORRUPTED' : '🛡️ VERIFIED'}</span></div>
                        <div class="node-content">
                            <div><div class="info-label">Manifest</div><div class="crypto-log" style="max-height:150px; overflow-y:auto;">${block.transactions.map(t => `<div>${t.sender.substring(0,8)}… ⇢ ${t.receiver.substring(0,8)}… <span style="float:right; color:var(--neon);">$${t.amount}</span></div>`).join('')}</div></div>
                            <div>
                                <div class="info-label">Hash_ID <span data-tippy-content="Hash SHA-256.">(?)</span></div><div class="crypto-log" style="font-size:0.7rem;">${block.hash}</div>
                                <div class="info-label" style="margin-top:20px;">Prev_Link</div><div class="crypto-log" style="font-size:0.7rem; opacity:0.4;">${block.previous_hash}</div>
                            </div>
                        </div>
                        <div style="margin-top:35px; display:flex; gap:20px; align-items:center;">
                            <button class="action-btn" style="width:auto; padding:10px 20px; border:1px solid var(--danger); color:var(--danger); background:transparent; font-size:0.75rem;" onclick="launchBreach(${i})">LAUNCH_INJECTION</button>
                            <span style="font-size:0.7rem; color:#64748b; font-family:monospace; opacity:0.6;">NONCE: ${block.proof}</span>
                        </div>
                    </div>
                    ${i < node.chain.length - 1 ? `<div class="node-connector ${isCorrupt ? 'connector-alert' : ''}"></div>` : ''}
                </div>`;
            }).reverse().join('');
            tippy('[data-tippy-content]', { animation: 'scale', theme: 'custom' });
        }
        updateNodeState();
    </script>
</body>
</html>
"""

# ==========================================
# 2. MASTER API LAYER (FLASK ROUTES)
# ==========================================

app = Flask(__name__)
# The node is initialized once
forensic_node = BlockchainProtocol()

@app.route('/')
def dashboard():
    return render_template_string(MASTER_UI)

@app.route('/api/tx', methods=['POST'])
def handle_transaction():
    data = request.get_json()
    if not data or not all(k in data for k in ['sender', 'receiver', 'amount']):
        return jsonify({"error": "INCOMPLETE_PACKET"}), 400
    try:
        idx = forensic_node.add_transaction(data['sender'], data['receiver'], data['amount'])
        log_event(f"Packet received for Block #{idx}")
        return jsonify({"message": f"Packet queued for Block #{idx}"}), 201
    except Exception as e:
        log_event(f"Error: {str(e)}", "error")
        return jsonify({"error": "FAULT"}), 500

@app.route('/api/mine', methods=['POST'])
def handle_mining():
    data = request.get_json()
    difficulty = int(data.get('difficulty', forensic_node.difficulty))
    try:
        last_block = forensic_node.get_last_block()
        proof = forensic_node.solve_pow(last_block.proof, difficulty)
        from core.block import Block as BlockModel
        prev_hash = BlockModel.calculate_hash(last_block.to_dict())
        block = forensic_node.create_block(proof, prev_hash)
        log_event(f"Block #{block.index} integrated.")
        return jsonify(block.to_dict()), 200
    except Exception as e:
        log_event(f"Mining error: {str(e)}", "error")
        return jsonify({"error": "FAULT"}), 500

@app.route('/api/hack', methods=['POST'])
def handle_hack():
    data = request.get_json()
    idx = int(data['index'])
    if 0 <= idx < len(forensic_node.chain):
        forensic_node.chain[idx].transactions = [{"sender": "HACKER", "receiver": "VOID", "amount": 0.0, "payload": data['malware']}]
        log_event(f"SECURITY_ALERT: Node #{idx+1} compromised!", "warning")
        return jsonify({"status": "SUCCESS"}), 200
    return jsonify({"error": "NOT_FOUND"}), 404

@app.route('/api/status', methods=['GET'])
def handle_status():
    is_valid, invalid_indices = forensic_node.validate_integrity()
    from core.block import Block as BlockModel
    ledger_state = []
    for b in forensic_node.chain:
        d = b.to_dict().copy()
        d['hash'] = BlockModel.calculate_hash(b.to_dict())
        ledger_state.append(d)
    return jsonify({"chain": ledger_state, "mempool": forensic_node.mempool, "integrity": is_valid, "invalid_indices": invalid_indices}), 200

if __name__ == '__main__':
    log_event("SFBS_NODE_ONLINE")
    app.run(host='0.0.0.0', port=5000, debug=True)
