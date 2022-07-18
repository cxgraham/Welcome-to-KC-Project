from flask_app import app
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



class Comment:
    db = 'solo_project'

    def __init__(self, data):
        self.id = data['id']
        self.comment_text = data['comment_text']
        self.date = data['date']
        self.comment_type = data['comment_type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.commentor = None
        self.likes = 0
    
    

    # CREATE 
    @classmethod
    def create_comment_for_top_restaurants(cls, data):
        if not cls.validate_comment(data):
            return False
        query = """
        INSERT INTO comments (comment_text, date, comment_type, user_id)
        VALUES (%(comment_text)s, NOW(), 'restaurants', %(user_id)s)
        ;"""
        comment_id = connectToMySQL(cls.db).query_db(query, data)
        # print(comment_id)
        return comment_id
    
    @classmethod
    def create_comment_for_top_things_to_do(cls, data):
        if not cls.validate_comment(data):
            return False
        query = """
        INSERT INTO comments (comment_text, date, comment_type, user_id)
        VALUES (%(comment_text)s, NOW(), 'to_do', %(user_id)s)
        ;"""
        comment_id = connectToMySQL(cls.db).query_db(query, data)
        # print(comment_id)
        return comment_id
    
    @classmethod
    def create_comment_for_top_bars(cls, data):
        if not cls.validate_comment(data):
            return False
        query = """
        INSERT INTO comments (comment_text, date, comment_type, user_id)
        VALUES (%(comment_text)s, NOW(), 'bars', %(user_id)s)
        ;"""
        comment_id = connectToMySQL(cls.db).query_db(query, data)
        # print(comment_id)
        return comment_id
    
    @classmethod
    def add_like_to_comment(cls, data):
        query = """
        INSERT INTO likes (user_id, comment_id)
        VALUES (%(user_id)s, %(comment_id)s)
        ;"""
        one_like = connectToMySQL(cls.db).query_db(query, data)
        if one_like:
            one_like = cls.likes + 1
        return one_like

    # READ 
    @classmethod
    def get_all_comments(cls):
        query = """
        SELECT * FROM comments
        LEFT JOIN likes ON comments.id = likes.comment_id
        LEFT JOIN users on comments.user_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        # print(results)
        all_comments = []
        for this_comment in results:
            new_comment = cls(this_comment)
            this_commentor = {
                'id': this_comment['users.id'],
                'first_name': this_comment['first_name'],
                'last_name': this_comment['last_name'],
                'email': this_comment['email'],
                'password': this_comment['password'],
                'created_at': this_comment['users.created_at'],
                'updated_at': this_comment['users.updated_at']
            }
            new_comment.commentor = user.User(this_commentor)
            all_comments.append(new_comment)
        return all_comments
    
    @classmethod
    def get_comment_info_by_id(cls, id):
        data = {'id': id}
        query = """
        SELECT * FROM comments
        WHERE id = %(id)s
        ;"""
        this_comment = connectToMySQL(cls.db).query_db(query, data)
        # print(this_comment)
        if this_comment:
            this_comment = cls(this_comment[0])
        return this_comment



    # UPDATE 
    @classmethod
    def edit_comment_by_id(cls, data):
        if not cls.validate_comment(data):
            return False
        query = """
        UPDATE comments
        SET comment_text = %(comment_text)s, date = NOW()
        WHERE comments.id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)


    # DELETE
    @classmethod 
    def delete_comment_by_id(cls, id):
        data = {'id': id}
        query = """
        DELETE FROM comments
        WHERE comments.id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)


    # VALIDATE
    @staticmethod
    def validate_comment(data):
        is_valid = True
        if (data['comment_text']) == "":
            flash('Cannot leave comment blank', 'comment')
            is_valid = False
        return is_valid