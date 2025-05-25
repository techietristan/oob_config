from requests import Response

def config_session(config: dict, response: Response) -> None:
    config['session_uri'] = response.headers['Location']
    config['token'] = response.headers['X-Auth-Token']
    config['ilo_headers']['X-Auth-Token'] = config['token']
    config['ilo_headers']['Cookie'] = f'sessionKey={config['token']}'
