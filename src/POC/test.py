import json
from http import HTTPStatus
from sympy.parsing.latex import parse_latex
from flask import Flask, request, send_file
from decimal import Decimal
app = Flask(__name__)

@app.route('/')
def hello_world():
    return send_file('index.html')

@app.route('/mathquill-0.10.1/<path:filename>')
def mathquill(filename):
    return send_file('mathquill-0.10.1/' + filename)

@app.route('/test')
def expression():
  expr = parse_latex(r"\frac {1 + \sqrt {\a}} {\b}")
  input = json.loads('{"a": 5, "b": 2}')
  result = expr.evalf(4, subs=input)
  return str(result)

@app.route('/upload', methods=['POST'])
def process_upload():
  print('Received POST: ')

  jsonData = request.get_json()

  print(jsonData['eq'])
  print(jsonData['ans']['x'])

  expr = parse_latex(jsonData['eq'])

  answerMap = map_answers_to_latex(jsonData['ans'])

  computationResult = expr.evalf(subs=answerMap)

  print(f'Computation result: {computationResult}')

  substitutionResult = expr.subs([('x', jsonData['ans']['x'])])

  print(f'Substitution result: {substitutionResult}')

  # if(computationResult.is_integer):
  #   result = computationResult
  # else:
  #   result = float('{:.4f}'.format(computationResult))

  # print(f'Result: {result == 0.0}')

  # return str(result == 0.0), HTTPStatus.OK

  return str(False), HTTPStatus.OK

def map_answers_to_latex(latexData):
  numberData = {}

  for variable in latexData:
    numberData[variable] = parse_latex(latexData[variable])

  return numberData