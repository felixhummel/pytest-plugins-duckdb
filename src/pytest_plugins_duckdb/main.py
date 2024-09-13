import dateparser
import requests
import duckdb
import pandas as pd
from bs4 import BeautifulSoup


url = "https://docs.pytest.org/en/stable/reference/plugin_list.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

plugins = []
table = soup.find('table')
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    plugin_data = {
        'name': cols[0].text.strip(),
        'summary': cols[1].text.strip(),
        'date': cols[2].text.strip(),
        'status': cols[3].text.strip(),
    }
    plugins.append(plugin_data)


def dt2iso(dt: str) -> str:
    x = dateparser.parse(dt)
    return x.date().isoformat()


df = pd.DataFrame(plugins)
df['date'] = df['date'].map(dt2iso)

con = duckdb.connect('db.duck')
_ = con.execute("DROP TABLE IF EXISTS plugins")
_ = con.execute("CREATE TABLE plugins AS SELECT * FROM df")
