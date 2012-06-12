class TestServer
  def self.start(port)
    server_start = system "env PID_FILE=/tmp/echo.pid SSL_TEST_PORT=#{port} spec/script/https_echo_server"
    raise "failed to start server" unless server_start
    wait_for_service :host => '127.0.0.1', :port => port
  end

  def self.stop
    system "kill -9 `cat /tmp/echo.pid`"
  end

  def self.wait_for_service(options = {})
    Timeout::timeout(options[:timeout] || 20) do
      loop do
        begin
          socket = TCPSocket.new(options[:host], options[:port])
          socket.close
          return
        rescue Exception
          sleep 0.5
        end
      end
    end
  end
end
