module Mallory
  class Proxy < Sinatra::Base
    post "/*" do
      _proxy_request(:post, env["PATH_INFO"], env["QUERY_STRING"], env["rack.request.form_vars"])
    end

    get "/*" do
      _proxy_request(:get, env["PATH_INFO"], env["QUERY_STRING"])
    end

    put "/*" do
      _proxy_request(:put, env["PATH_INFO"], env["QUERY_STRING"])
    end

    delete "/*" do
      _proxy_request(:delete, env["PATH_INFO"], env["QUERY_STRING"])
    end

    def _proxy_request(http_method, path, query, body = nil)
      uri = URI.join(Mallory.target, path)
      uri.query = query
      connect_options = {}
      connect_options[:tls] = {:verify_peer => true, :cert_chain_file => Mallory.ca_file} if uri.scheme == "https"

      request_options = {}
      request_options[:body] = body unless body.nil?

      response = EM::HttpRequest.new(uri, connect_options).send(http_method, request_options)
      status = response.state == :finished ? response.response_header.status : 503
      [status, response.response_header, response.response]
    end
  end
end
