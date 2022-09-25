from . import bp as app
from flask import render_template, request, redirect, url_for, flash
from app.blueprints.main.models import Pokemon
from app import db
from flask_login import current_user, login_required

# Routes that return/display HTML

@app.route('/')
@login_required
def home():
    pokemons = Pokemon.query.all()

    return render_template('home.html', user=current_user, pokemons=pokemons)

@app.route('/pokedex')
@login_required
def all_pokemon():
    pokemon = Pokemon.query.all()
    return render_template('pokedex.html', all_pokemon=pokemon)

@app.route('/pokemon', methods=['POST'])
@login_required
def create_pokemon():
    poke_name = request.form['name']
    poke_description = request.form['description']
    poke_type = request.form['type']
    
    new_pokemon = Pokemon(name=poke_name, description=poke_description, type=poke_type, owner=current_user.id)

    db.session.add(new_pokemon)
    db.session.commit()

    flash('Pokemon has been added successfully', 'success')
    return redirect(url_for('main.home'))

@app.route('/captured/<id>')
def captured(id):
    single_pokemon = Pokemon.query.get(id)
    return render_template('captured.html', captured=single_pokemon)
    

@app.route('/myPokedex/<id>')
def pokemon_info(id):
    pokemon = Pokemon.query.all(id)
    return render_template('pokedex.html', pokemon_info=pokemon)