from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

# ── Environment Variables ──────────────────────
ENVIRONMENT  = os.environ.get('ENVIRONMENT',  'production')
BUILD_NUMBER = os.environ.get('BUILD_NUMBER', 'local')
SERVER       = os.environ.get('SERVER',       'PC2')

# ── HTML Template (inline — no separate file needed) ──
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC2 — Jenkins Slave Server</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0a0a1a, #1a0a2e, #0a1a2e);
            min-height: 100vh;
            color: #e2e8f0;
        }

        /* ── Navbar ── */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px 40px;
            background: rgba(0,0,0,0.4);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(139,92,246,0.3);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav-brand {
            font-size: 1.4em;
            font-weight: bold;
            color: #a78bfa;
        }

        .nav-server {
            background: rgba(139,92,246,0.2);
            border: 1px solid rgba(139,92,246,0.4);
            color: #a78bfa;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }

        .nav-links a {
            color: #94a3b8;
            text-decoration: none;
            margin-left: 25px;
            font-size: 0.9em;
            transition: color 0.2s;
        }

        .nav-links a:hover { color: #a78bfa; }

        /* ── Hero ── */
        .hero {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 60px 20px 40px;
            text-align: center;
        }

        .server-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(139,92,246,0.15);
            border: 1px solid rgba(139,92,246,0.4);
            color: #a78bfa;
            padding: 8px 20px;
            border-radius: 30px;
            font-size: 0.9em;
            font-weight: bold;
            margin-bottom: 25px;
        }

        .dot {
            width: 8px;
            height: 8px;
            background: #a78bfa;
            border-radius: 50%;
            animation: blink 1.5s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.3; }
        }

        h1 {
            font-size: 3em;
            color: #fff;
            margin-bottom: 12px;
            line-height: 1.2;
        }

        h1 span { color: #a78bfa; }

        .subtitle {
            color: #94a3b8;
            font-size: 1.1em;
            margin-bottom: 50px;
            max-width: 600px;
        }

        /* ── Info Cards ── */
        .info-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            max-width: 900px;
            width: 100%;
            margin-bottom: 50px;
        }

        .info-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(139,92,246,0.2);
            border-radius: 15px;
            padding: 25px 20px;
            text-align: center;
            transition: all 0.3s;
        }

        .info-card:hover {
            border-color: rgba(139,92,246,0.6);
            background: rgba(139,92,246,0.08);
            transform: translateY(-4px);
        }

        .info-icon  { font-size: 2em; margin-bottom: 10px; }
        .info-label { color: #64748b; font-size: 0.8em; margin-bottom: 6px; }
        .info-value { color: #a78bfa; font-size: 1.2em; font-weight: bold; }

        /* ── Pipeline Flow ── */
        .pipeline-section {
            max-width: 900px;
            width: 100%;
            margin-bottom: 40px;
        }

        .section-title {
            color: #fff;
            font-size: 1.3em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(139,92,246,0.3);
        }

        .pipeline-flow {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(139,92,246,0.2);
            border-radius: 15px;
            padding: 25px;
            flex-wrap: wrap;
        }

        .pipeline-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            padding: 12px 16px;
        }

        .step-icon  { font-size: 1.8em; }
        .step-name  { color: #a78bfa; font-size: 0.75em; font-weight: bold; text-align: center; }
        .step-arrow { color: #4c1d95; font-size: 1.5em; padding: 0 5px; }

        /* ── Endpoints ── */
        .endpoints-section {
            max-width: 900px;
            width: 100%;
            margin-bottom: 40px;
        }

        .endpoint-list {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .endpoint-item {
            display: flex;
            align-items: center;
            gap: 15px;
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(139,92,246,0.2);
            border-radius: 12px;
            padding: 15px 20px;
            text-decoration: none;
            transition: all 0.2s;
        }

        .endpoint-item:hover {
            border-color: rgba(139,92,246,0.6);
            background: rgba(139,92,246,0.08);
            transform: translateX(5px);
        }

        .method-badge {
            background: rgba(139,92,246,0.3);
            color: #a78bfa;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75em;
            font-weight: bold;
            font-family: monospace;
            white-space: nowrap;
            border: 1px solid rgba(139,92,246,0.4);
        }

        .endpoint-path {
            color: #7dd3fc;
            font-family: monospace;
            font-size: 0.9em;
            flex: 1;
        }

        .endpoint-desc {
            color: #64748b;
            font-size: 0.8em;
        }

        /* ── Build Info ── */
        .build-section {
            max-width: 900px;
            width: 100%;
            margin-bottom: 40px;
        }

        .build-card {
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(139,92,246,0.2);
            border-radius: 15px;
            padding: 25px;
        }

        .build-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .build-row:last-child { border-bottom: none; }
        .build-label { color: #64748b; font-size: 0.9em; }

        .build-value {
            color: #e2e8f0;
            font-family: monospace;
            font-size: 0.9em;
        }

        .badge-purple {
            background: rgba(139,92,246,0.2);
            color: #a78bfa;
            border: 1px solid rgba(139,92,246,0.3);
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.8em;
        }

        .badge-green {
            background: rgba(22,163,74,0.2);
            color: #4ade80;
            border: 1px solid rgba(22,163,74,0.3);
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.8em;
        }

        /* ── Footer ── */
        .footer {
            text-align: center;
            padding: 30px;
            color: #475569;
            font-size: 0.85em;
            border-top: 1px solid rgba(139,92,246,0.2);
            line-height: 2;
            margin-top: 20px;
        }

        .footer span { color: #a78bfa; }

        /* ── Responsive ── */
        @media (max-width: 600px) {
            .info-grid      { grid-template-columns: repeat(2, 1fr); }
            .endpoint-list  { grid-template-columns: 1fr; }
            h1              { font-size: 2em; }
            .pipeline-flow  { flex-direction: column; }
            .step-arrow     { transform: rotate(90deg); }
        }
    </style>
</head>
<body>

    <nav class="navbar">
        <div class="nav-brand">🖥️ PC2 Slave Server</div>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/health">Health</a>
            <a href="/version">Version</a>
            <a href="/dashboard">Dashboard</a>
        </div>
        <div class="nav-server">{{ server }}</div>
    </nav>

    <div class="hero">
        <div class="server-badge">
            <div class="dot"></div>
            LIVE — Deployed by Jenkins from PC1
        </div>

        <h1>Friend's <span>PC2</span> Server</h1>
        <p class="subtitle">
            This server is controlled and deployed by Jenkins running on PC1.
            Every build on PC1 automatically reflects here.
        </p>

        <!-- Info Cards -->
        <div class="info-grid">
            <div class="info-card">
                <div class="info-icon">🖥️</div>
                <div class="info-label">Server</div>
                <div class="info-value">{{ server }}</div>
            </div>
            <div class="info-card">
                <div class="info-icon">🌍</div>
                <div class="info-label">Environment</div>
                <div class="info-value">{{ environment }}</div>
            </div>
            <div class="info-card">
                <div class="info-icon">🔢</div>
                <div class="info-label">Build</div>
                <div class="info-value">#{{ build }}</div>
            </div>
            <div class="info-card">
                <div class="info-icon">✅</div>
                <div class="info-label">Status</div>
                <div class="info-value">Running</div>
            </div>
        </div>

        <!-- Pipeline Flow -->
        <div class="pipeline-section">
            <div class="section-title">🔄 How This Got Deployed</div>
            <div class="pipeline-flow">
                <div class="pipeline-step">
                    <div class="step-icon">💻</div>
                    <div class="step-name">PC1<br>Code Push</div>
                </div>
                <div class="step-arrow">→</div>
                <div class="pipeline-step">
                    <div class="step-icon">🐙</div>
                    <div class="step-name">GitHub<br>Webhook</div>
                </div>
                <div class="step-arrow">→</div>
                <div class="pipeline-step">
                    <div class="step-icon">⚙️</div>
                    <div class="step-name">Jenkins<br>Pipeline</div>
                </div>
                <div class="step-arrow">→</div>
                <div class="pipeline-step">
                    <div class="step-icon">🧪</div>
                    <div class="step-name">Tests<br>Pass</div>
                </div>
                <div class="step-arrow">→</div>
                <div class="pipeline-step">
                    <div class="step-icon">🐳</div>
                    <div class="step-name">Docker<br>Build</div>
                </div>
                <div class="step-arrow">→</div>
                <div class="pipeline-step">
                    <div class="step-icon">🖥️</div>
                    <div class="step-name">PC2<br>Deploy</div>
                </div>
            </div>
        </div>

        <!-- Endpoints -->
        <div class="endpoints-section">
            <div class="section-title">🔌 API Endpoints</div>
            <div class="endpoint-list">
                <a href="/" class="endpoint-item">
                    <span class="method-badge">GET</span>
                    <span class="endpoint-path">/</span>
                    <span class="endpoint-desc">Home page</span>
                </a>
                <a href="/health" class="endpoint-item">
                    <span class="method-badge">GET</span>
                    <span class="endpoint-path">/health</span>
                    <span class="endpoint-desc">Health check</span>
                </a>
                <a href="/version" class="endpoint-item">
                    <span class="method-badge">GET</span>
                    <span class="endpoint-path">/version</span>
                    <span class="endpoint-desc">Version info</span>
                </a>
                <a href="/dashboard" class="endpoint-item">
                    <span class="method-badge">GET</span>
                    <span class="endpoint-path">/dashboard</span>
                    <span class="endpoint-desc">Full dashboard</span>
                </a>
            </div>
        </div>

        <!-- Build Info -->
        <div class="build-section">
            <div class="section-title">📊 Build Information</div>
            <div class="build-card">
                <div class="build-row">
                    <span class="build-label">Server</span>
                    <span class="badge-purple">{{ server }}</span>
                </div>
                <div class="build-row">
                    <span class="build-label">Environment</span>
                    <span class="badge-purple">{{ environment }}</span>
                </div>
                <div class="build-row">
                    <span class="build-label">Build Number</span>
                    <span class="badge-green">#{{ build }}</span>
                </div>
                <div class="build-row">
                    <span class="build-label">Deployed By</span>
                    <span class="build-value">Jenkins from PC1</span>
                </div>
                <div class="build-row">
                    <span class="build-label">Framework</span>
                    <span class="build-value">Flask 3.0 / Python 3.10</span>
                </div>
                <div class="build-row">
                    <span class="build-label">Container</span>
                    <span class="build-value">Docker</span>
                </div>
                <div class="build-row">
                    <span class="build-label">CI/CD</span>
                    <span class="build-value">Jenkins 2.555.3</span>
                </div>
            </div>
        </div>

    </div>

    <footer class="footer">
        <p>PC2 Server — Controlled by <span>Jenkins on PC1</span></p>
        <p>Build <span>#{{ build }}</span> | Environment: <span>{{ environment }}</span></p>
    </footer>

</body>
</html>
"""

# ── Routes ────────────────────────────────────

@app.route('/')
def home():
    """Home page — serves HTML with build info"""
    try:
        return render_template_string(
            HTML_TEMPLATE,
            server=SERVER,
            environment=ENVIRONMENT,
            build=BUILD_NUMBER
        )
    except Exception as e:
        return jsonify({
            "message"     : "Hello from PC2!",
            "status"      : "running",
            "server"      : SERVER,
            "environment" : ENVIRONMENT,
            "build"       : BUILD_NUMBER,
            "deployed_by" : "Jenkins from PC1",
            "error"       : str(e)
        })

@app.route('/health')
def health():
    """Health check — used by Jenkins pipeline"""
    return jsonify({
        "status"      : "healthy",
        "server"      : SERVER,
        "environment" : ENVIRONMENT,
        "build"       : BUILD_NUMBER
    }), 200

@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    """Add two numbers"""
    return jsonify({
        "a"         : a,
        "b"         : b,
        "result"    : a + b,
        "operation" : "addition",
        "server"    : SERVER
    })

@app.route('/version')
def version():
    """Version info"""
    return jsonify({
        "version"     : "1.0",
        "build"       : BUILD_NUMBER,
        "server"      : SERVER,
        "environment" : ENVIRONMENT,
        "framework"   : "Flask 3.0",
        "python"      : "3.10"
    })

@app.route('/dashboard')
def dashboard():
    """Full system dashboard"""
    return jsonify({
        "server" : {
            "name"        : SERVER,
            "build"       : BUILD_NUMBER,
            "environment" : ENVIRONMENT,
            "status"      : "running"
        },
        "pipeline" : {
            "controller"  : "Jenkins on PC1",
            "slave"       : "ssh-slave-2 on PC2",
            "trigger"     : "GitHub Webhook",
            "deploy_type" : "Docker Container"
        },
        "endpoints" : [
            {"path": "/",          "desc": "Home HTML page"},
            {"path": "/health",    "desc": "Health check JSON"},
            {"path": "/version",   "desc": "Version info JSON"},
            {"path": "/add/a/b",   "desc": "Add numbers JSON"},
            {"path": "/dashboard", "desc": "Full dashboard JSON"}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
