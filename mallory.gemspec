# -*- encoding: utf-8 -*-
require File.expand_path('../lib/mallory/version', __FILE__)

Gem::Specification.new do |gem|
  gem.authors       = ["Braintree"]
  gem.email         = ["code@getbraintree.com"]
  gem.description   = %q{HTTPS Man-in-the-middle}
  gem.summary       = %q{Sometimes men in the middle are helpful}
  gem.homepage      = ""

  gem.files         = `git ls-files`.split($\)
  gem.executables   = gem.files.grep(%r{^bin/}).map{ |f| File.basename(f) }
  gem.test_files    = gem.files.grep(%r{^(test|spec|features)/})
  gem.name          = "mallory"
  gem.require_paths = ["lib"]
  gem.version       = Mallory::VERSION

  gem.add_dependency "thin",              "~> 1.3.1"
  gem.add_dependency "async-rack",        "~> 0.5.1"
  gem.add_dependency "sinatra",           "~> 1.0"
  gem.add_dependency "rack-fiber_pool",   "~> 0.9"
  gem.add_dependency "eventmachine",      "> 1.0.0.beta.1", "< 1.0.0.beta.100"
  gem.add_dependency "em-http-request",   "~> 1.0.2"
  gem.add_dependency "em-synchrony",      "~> 1.0.1"
  gem.add_dependency "em-resolv-replace", "~> 1.1"
  gem.add_dependency "em-syslog",         "~> 0.0.2"

  gem.add_development_dependency "rspec",       "~> 2.9.0"
  gem.add_development_dependency "rack-test",   "~> 0.6.1"
  gem.add_development_dependency "rake"
  gem.add_development_dependency "rake_commit", "~> 0.13"
end
