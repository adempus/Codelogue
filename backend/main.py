from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from flask import jsonify
from flask_graphql import GraphQLView
from src.app import createApp

appData = createApp()
app = appData['app']
jwt = JWTManager(app)


# @jwt_required
def graphql_view():
    view = GraphQLView.as_view('graphql', schema=appData['schema'], graphiql=True)
    return view

app.add_url_rule(
    '/graphql', view_func=graphql_view()
)

@jwt.expired_token_loader
def handleExpiredSession(expiredToken):
    # token_type = expiredToken['type']
    return jsonify({
        'error': True,
        'msg': 'The session has expired. Please sign in.'
    })


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
