require 'spec_helper'

describe Mallory::Proxy do
  def app
    Mallory::Proxy
  end

  run_in_reactor

  before(:all) do
    TestServer.start(9294)
    Mallory.target = "https://127.0.0.1:9294"
    Mallory.ca_file = File.expand_path("../ssl/server.crt", File.dirname(__FILE__))
  end

  after(:all) do
    TestServer.stop
  end

  describe "POST /foo" do
    it "proxies the traffic to the backend server" do
      post "/foo"

      last_response.body.should == "POST: /foo"
    end
  end
end
