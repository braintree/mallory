$LOAD_PATH.unshift File.expand_path('lib', File.dirname(__FILE__))
require 'mallory'

use Rack::CommonLogger, Mallory.logger
run Mallory::Proxy
