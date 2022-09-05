import pydevd_pycharm


def start_debug_client():
    """
    The 172.17.0.1 is the host.docker.internal, which points to the host's localhost in a bridge network.
    Since our pycharm debug config consists of host: 127.0.0.1 (localhost) and port: 12345,
    the following is necessary in order to send debug requests
    from our container to the pycharm's server on host's localhost:12345
    """
    return pydevd_pycharm.settrace('172.17.0.1', port=12345, stdoutToServer=True, stderrToServer=True)
