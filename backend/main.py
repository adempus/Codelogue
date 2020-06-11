from src.app import createApp

app = createApp()


if __name__=='__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True, port=5000)