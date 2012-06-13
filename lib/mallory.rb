require "sinatra/base"
require "sinatra/synchrony"
require "em-synchrony/em-http"
require "em/syslog"

require "thin"
require "thin/callbacks"
require "thin/backends/tcp_server_with_callbacks"
require "thin/callback_rack_handler"

require "mallory/logger"
require "mallory/proxy"
require "mallory/version"

require "mallory/extensions/em/http"

module Mallory
  class << self
    attr_accessor :target, :ca_file, :logger
  end

  self.logger = Mallory::Logger.new

  def self.setup!
    logger.setup!
  end
end
