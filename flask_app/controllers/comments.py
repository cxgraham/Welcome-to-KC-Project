from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, comment

# CREATE 
@app.route('/comments/create/restaurants', methods = ['POST'])
def add_comment_to_restaurants():
    if 'user_id' not in session:
        flash('You must create an account to add a comment', 'comment')
        return redirect('/top_five_restaurants')
    new_comment = comment.Comment.create_comment_for_top_restaurants(request.form)
    if new_comment:
        return redirect('/top_five_restaurants')
    return redirect('/top_five_restaurants')

@app.route('/comments/create/bars', methods = ['POST'])
def add_comment_to_bars():
    if 'user_id' not in session:
        flash('You must create an account to add a comment', 'comment')
        return redirect('/top_five_bars')
    new_comment = comment.Comment.create_comment_for_top_bars(request.form)
    if new_comment:
        return redirect('/top_five_bars')
    return redirect('/top_five_bars')

@app.route('/comments/create/things_to_do', methods = ['POST'])
def add_comment_to_things_to_do():
    if 'user_id' not in session:
        flash('You must create an account to add a comment', 'comment')
        return redirect('/top_five_things_to_do')
    new_comment = comment.Comment.create_comment_for_top_things_to_do(request.form)
    if new_comment:
        return redirect('/top_five_things_to_do')
    return redirect('/top_five_things_to_do')

@app.route('/comments/add_like', methods = ['POST'])
def add_like():
    # data = {
    #     'user_id': session['user_id'],
    #     'comment_id': request.form["comment_id"]
    # }
    comment.Comment.add_like_to_comment(request.form)
    return redirect(request.referrer)

# READ 
@app.route('/comments/edit/<int:id>')
def add_comment(id):
    this_comment = comment.Comment.get_comment_info_by_id(id)
    return render_template('edit_comment.html', this_comment = this_comment)

# UPDATE 
@app.route('/comments/update', methods = ['POST'])
def edit_comment():
    data = {
        'comment_text': request.form['comment_text']
    }
    comment.Comment.edit_comment_by_id(data)
    return redirect ('/users/dashboard')


# DELETE
@app.route('/comments/delete/<int:id>')
def delete_comment(id):
    comment.Comment.delete_comment_by_id(id)
    return redirect (request.referrer)