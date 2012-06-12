require 'spec_helper'

describe Mallory::Proxy do
  def app
    Mallory::Proxy
  end

  describe "POST /foo" do
    it "works" do
      post "/foo"

      last_response.body.should == "Hello /foo"
    end
  end
end
