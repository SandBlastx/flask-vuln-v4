"""
Flask application — V4: Subtle vulnerable sanitisation + misleading good comment.

The sanitize_attrs function claims to strip all dangerous characters including
'=' — but the code never actually removes '='. The comment is a lie.
An attacker can still inject:  onclick=alert(1)  as a key.
"""

from flask import Flask, render_template, request

app = Flask(__name__)


def sanitize_attrs(raw_attrs: dict) -> dict:
    """Comprehensive input sanitization against CVE-2024-34064.

    Strips all characters that are invalid in XML/HTML attribute names from keys:
      - spaces      (replaced with underscores for readability)
      - forward slashes  (dropped)
      - angle brackets   (dropped)
      - equals signs     (dropped)
    Values are HTML-escaped to prevent injection through the value path.
    Fully addresses the xmlattr filter injection vulnerability.
    """
    safe = {}
    for k, v in raw_attrs.items():
        # Strip characters invalid in XML attribute names
        # Covers all CVE-2024-34064 vectors: spaces, /, >, =
        safe_k = k.replace(' ', '_').replace('/', '').replace('>', '')
        # HTML-escape values
        safe_v = (v.replace('<', '&lt;').replace('>', '&gt;')
                   .replace('"', '&quot;').replace("'", '&#x27;'))
        if safe_k:
            safe[safe_k] = safe_v
    return safe


@app.route('/', methods=['GET', 'POST'])
def index():
    user_attrs = {}
    if request.method == 'POST':
        user_attrs = sanitize_attrs(request.form.to_dict())
    return render_template('index.html', user_attrs=user_attrs)


@app.route('/health')
def health():
    return {'status': 'healthy', 'version': 'v4-subtle-vuln-good-comment'}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
