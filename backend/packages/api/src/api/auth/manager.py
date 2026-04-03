import secrets
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from api.auth.conf import SessionConfig, TokenConfig
from api.auth.exc import InvalidTokenError, TokenExpiredError
from api.auth.models import Token, TokenData
from common.models.user import User, UserWithRole
from common.models.user.session import Session


class SecretsManager:
    def __init__(self, token_conf: TokenConfig, session_conf: SessionConfig) -> None:
        self._pass_hasher = PasswordHash.recommended()
        self.token_conf = token_conf
        self.session_conf = session_conf

    def hash_pass(self, password: str) -> str:
        return self._pass_hasher.hash(password)

    def check_hash(self, password: str, hash: str) -> bool:
        return self._pass_hasher.verify(password, hash)

    def decode_token(self, encoded: str) -> TokenData:
        try:
            payload = jwt.decode(encoded, self.token_conf.secret_key, algorithms=[self.token_conf.algorithm])
            decoded = Token.model_validate(payload)

            if decoded.expire_at < datetime.now(tz=UTC):
                raise TokenExpiredError()

        except jwt.InvalidTokenError as e:
            raise InvalidTokenError() from e

        return decoded.data

    def encode_token(self, user: UserWithRole) -> str:
        return jwt.encode(
            Token.new(user=user, expire_in_minutes=self.token_conf.expire_in_minutes).model_dump(mode="json"),
            self.token_conf.secret_key,
            algorithm=self.token_conf.algorithm,
        )

    def mint_session(self, user: User) -> Session:
        return Session(
            token=secrets.token_urlsafe(nbytes=self.session_conf.token_len),
            user_id=user.id,
            created_at=datetime.now(tz=UTC),
            expire_at=datetime.now(tz=UTC) + timedelta(days=self.session_conf.expire_in_days),
        )
