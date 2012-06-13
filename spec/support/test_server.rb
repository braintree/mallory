class TestServer
  def self.start(port)
    options = [
      "--rackup spec/support/echo.ru",
      "--ssl",
      "--ssl-key-file spec/ssl/server.key",
      "--ssl-cert-file spec/ssl/server.crt",
      "--port #{port}",
      "--daemonize",
      "--pid /tmp/echo.pid",
      "--log /dev/null",
      "start"
    ]

    raise "failed to start server" unless system "bundle exec thin #{options.join(' ')}"
    wait_for_service :host => '127.0.0.1', :port => port
  end

  def self.stop
    system "bundle exec thin --pid /tmp/echo.pid stop 2>&1 > /dev/null"
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
