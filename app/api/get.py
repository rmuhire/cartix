from app import *
from app.model.models import *
from app.model.schema import *
from flask import jsonify

@app.errorhandler(404)
def page_not_found(e):
    return 'Error 404: Page not found, Please check ur route well.'

@app.route('/api/v1/sg')
def sg():
    sg = SavingGroup.query.all()
    result = sgs_schema.dump(sg)
    return jsonify({'Saving groups':result.data})


@app.route('/api/v1/sg/<name>')
def sg_name(name):
    sg = SavingGroup.query.filter_by(name=name).first()
    if sg:
        result=sg_schema.dump(sg)
        return jsonify({'Saving Group':result.data})
    else:
        return jsonify({'Message':'0'})


@app.route('/api/v1/amount')
def amount():
    amount = Amount.query.all()
    result = amounts_schema.dump(amount).data
    return jsonify({'Amounts':result})

@app.route('/api/v1/amount/<int:id>')
def amount_sg(id):
    amount = Amount.query.filter_by(sg_id=id).first()
    if amount:
        result = amount_schema.dump(amount)
        return jsonify({'SG-Amount':result.data})
    else:
        return jsonify({'Message':'0'})

@app.route('/api/v1/ngos')
def ngo():
    ngo = Ngo.query.all()
    result = ngos_schema.dump(ngo).data
    return jsonify({'NGOs':result})

@app.route('/api/v1/ngo/<name>')
def ngo(name):
    ngo = Ngo.query.filter_by(name=name).first()
    if ngo:
        result = ngo_schema.dump(ngo)
        return jsonify({'NGO':result.data})

    else:
        return jsonify({'Message':'0'})