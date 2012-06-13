require 'em-http'
require 'openssl'

module DelegateVerifySSL
  def ssl_handshake_completed
    @parent.ssl_handshake_completed
  end

  def ssl_verify_peer(cert)
    @parent.ssl_verify_peer(cert)
  end
end

module VerifySSL
  def ssl_handshake_completed
    @conn.succeed
  end

  def ssl_verify_peer(peer_cert)
    key = OpenSSL::X509::Certificate.new(peer_cert)
    store = OpenSSL::X509::Store.new
    store.add_file(File.expand_path(@connopts.tls[:cert_chain_file]))
    store.verify(key) && OpenSSL::SSL.verify_certificate_identity(key, @connopts.host)
  end

  def start
    if client && client.req.ssl?
      @conn.start_tls(@connopts.tls)
    else
      @conn.succeed
    end
  end
end

EM::HttpStubConnection.send(:include, DelegateVerifySSL)
EM::HttpConnection.send(:include, VerifySSL)
