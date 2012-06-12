require 'spec_helper'

describe Mallory::Proxy do
  def app
    Mallory::Proxy
  end

  run_in_reactor

  before(:all) do
    TestServer.start(9294)
  end

  after(:all) do
    TestServer.stop
  end

  before(:each) do
    Mallory.target = "https://127.0.0.1:9294"
    Mallory.ca_file = File.expand_path("../ssl/server.crt", File.dirname(__FILE__))
  end

  describe "SSL verification" do
    it "returns a 503 when the SSL cert does not verify" do
      Mallory.ca_file = File.expand_path("../ssl/badguy.crt", File.dirname(__FILE__))

      post "/foo"
      last_response.status.should == 503
    end

    it "returns a 503 when the SSL cert does not match the host" do
      Mallory.target = "https://localhost:9294"

      post "/foo"
      last_response.status.should == 503
    end

    it "verifies when the ca cert is a bunch of certs concatinated together" do
      Mallory.ca_file = File.expand_path("../ssl/ca-certificates.crt", File.dirname(__FILE__))

      post "/foo"
      last_response.body.should match("POST: /foo")
      last_response.status.should == 200
    end
  end

  describe "HTTP verbs" do
    it "POST proxies the traffic to the backend server" do
      post "/foo"

      last_response.body.should match("POST: /foo")
      last_response.status.should == 200
    end

    it "GET proxies the traffic to the backend server" do
      get "/foo"

      last_response.body.should match("GET: /foo")
      last_response.status.should == 200
    end

    it "PUT proxies the traffic to the backend server" do
      EM.stop
      pending "WEBrick does not support put"
      put "/foo"

      last_response.body.should match("PUT: /foo")
      last_response.status.should == 200
    end

    it "DELETE proxies the traffic to the backend server" do
      EM.stop
      pending "WEBrick does not support delete"
      delete "/foo"

      last_response.body.should match("DELETE: /foo")
      last_response.status.should == 200
    end
  end

  it "passes along query params" do
    post "/query?a=b&c=d"

    last_response.body.should match("QUERY: a=b&c=d")
    last_response.status.should == 200
  end

  it "passes along post body" do
    post "/body", "<xml>foo</xml>"

    last_response.body.should match("POST BODY: <xml>foo</xml>")
    last_response.status.should == 200
  end

  it "passes along headers" do
    post "/body", "<xml>foo</xml>", "HTTP_X_HEADER" => "foo", "CONTENT_TYPE" => "text/xml"

    last_response.body.should match("x_header: foo")
    last_response.body.should match("content_type: text/xml")
    last_response.status.should == 200
  end
end
