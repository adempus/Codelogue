from flask_jwt_extended import create_access_token, JWTManager
from flask import jsonify
from flask_graphql import GraphQLView
from src.app import createApp

appData = createApp()
app = appData['app']
jwt = JWTManager(app)

app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view('graphql', schema=appData['schema'], graphiql=True)
)

@jwt.expired_token_loader
def handleExpiredSession(expiredToken):
    # token_type = expiredToken['type']
    return jsonify({
        'error': True,
        'msg': 'The session has expired. Please sign in.'
    })



if __name__=='__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True, port=5000)
