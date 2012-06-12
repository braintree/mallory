module Mallory
  class Proxy < Sinatra::Base
    post "/*" do
      _proxy_request(:post, env["PATH_INFO"])
    end

    get "/*" do
      _proxy_request(:get, env["PATH_INFO"])
    end

    put "/*" do
      _proxy_request(:put, env["PATH_INFO"])
    end

    delete "/*" do
      _proxy_request(:delete, env["PATH_INFO"])
    end

    def _proxy_request(http_method, path)
      uri = URI.join(Mallory.target, path)
      request_options = {}
      request_options[:tls] = {:verify_peer => true, :cert_chain_file => Mallory.ca_file} if uri.scheme == "https"

      response = EM::HttpRequest.new(uri, request_options).send(http_method)
      status = response.state == :finished ? response.response_header.status : 503
      [status, response.response_header, response.response]
    end
  end
end
