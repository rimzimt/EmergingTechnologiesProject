from flask import Flask, send_file
from flask import request, jsonify, abort, make_response
from flask_cors import CORS
from summarizer.ArticleService import ArticleService
from summarizer.SummarizationService import SummarizationService
from summarizer.UdacityParser import UdacityParser


app = Flask(__name__)
CORS(app)

article_service = ArticleService()
summary_service = SummarizationService()


def validate_article(request):
    if 'course' not in request or not request['course']:
        abort(make_response(jsonify(message="course must be supplied"), 400))
    if 'content' not in request or not request['content']:
        abort(make_response(jsonify(message="content must be supplied"), 400))
    if 'name' not in request or not request['name']:
        abort(make_response(jsonify(message="name must be supplied"), 400))


@app.route('/articles', methods=['POST'])
def create_article():
    validate_article(request.json)
    return jsonify(article_service.create_article(request.json))


@app.route('/articles', methods=['GET'])
def get_articles():
    course = request.args.get('course', None)
    name = request.args.get('name', None)
    limit = int(request.args.get('limit', 10))
    return jsonify(article_service.get_articles(course, name, limit))


@app.route('/articles/<articleid>', methods=['GET'])
def get_article(articleid):
    if articleid is None:
        abort(make_response(jsonify(message="you must supply a article id"), 400))
    result = article_service.get_article(articleid)
    if result:
        return jsonify(result)
    abort(make_response(jsonify(message="article not found"), 404))


@app.route('/articles/<articleid>', methods=['DELETE'])
def delete_article(articleid):
    if articleid is None:
        abort(make_response(jsonify(message="you must supply a article id"), 400))
    result = article_service.delete_article(articleid)
    if result:
        return jsonify(result)
    abort(make_response(jsonify(message="article not found"), 404))


@app.route('/articles/<articleid>/summaries', methods=['POST'])
def create_summary(articleid):
    if articleid is None:
        abort(make_response(jsonify(message="you must supply a article id"), 400))
    try:
        result = summary_service.create_summary(articleid, request.json)
        if result:
            return jsonify(result)
    except Exception as e:
        abort(make_response(jsonify(message=str(e)), 400))
    abort(make_response(jsonify(message="article not found"), 404))


@app.route('/articles/<articleid>/summaries', methods=['GET'])
def get_summaries(articleid):
    article: int = articleid
    name: str = request.args.get('name', None)
    limit: int = int(request.args.get('limit', 10))
    return jsonify(summary_service.list_summaries(name, article, limit))


@app.route('/articles/<articleid>/summaries/<summaryid>', methods=['GET'])
def get_summary(articleid, summaryid):
    if articleid is None or summaryid is None:
        abort(make_response(jsonify(message="article id and summary id must be supplied in URL"), 400))
    summary = summary_service.get_summary(articleid, summaryid)
    if summary:
        return jsonify(summary)
    abort(make_response(jsonify(message="Summary or article not found"), 404))


@app.route('/articles/<articleid>/summaries/<summaryid>', methods=['DELETE'])
def delete_summary(articleid, summaryid):
    if articleid is None or summaryid is None:
        abort(make_response(jsonify(message="you must supply a article id and summary id"), 400))
    result = summary_service.delete_summary(summaryid)
    if result:
        return jsonify(result)
    abort(make_response(jsonify(message="summary or article not found"), 404))


@app.route('/udacity', methods=['POST'])
def convert_udacity():
    data = request.data
    if not data:
        abort(make_response(jsonify(message="Request must have raw text"), 400))
    return jsonify(UdacityParser(data).convert_to_paragraphs())

@app.route('/')
def index():
    return jsonify({"healthy": 200})


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.errorhandler(500)
def unknown_error(e):
    return jsonify(error=500, text='Unexpected Error Occurred'), 500

@app.route('/articles/eda/<articleid>', methods=['GET'])
def get_eda(articleid):
    if articleid is None:
        abort(make_response(jsonify(message="you must supply a article id"), 400))
    print("article"+ articleid)
    result_bytes = article_service.get_EDA(articleid)
    if result_bytes:
        return send_file(result_bytes,attachment_filename='wordcloudplot.png',mimetype='image/png')
    abort(make_response(jsonify(message="article not found"), 404))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)



