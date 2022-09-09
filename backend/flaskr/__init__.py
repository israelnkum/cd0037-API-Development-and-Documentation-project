import random

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        all_categories = [category.format() for category in selection]
        current_Questions = all_categories[start:end]

        return current_Questions

    def categories():
        all_categories = Category.query.all()
        return [category.format() for category in all_categories]

    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        return jsonify(
            {
                "success": True,
                "categories": categories(),
            }
        )

    @app.route('/questions', methods=['GET'])
    def get_questions(category_id=0):
        if category_id == 0:
            selection = Question.query.order_by(Question.id).all()
        else:
            selection = \
                Question.query.filter(Question.category == category_id) \
                .order_by(Question.id).all()

        all_questions = paginate_questions(request, selection)

        if len(all_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": all_questions,
                "total_questions": len(selection),
                "categories": categories(),
                "current_category": "Science"
            }
        )

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = \
                Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(422)

            question.delete()
            return get_questions()
        except Exception as ex:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            body = request.get_json()

            question = body.get("question")
            answer = body.get("answer", )
            category = body.get("category")
            difficulty = body.get("difficulty")

            if not ('question' in body
                    and 'answer' in body
                    and 'difficulty' in body
                    and 'category' in body):
                abort(422)
            question = Question(question=question,
                                answer=answer,
                                category=category,
                                difficulty=difficulty)
            question.insert()

            return jsonify(
                {
                    "success": True,
                    "message": "Question Saved",
                }
            )

        except Exception as ex:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = body.get("searchTerm", None)

        if not search_term:
            abort(404)
        results = Question.query\
            .filter(Question.question.ilike("%" + search_term + "%"))\
            .all()

        all_questions = paginate_questions(request, results)

        return jsonify(
            {
                "success": True,
                "questions": all_questions,
                "total_questions": len(results),
                "current_category": "Science"
            }
        )

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
        category = Category.query.filter(Category.id == category_id)
        if category is None:
            abort(400)
        return get_questions(category_id)

    @app.route('/quizzes', methods=['POST'])
    def get_next_question():

        try:
            body = request.get_json()
            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(422)
            category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)

            if category['id'] == 0:
                available_questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id'])\
                    .filter(Question.id.notin_(previous_questions))\
                    .all()

            if len(available_questions) > 0:
                random_id = random.randrange(0, len(available_questions))
                next_question = available_questions[random_id].format()

                return jsonify({
                    'success': True,
                    'question': next_question,
                    'quiz_category': category['type']
                })

            else:
                return jsonify({
                    'success': True,
                    'question': None,
                    'quiz_category': category['type']
                })

        except Exception as ex:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    return app
