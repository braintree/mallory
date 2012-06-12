require 'spec_helper'

describe Mallory::VERSION do
  it "is not nil" do
    Mallory::VERSION.should_not be_nil
  end
end
