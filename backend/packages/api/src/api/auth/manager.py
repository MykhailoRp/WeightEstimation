import secrets
import string
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash
from pydantic import BaseModel

from api.auth.conf import ApiTokenConfig, SessionConfig, TokenConfig
from api.auth.exc import InvalidTokenError, TokenExpiredError
from api.auth.models import Token, TokenData
from common.models.customer.api_token import ApiToken
from common.models.user import User, UserWithRole
from common.models.user.session import Session
from common.types import UserId
from common.utils import secrets_choice


class SecretsManager:
    def __init__(self, token_conf: TokenConfig, session_conf: SessionConfig, api_token_conf: ApiTokenConfig) -> None:
        self._pass_hasher = PasswordHash.recommended()
        self.token_conf = token_conf
        self.session_conf = session_conf
        self.api_token_conf = api_token_conf

    def hash_pass(self, password: str) -> str:
        return self._pass_hasher.hash(password)

    def check_hash(self, password: str, hash: str) -> bool:
        return self._pass_hasher.verify(password, hash)

    def _encode_model(self, m: BaseModel) -> str:
        return jwt.encode(
            m.model_dump(mode="json"),
            self.token_conf.secret_key,
            algorithm=self.token_conf.algorithm,
        )

    def _decode_model[T: BaseModel](self, t: type[T], encoded: str) -> T:
        try:
            return t.model_validate(jwt.decode(encoded, self.token_conf.secret_key, algorithms=[self.token_conf.algorithm]))
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError() from e

    def decode_token(self, encoded: str) -> TokenData:
        decoded = self._decode_model(Token, encoded)
        if decoded.expire_at < datetime.now(tz=UTC):
            raise TokenExpiredError()
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

    def mint_api_token(self, customer_id: UserId) -> ApiToken:
        now = datetime.now(tz=UTC)
        return ApiToken(
            token=secrets_choice(string.ascii_letters + string.digits, n=self.api_token_conf.token_len),
            customer_id=customer_id,
            created_at=now,
        )
