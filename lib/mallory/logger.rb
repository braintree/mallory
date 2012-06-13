module Mallory
  class Logger
    extend Forwardable
    def_delegators :EM, :debug, :info

    def write(message)
      info(message)
    end

    def setup!
      EM.syslog_setup('0.0.0.0', 514)
    end
  end
end
