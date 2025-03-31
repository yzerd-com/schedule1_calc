from jinja2 import Template
from config import OUTPUT_HTML_FILE

html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Optimal Combo Optimizer Results</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2em; }
    select { font-size: 1em; padding: 0.25em; }
    table { border-collapse: collapse; width: 100%; margin-top: 1em; }
    th, td { border: 1px solid #ccc; padding: 0.5em; text-align: center; }
    th { background-color: #f0f0f0; }
    .hidden { display: none; }
  </style>
</head>
<body>
  <h1>Optimal Combo Optimizer Results</h1>
  
  <label for="baseSelect">Select Primary Product:</label>
  <select id="baseSelect"></select>
  <br><br>
  <label for="levelSelect">Select Your Level:</label>
  <select id="levelSelect"></select>
  <br><br>
  <button id="viewButton">View Results</button>

  <div id="resultsSection" class="hidden">
    <h2>Results</h2>
    <div id="resultsContent"></div>
  </div>

  <script>
    const precomputedData = {{ precomputed|tojson }};
    const availableLevels = {{ levels|tojson }};
    const baseProductNames = {{ base_products|tojson }};
    
    const baseSelect = document.getElementById("baseSelect");
    const levelSelect = document.getElementById("levelSelect");
    const resultsSection = document.getElementById("resultsSection");
    const resultsContent = document.getElementById("resultsContent");
    
    baseProductNames.forEach(base => {
      const opt = document.createElement("option");
      opt.value = base;
      opt.innerText = base;
      baseSelect.appendChild(opt);
    });
    
    function updateLevels() {
      const selectedBase = baseSelect.value;
      levelSelect.innerHTML = "";
      availableLevels.forEach(level => {
        if (precomputedData[selectedBase] && precomputedData[selectedBase][level]) {
          const opt = document.createElement("option");
          opt.value = level;
          opt.innerText = level;
          levelSelect.appendChild(opt);
        }
      });
    }
    
    baseSelect.addEventListener("change", updateLevels);
    updateLevels();
    
    document.getElementById("viewButton").addEventListener("click", function() {
      const selectedBase = baseSelect.value;
      const selectedLevel = levelSelect.value;
      if (!precomputedData[selectedBase] || !precomputedData[selectedBase][selectedLevel]) {
        resultsContent.innerHTML = "<p>No data available for this selection.</p>";
        resultsSection.classList.remove("hidden");
        return;
      }
      
      const result = precomputedData[selectedBase][selectedLevel];
      let html = "";
      const lengths = Object.keys(result.by_length).map(x => parseInt(x)).sort((a, b) => a - b);
      html += "<table>";
      html += "<thead><tr><th>Len</th><th>Δ Net</th><th>Net Benefit</th><th>Expected Value</th><th>Cost</th><th>Multiplier</th><th># Effects</th><th>Sequence</th><th>Effects</th></tr></thead><tbody>";
      let lastNet = null;
      lengths.forEach(len => {
        const combo = result.by_length[len.toString()];
        const net = combo.net_benefit;
        const delta = (lastNet !== null) ? (net - lastNet).toFixed(2) : "–";
        lastNet = net;
        html += `<tr>
                  <td>${len}</td>
                  <td>${delta}</td>
                  <td>${combo.net_benefit}</td>
                  <td>${combo.expected_total_value}</td>
                  <td>${combo.cost}</td>
                  <td>${combo.total_multiplier.toFixed(2)}</td>
                  <td>${combo.effects.length}</td>
                  <td>${combo.sequence.join(", ")}</td>
                  <td>${combo.effects.join(", ")}</td>
                </tr>`;
      });
      html += "</tbody></table>";
      resultsContent.innerHTML = html;
      resultsSection.classList.remove("hidden");
    });
  </script>
</body>
</html>
"""

def generate_static_html(precomputed, levels, base_products):
    template = Template(html_template)
    rendered_html = template.render(precomputed=precomputed,
                                    levels=levels,
                                    base_products=base_products)
    with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as f:
        f.write(rendered_html)
    print(f"Static HTML file generated: {OUTPUT_HTML_FILE}")
