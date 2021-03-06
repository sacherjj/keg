from __future__ import absolute_import

from io import StringIO

from keg import signals
from keg_apps.logging import LoggingApp, log
import mock


class TestLogging(object):

    def test_stream_handler(self):
        with mock.patch('sys.stderr', new_callable=StringIO) as m_stderr:
            LoggingApp().init(use_test_profile=True)
            log.warning(u'test warn log')
            log.info(u'test info log')

        output = m_stderr.getvalue().strip().splitlines()
        assert len(output) == 2, output

        assert output[0] == 'WARNING - keg_apps.logging - test warn log'
        assert output[1] == 'INFO - keg_apps.logging - test info log'

    def test_disable_handlers(self):
        app = LoggingApp()

        # It's important to use connect_via() here or the signal will apply to all tests, which
        # produces intermittent test failure, which is hard to troubleshoot, which is bad.
        @signals.config_ready.connect_via(app)
        def apply_config(app):
            app.config['KEG_LOG_STREAM_ENABLED'] = False
            app.config['KEG_LOG_SYSLOG_ENABLED'] = False

        with mock.patch('keg.logging.Logging.init_syslog') as m_init_syslog, \
                mock.patch('keg.logging.Logging.init_stream') as m_init_stream:
            app.init(use_test_profile=True)
            m_init_syslog.assert_not_called()
            m_init_stream.assert_not_called()

    def test_syslog_handler(self):
        with mock.patch('keg.logging.SysLogHandler.emit') as m_emit:
            LoggingApp().init(use_test_profile=True)
            log.warning('test warn log')
            log.info('test info log')

        calls = m_emit.call_args_list
        assert len(calls) == 2

        args, kwargs = calls[0]
        log_record = args[0]
        assert log_record.message == 'test warn log'

        args, kwargs = calls[1]
        log_record = args[0]
        assert log_record.message == 'test info log'
