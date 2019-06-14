import json
import pandas as pd
import sys
js = json.loads(open(sys.argv[1]).read())
y = pd.DataFrame.from_dict(js)
print(y.head())
