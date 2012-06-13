module Thin
  class Callbacks
    def self.after_connect_callbacks
      @after_connect_callbacks ||= []
    end

    def self.after_connect(&block)
      after_connect_callbacks << block
    end

    def self.before_disconnect_callbacks
      @before_disconnect_callbacks ||= []
    end

    def self.before_disconnect(&block)
      before_disconnect_callbacks << block
    end
  end
end
