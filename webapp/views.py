# encoding: utf-8

from webapp import app, basic_auth
from flask import render_template, make_response, abort, request, Response, redirect
from models import *
from forms import *
import models, util
import json, time, os
from subprocess import call
from sqlalchemy import or_


@app.route('/')
def index():
  return render_template('index.html')

@app.route("/tree-list")
def tree_list():
  start_time = time.time()
  trees = Tree.query.filter_by(public=1).all()
  result = []
  for tree in trees:
    result.append({
      'id': tree.id,
      'lat': tree.lat,
      'lng': tree.lng,
      'type': tree.type
    })
  ret = {
    'status': 0,
    'duration': round((time.time() - start_time) * 1000),
    'request': {},
    'response': result
  }
  json_output = json.dumps(ret, cls=util.MyEncoder, sort_keys=True)
  response = make_response(json_output, 200)
  response.mimetype = 'application/json'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = -1
  response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
  return(response)
  
@app.route("/tree-details")
def tree_details():
  start_time = time.time()
  try:
    tree_id = id=int(request.args.get('id'))
  except ValueError:
    abort(500)
  tree = Tree.query.filter_by(id=tree_id).first_or_404()
  result = {
    'id': tree.id,
    'address': tree.address,
    'postalcode': tree.postalcode,
    'city': tree.city,
    'descr': tree.descr,
    'picture': tree.picture,
    'lat': tree.lat,
    'lng': tree.lng,
    'type': tree.type
  }
  ret = {
    'status': 0,
    'duration': round((time.time() - start_time) * 1000),
    'request': {},
    'response': result
  }
  json_output = json.dumps(ret, cls=util.MyEncoder, sort_keys=True)
  response = make_response(json_output, 200)
  response.mimetype = 'application/json'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = -1
  response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
  return(response)

@app.route("/new-tree", methods=['GET', 'POST'])
def new_tree():
  tree = Tree()
  tree_form = NewTree(request.form, tree)
  if request.method == 'POST' and tree_form.validate():
    tree_form.populate_obj(tree)
    tree.city = 'Bochum'
    tree.public = 0
    db.session.add(tree)
    db.session.commit()
    #msg = Message(recipients=[edit_user.email],
    #  sender="mail@ernestoruge.de",
    #  body="Neuer Baum eingetragen",
    #  html=content_html,
    #  subject=u"Neuer Baum wurde eingereicht")
    #mail.send(msg)
    if request.files['image'].filename:
      image_data = request.files['image'].read()
      # write new image data
      open(os.path.join(app.config['IMAGE_UPLOAD_PATH_BASE'], str(tree.id) + '.jpg'), 'w').write(image_data)
      call(['/usr/bin/convert', '-resize', '270x270', os.path.join(app.config['IMAGE_UPLOAD_PATH_BASE'], str(tree.id) + '.jpg'), os.path.join(app.config['IMAGE_UPLOAD_PATH_BASE'], str(tree.id) + '-small.jpg')])
      tree.image = 1
      db.session.add(tree)
      db.session.commit()
    return redirect("/")
  return render_template('new-tree.html', tree_form=tree_form)



@app.route("/information")
def information():
  return render_template('information.html')

@app.route("/admin")
@basic_auth.required
def admin():
  return render_template('information.html')

@app.route("/geocode")
def geocode():
    start = time.time()
    jsonp_callback = request.args.get('callback', None)
    address = request.args.get('address', '')
    if address == '':
        abort(400)
    obj = {
        'result': util.geocode(address)
    }
    obj['duration'] = int((time.time() - start) * 1000)
    json_output = json.dumps(obj, sort_keys=True)
    if jsonp_callback is not None:
        json_output = jsonp_callback + '(' + json_output + ')'
    response = make_response(json_output, 200)
    response.mimetype = 'application/json'
    response.headers['Expires'] = util.expires_date(hours=24)
    response.headers['Cache-Control'] = util.cache_max_age(hours=24)
    return response
