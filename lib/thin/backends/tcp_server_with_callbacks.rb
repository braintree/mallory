module Thin
  module Backends
    class TcpServerWithCallbacks < TcpServer
      def initialize(host, port, options)
        super(host, port)
      end

      def connect
        super
        Thin::Callbacks.after_connect_callbacks.each { |callback| callback.call }
      end

      def disconnect
        Thin::Callbacks.before_disconnect_callbacks.each { |callback| callback.call }
        super
      end
    end
  end
end

