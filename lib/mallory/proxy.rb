module Mallory
  class Proxy < Sinatra::Base
    post "/*" do
      _proxy_request(:post, env["PATH_INFO"])
    end

    def _proxy_request(http_method, path)
      uri = URI.join(Mallory.target, path)
      request_options = {}
      request_options[:ssl] = {:verify_peer => true, :cert_chain_file => Mallory.ca_file} if uri.scheme == "https"

      response = EM::HttpRequest.new(uri).send(http_method, request_options)
      response.response
    end
  end
end
