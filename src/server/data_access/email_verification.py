from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email, key):
    serializer = URLSafeTimedSerializer(key)
    return serializer.dumps(email, salt=key)


def confirm_token(token, key, expiration=3600):
    serializer = URLSafeTimedSerializer(key)
    try:
        email = serializer.loads(
                                 token,
                                 salt=application.config['SECURITY_PASSWORD_SALT'],
                                 max_age=expiration
                                 )
    except:
        return False
    return email
