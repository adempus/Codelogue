from flask_jwt_extended import create_access_token, JWTManager
from flask import jsonify
from src.app import createApp

app = createApp()
jwt = JWTManager(app)

@jwt.expired_token_loader
def handleExpiredSession(expiredToken):
    # token_type = expiredToken['type']
    return jsonify({
        'error': True,
        'msg': 'The session has expired. Please sign in.'
    })



if __name__=='__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True, port=5000)
