from jwcrypto import jwk
 
if __name__ == '__main__':
    print(jwk.JWK.generate(kty='RSA', size=2048).export_public())
    print(jwk.JWK.generate(kty='RSA', size=2048).export_private())

