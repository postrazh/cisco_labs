import ssl

class Config:
    def __init__(self):
        self.hostname = "ise24.acme.local"
        self.nodename = "xxx3"
        self.password = "ekMynr9Zu1rpqgqj"
        self.description = ""

        self.clientcert = "win7vm.acme.local_192.168.128.114.cer"
        self.clientkey = "win7vm.acme.local_192.168.128.114.key"
        self.clientkeypassword = "Cisco123"
        self.isecert = "CertificateServicesRootCA-ise24_.cer"

    def get_host_name(self):
        return self.hostname

    def get_node_name(self):
        return self.nodename

    def get_password(self):
        if self.password is not None:
            return self.password
        else:
            return ''

    def get_description(self):
        return self.description

    def get_ssl_context(self):
        context = ssl.create_default_context()
        if self.clientcert is not None:
            context.load_cert_chain(certfile=self.clientcert,
                                    keyfile=self.clientkey,
                                    password=self.clientkeypassword)
            context.load_verify_locations(cafile=self.isecert)
            return context
        return None
