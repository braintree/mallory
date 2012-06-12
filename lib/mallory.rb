require "sinatra/base"
require "sinatra/synchrony"
require "em-synchrony/em-http"

require "mallory/proxy"
require "mallory/version"

module Mallory
  class << self
    attr_accessor :target, :ca_file
  end
end
