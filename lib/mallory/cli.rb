module Mallory
  class CLI < Rack::Server
    class Options
      def parse!(args)
        args, options = args.dup, {}

        opt_parser = OptionParser.new do |opts|
          opts.banner = "Usage: mallory [options]"
          opts.on("-t", "--target=URI", String, "Proxy target") { |v| options[:proxy_target] = v }
          opts.on("--proxy-ca-cert=FILE", String, "CA Certificate for validating the proxy target's SSL") { |v| options[:proxy_ca_cert] = v }

          opts.separator ""

          opts.on("-p", "--port=port", Integer, "Runs Litmus on the specified port.", "Default: 9292") { |v| options[:Port] = v }
          opts.on("-b", "--binding=ip", String, "Binds Litmus to the specified ip.", "Default: 0.0.0.0") { |v| options[:Host] = v }
          opts.on("-d", "--daemon", "Make server run as a Daemon.") { options[:daemonize] = true }
          opts.on("-P","--pid=pid",String, "Specifies the PID file.", "Default: rack.pid") { |v| options[:pid] = v }
          opts.on("--ssl", "Enables SSL") { options[:ssl] = true }
          opts.on("--ssl-key-file=FILE", String, "Path to server's private key") { |v| options[:ssl_key_file] = v }
          opts.on("--ssl-cert-file=FILE", String, "Path to server's certificate") { |v| options[:ssl_cert_file] = v }

          opts.separator ""

          opts.on("-h", "--help", "Show this help message.") { puts opts; exit }
        end

        opt_parser.parse! args

        options[:config] = File.expand_path("../../config.ru", File.dirname(__FILE__))
        options[:server] = 'thin-with-callbacks'
        options[:backend] = Thin::Backends::TcpServerWithCallbacks
        options
      end
    end

    def opt_parser
      Options.new
    end

    def start
      assert_required_options!

      Mallory.target = options[:proxy_target]
      Mallory.ca_file = options[:proxy_ca_cert]

      Thin::Callbacks.after_connect do
        Mallory.setup!
      end

      super
    end

    def assert_required_options!
      missing_options = []
      missing_options << "--target" unless options.has_key? :proxy_target
      missing_options << "--proxy-ca-cert" unless options.has_key? :proxy_ca_cert

      if missing_options.any?
        missing_options.each { |option| puts "Missing required option #{option}" }
        exit 1
      end
    end
  end
end
