# -*- encoding: utf-8 -*-
require File.expand_path('../lib/mallory/version', __FILE__)

Gem::Specification.new do |gem|
  gem.authors       = ["TODO: Write your name"]
  gem.email         = ["code@getbraintree.com"]
  gem.description   = %q{TODO: Write a gem description}
  gem.summary       = %q{TODO: Write a gem summary}
  gem.homepage      = ""

  gem.files         = `git ls-files`.split($\)
  gem.executables   = gem.files.grep(%r{^bin/}).map{ |f| File.basename(f) }
  gem.test_files    = gem.files.grep(%r{^(test|spec|features)/})
  gem.name          = "mallory"
  gem.require_paths = ["lib"]
  gem.version       = Mallory::VERSION

  gem.add_dependency "em-http-request", "~> 1.0.2"
  gem.add_dependency "em-synchrony", "~> 1.0.1"
  gem.add_dependency "thin", "~> 1.3.1"

  gem.add_development_dependency "rspec", "2.10.0"
end
