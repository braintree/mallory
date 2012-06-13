
app = proc do |env|
  body =  "#{env["REQUEST_METHOD"]}: #{env["PATH_INFO"]}\n"
  body += "QUERY: #{env["QUERY_STRING"]}\n"
  body += "POST BODY: #{env["rack.input"].read}\n"
  env.reject{ |k,v| k =~ /^rack/ }.each do |key, value|
    body += "#{key}: #{value}\n"
  end
  [200, {}, body]
end

run app
