from src import app

if __name__ == "__main__":
    context = ('/etc/letsencrypt/live/cakefactorykota.com/fullchain.pem',
    '/etc/letsencrypt/live/cakefactorykota.com/privkey.pem')

    # Run on port 443 with the SSL context
    app.run(host='0.0.0.0', port=443, ssl_context=context)