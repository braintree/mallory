task :clean do
  rm_rf "build"
  rm_rf "dist"
  rm_f "MANIFEST"
end

task :test do
  sh "nosetests test/"
end

namespace :pypi do
  desc "Upload a new version to PyPI"
  task :upload => :clean do
    sh "python setup.py sdist upload"
  end
end

task :default => ['test']
