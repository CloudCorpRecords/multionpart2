from flask import Flask, jsonify, Response
from flask_cors import CORS
from multion.client import MultiOn
import agentops

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize AgentOps with your API key
# agentops.init('e958ba3e-2d5a-4878-b4c7-5c1d05e4c66d')

multion = MultiOn(api_key="01fac5877eea4fa18839503af2f0aa25", agentops_api_key="e958ba3e-2d5a-4878-b4c7-5c1d05e4c66d")

@app.route('/stocks', methods=['GET'])
def get_top_traded_stocks():
    try:
        browse = multion.browse(
            cmd="Find what stocks moved the most last Friday. Display Output in descending order of highest short interest.If Unsure , just give current list with output only. Do not ask questions.",
            url="https://stockanalysis.com/markets/most-active/"
        )
        # Convert browse response to string
        browse_response = str(browse)
        
        # Remove unwanted parts using regex
        import re
        clean_response = re.sub(
            r"(message=| status='[A-Z_]+'| url='https:\/\/stockanalysis\.com\/markets\/most-active\/'| screenshot=''| session_id='[a-f0-9-]+'| metadata=Metadata\(step_count=\d+, processing_time=\d+, temperature=\d\.\d\))",
            '',
            browse_response
        ).strip()

        return Response(clean_response, mimetype='text/plain')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)