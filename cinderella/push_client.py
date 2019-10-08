import zmq
import json

class PushClient:
    def __init__(self,  ip, push_port, req_port):
        self.context = zmq.Context()
        self.push = self.context.socket(zmq.PUSH)
        self.push.connect("tcp://%s:%s" % (ip, push_port))
        self.req = self.context.socket(zmq.REQ)
        self.req.connect('tcp://%s:%s' % (ip, req_port))
    
    def push_message(self, flags, msg):
        context = json.dumps(msg)
        self.push.send_multipart([flags, str.encode(context)]);

    def request(self, flags, msg):
        context = json.dumps(msg)
        self.req.send_multipart([flags, str.encode(context)]);
        message = self.req.recv()
        return {'balance': float(message.decode('ascii'))}
        
