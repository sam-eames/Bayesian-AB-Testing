# From the course: Bayesian Machine Learning in Python: A/B Testing
# https://deeplearningcourses.com/c/bayesian-machine-learning-in-python-ab-testing
# https://www.udemy.com/bayesian-machine-learning-in-python-ab-testing
import requests
import pandas as pd

# get data
df = pd.read_csv('advertisement_clicks.csv')
a = df[df['advertisement_id'] == 'A']
b = df[df['advertisement_id'] == 'B']
a = a['action'].values
b = b['action'].values

print("a.mean:", a.mean())
print("b.mean:", b.mean())

i = 0
j = 0
count = 0

# run until dataset ends
while i < len(a) and j < len(b):
  
  r = requests.get('http://localhost:5000/get_ad')
  r = r.json()
  
  # view
  if r['advertisement_id'] == 'A':
    action = a[i]
    i += 1
  else:
    action = b[j]
    j += 1

  if action == 1:
    # click
    requests.post(
      'http://localhost:5000/click_ad',
      data={'advertisement_id': r['advertisement_id']}
    )

  # every 100 views show num times each ad shown
  count += 1
  if count % 100 == 0:
    print("Seen %s ads, A: %s, B: %s" % (count, i, j))
