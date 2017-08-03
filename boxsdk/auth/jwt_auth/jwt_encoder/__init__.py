# coding: utf-8

from __future__ import absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod
import random
import string

from six import binary_type, text_type

from boxsdk.util.compat import NoneType, with_metaclass


system_random = random.SystemRandom()


def merge_dict(original, updates):
    if not original:
        return updates
    if not updates:
        return original
    return dict(original, **updates)


class JWTEncoder(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def __call__(self, claims, algorithm, headers=None):
        """
        :param claims:
                    NO: This should always be present at init, will never change. :param secret_key_override:
        :param headers:
        :param algorithm:
        """
        raise NotImplementedError


class PyJWTBasedJWTEncoder(JWTEncoder):

    def __init__(self, private_key, json_encoder=None, **kwargs):
        import jwt
        super(PyJWTBasedJWTEncoder, self).__init__(**kwargs)
        self.json_encoder = json_encoder
        self._py_jwt_encode = jwt.encode

    def __call__(self, claims, algorithm, headers=None):
        return self._py_jwt_encode(
            payload=claims,
            key=self.private_key,
            algorithm=algorithm,
            headers=headers,
            json_encoder=self.json_encoder,
        )


class BoxAuthJWTEncoder(with_metaclass(ABCMeta, object)):

    def __init__(
            self,
            jwt_encoder,
            kid_public_key_id_header=None,
            iss_issuer_client_id_claim=None,
            algorithm='RS256',
            typ_type_header='JWT',
            aud_audience_claim='https://api.box.com/oauth2/token',
            headers=None,
            claims=None,
            **kwargs
    ):
        kid_public_key_id_header = self._normalize_string_parameter(kid_public_key_id_header, 'kid_public_key_id_header')
        iss_issuer_client_id_claim = self._normalize_string_parameter(iss_issuer_client_id_claim, 'iss_issuer_client_id_claim')
        typ_type_header = self._normalize_string_parameter(typ_type_header, 'typ_type_header')
        aud_audience_claim = self._normalize_string_parameter(aud_audience_claim, 'aud_audience_claim')
        headers = headers if (headers is None) else {}
        claims = claims if (claims is None) else {}
        super(BoxAuthJWTEncoder, self).__init__(**kwargs)
        self.jwt_encoder = jwt_encoder
        self.algorithm = algorithm
        self.claims = claims
        for claim_name, claim_value in [('iss', iss_issuer_client_id_claim), ('aud', aud_audience_claim)]:
            if claim_value:
                self.claims[claim_name] = claim_value
        self.headers = headers
        for header_name, header_value in [('kid', kid_public_key_id_header), ('typ', typ_type_header)]:
            if header_value:
                self.headers[header_name] = header_value

    def __call__(self, claims, algorithm, headers=None, exp_expiration_time=True, nbf_not_before_time=False, iat_issued_at_time=False):
        claims = merge_dict(self.claims, claims)
        headers = merge_dict(self.headers, headers)
        algorithm = algorithm or self.algorithm
        if 'jti' not in claims:
            claims['jti'] = self._generate_jti_jwt_id_claim()
        return self.jwt_encoder(claims=claims, algorithm=algorithm, headers=headers)

    @staticmethod
    def _normalize_string_parameter(value, parameter_name, optional=True):
        if isinstance(value, binary_type):
            try:
                return value.decode('ascii')
            except UnicodeError:
                pass
        expected_types = (text_type, NoneType) if optional else text_type
        if not isinstance(value, expected_types):
            raise TypeError(
                "{!s} must be a text/unicode string, got {!r}"
                .format(parameter_name, kid_public_key_id_header.__class__.__name__)
            )

    @staticmethod
    def _generate_jti_jwt_id_claim():
        jti_length = system_random.randint(16, 128)
        ascii_alphabet = string.ascii_letters + string.digits
        ascii_len = len(ascii_alphabet)
        return ''.join(ascii_alphabet[int(system_random.random() * ascii_len)] for _ in range(jti_length))
