# SSL Configuration
If you require SSL for your API server, drop your server.key and server.crt in this directory.

## Getting Keys
[I suggest utilizing letsencrypt for your SSL certificates. It's free!](https://letsencrypt.org/getting-started/)

`./letsencrypt-auto certonly --standalone -d myarkserver.example.com`

This will create the keys as follows:

`/etc/letsencrypt/live/myarkserver.example.com/cert.pem` The certificate PEM.
`/etc/letsencrypt/live/myarkserver.example.com/privkey.pem` The private key.

Copy these into your ssl directory:

`sudo cp /etc/letsencrypt/live/myarkserver.example.com/cert.pem ssl/`
`cudo cp /etc/letsencrypt/live/myarkserver.example.com/privkey.pem ssl/`

Unfortunately for windows users, you are on your own. Get a certificate and key by self-signing or buying a certificate.
Let's Encrypt may have a Windows option, it is worth looking into for the free key.

## Configuration
You need to configure the following options in your `server.conf` file:

    ssl_crt = cert.pem
    ssl_key = privkey.pem

These are the file names of your certificate and key.