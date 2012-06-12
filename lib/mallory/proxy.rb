module Mallory
  class Proxy < Sinatra::Base
    post "/*" do
      path = "/#{params[:splat].first}"
      "Hello #{path}"
    end
  end
end
