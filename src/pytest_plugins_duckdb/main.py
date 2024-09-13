import requests
import duckdb
import pandas as pd
from bs4 import BeautifulSoup

# Fetch the plugin list page
url = "https://docs.pytest.org/en/stable/reference/plugin_list.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract plugin data from the table
plugins = []
table = soup.find('table')
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    plugin_data = {
        'name': cols[0].text.strip(),
        'summary': cols[1].text.strip(),
        'status': cols[2].text.strip(),
        'date': cols[3].text.strip()
    }
    plugins.append(plugin_data)

# Convert to DataFrame
df = pd.DataFrame(plugins)

# Save to DuckDB and query
con = duckdb.connect(':memory:')
con.execute("CREATE TABLE plugins AS SELECT * FROM df")
# Query the first 100 records, sorted by date desc
result = con.execute("SELECT * FROM plugins ORDER BY date DESC LIMIT 100").df()

# Display the result
print(result)
