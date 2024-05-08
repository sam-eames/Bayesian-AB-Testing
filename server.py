# From the course: Bayesian Machine Learning in Python: A/B Testing
# https://deeplearningcourses.com/c/bayesian-machine-learning-in-python-ab-testing
# https://www.udemy.com/bayesian-machine-learning-in-python-ab-testing

import numpy as np
from flask import Flask, jsonify, request
from scipy.stats import beta

app = Flask(__name__)

# bandit class to model each ad
class Bandit:
  def __init__(self, name):
    self.clicks = 0
    self.views = 0
    self.name = name

  def sample(self):
    # Beta(1, 1) is the initial prior, update with:
    a = 1 + self.clicks
    b = 1 + self.views - self.clicks
    return np.random.beta(a, b)

  def add_click(self):
    self.clicks += 1

  def add_view(self):
    self.views += 1

    # every 100 clicks, return stats
    if self.views % 100 == 0:
      print("%s: clicks=%s, views=%s" % (self.name, self.clicks, self.views))


# initialize bandits
banditA = Bandit('A')
banditB = Bandit('B')


@app.route('/get_ad')
def get_ad():
  if banditA.sample() > banditB.sample():
    ad = 'A'
    banditA.add_view()
  else:
    ad = 'B'
    banditB.add_view()
  return jsonify({'advertisement_id': ad})


@app.route('/click_ad', methods=['POST'])
def click_ad():
  result = 'OK'
  if request.form['advertisement_id'] == 'A':
    banditA.add_click()
  elif request.form['advertisement_id'] == 'B':
    banditB.add_click()
  else:
    result = 'Invalid Input.'

  return jsonify({'result': result})


if __name__ == '__main__':
  app.run(port='5000')