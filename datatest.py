from datasets import load_dataset
import pandas as pd

ds = load_dataset("ag_news")
# train/test splits are usually provided:
train = pd.DataFrame(ds['train'])
test = pd.DataFrame(ds['test'])

# Columns are usually: 'text' and 'label'
# Map labels (0..3) to names:
label_map = {0: 'World', 1:'Sports', 2:'Business', 3:'Sci/Tech'}
train['category'] = train['label'].map(label_map)
test['category']  = test['label'].map(label_map)
train = train.rename(columns={'text':'article'})
test  = test.rename(columns={'text':'article'})
