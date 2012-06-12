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

  describe "POST /foo" do
    before(:each) do
      Mallory.target = "https://127.0.0.1:9294"
      Mallory.ca_file = File.expand_path("../ssl/server.crt", File.dirname(__FILE__))
    end

    it "proxies the traffic to the backend server" do
      post "/foo"

      last_response.body.should == "POST: /foo"
      last_response.status.should == 200
    end

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
      last_response.body.should == "POST: /foo"
      last_response.status.should == 200
    end
  end
end
