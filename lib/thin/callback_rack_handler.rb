module Thin
  class CallbackRackHandler
    def self.run(app, options)
      server = ::Thin::Server.new(options[:Host] || '0.0.0.0',
                                  options[:Port] || 8080,
                                  app,
                                  options)
      yield server if block_given?

      if options[:ssl]
        server.ssl = true
        server.ssl_options = { :private_key_file => options[:ssl_key_file], :cert_chain_file => options[:ssl_cert_file], :verify_peer => options[:ssl_verify] }
      end
      server.start
    end
  end
end

Rack::Handler.register 'thin-with-callbacks', Thin::CallbackRackHandler
