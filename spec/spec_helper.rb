ENV['RACK_ENV'] = 'test'

require 'mallory'
require 'rspec'
require 'rack/test'

Dir.glob("#{File.expand_path('support', File.dirname(__FILE__))}/**/*.rb").each { |f| require f }

RSpec.configure do |config|
  config.expect_with :rspec
  config.include Rack::Test::Methods
end

def run_in_reactor(timeout = 5)
  around(:each) do |spec|
    EM.synchrony do
      sig = EM.add_timer(timeout) { fail "timeout!"; EM.stop }
      spec.run
      EM.cancel_timer(sig)
      EM.stop
    end
  end
end
